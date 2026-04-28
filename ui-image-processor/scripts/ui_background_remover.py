#!/usr/bin/env python3
"""
UI Background Remover - 洪水填充 + 激进腐蚀 + 颜色融合

核心算法（已验证有效）：
1. 洪水填充：从图片边缘删除白色背景
2. 多轮激进腐蚀：亮度阈值从高到低递减，把毛边压到最小
3. 颜色融合：对极少量残留像素染色（融入相邻UI颜色）

特点：
- 只删除与边缘相连的白色，保留UI内部白色
- 专门处理AI生成的"偏蓝白"毛边（深蓝主题混边）
- 15轮渐进腐蚀 + 最终融合，边缘干净平滑
"""

import argparse
import json
import math
from pathlib import Path
from PIL import Image
from collections import deque
from typing import Tuple, Set, List, Optional


def is_white_pixel(pixel: Tuple[int, int, int, int], threshold: int = 250) -> bool:
    """判断像素是否为白色（RGB三通道都≥阈值）"""
    r, g, b, a = pixel if len(pixel) == 4 else (*pixel, 255)
    if a == 0:
        return False
    return r >= threshold and g >= threshold and b >= threshold


def is_fringe_pixel(r: int, g: int, b: int, a: int, brightness_min: float) -> bool:
    """
    判断是否为毛边像素
    
    检测两种类型：
    1. 偏蓝白：B通道最大，B≥170，亮度≥brightness_min（AI生成深蓝主题混边）
    2. 灰色：低饱和度(<0.25)，亮度≥brightness_min（抗锯齿灰边）
    """
    if a == 0:
        return False
    
    brightness = (r + g + b) / 3
    
    # 偏蓝白毛边（B通道主导）
    if b >= r and b >= g and b >= 170 and brightness >= brightness_min:
        return True
    
    # 灰色毛边（低饱和度）
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    if max_c > 0:
        saturation = (max_c - min_c) / max_c
        if saturation < 0.25 and brightness >= brightness_min:
            return True
    
    return False


def flood_fill_remove_bg(
    image: Image.Image,
    threshold: int = 250
) -> Tuple[Image.Image, int]:
    """
    洪水填充法：从图片四边开始删除与边缘相连的白色区域
    
    Returns:
        (处理后的Image, 清理的像素数量)
    """
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    width, height = image.size
    pixels = image.load()
    
    processed: Set[Tuple[int, int]] = set()
    to_transparent: Set[Tuple[int, int]] = set()
    queue = deque()
    
    # 从四条边缘收集起始点
    for x in range(width):
        if is_white_pixel(pixels[x, 0], threshold):
            queue.append((x, 0))
        if is_white_pixel(pixels[x, height - 1], threshold):
            queue.append((x, height - 1))
    for y in range(height):
        if is_white_pixel(pixels[0, y], threshold):
            queue.append((0, y))
        if is_white_pixel(pixels[width - 1, y], threshold):
            queue.append((width - 1, y))
    
    # BFS洪水填充
    while queue:
        x, y = queue.popleft()
        
        if (x, y) in processed:
            continue
        if x < 0 or x >= width or y < 0 or y >= height:
            continue
        if not is_white_pixel(pixels[x, y], threshold):
            continue
        
        processed.add((x, y))
        to_transparent.add((x, y))
        
        # 4方向扩展
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            queue.append((x + dx, y + dy))
    
    # 将标记的像素设为透明
    for x, y in to_transparent:
        pixels[x, y] = (255, 255, 255, 0)
    
    return image, len(to_transparent)


def aggressive_erosion(
    image: Image.Image,
    rounds: int = 15,
    start_brightness: int = 220,
    end_brightness: int = 80,
    verbose: bool = False
) -> Tuple[Image.Image, int]:
    """
    多轮激进腐蚀：从外向内收缩毛边
    
    每轮降低亮度阈值，清理更多边缘像素
    透明邻居越多，腐蚀阈值越低（更激进）
    
    Args:
        image: PIL Image（已做洪水填充）
        rounds: 腐蚀轮数
        start_brightness: 起始亮度阈值
        end_brightness: 最终亮度阈值
        verbose: 是否打印进度
    
    Returns:
        (处理后的Image, 总腐蚀像素数)
    """
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    width, height = image.size
    pixels = image.load()
    
    # 每轮亮度递减幅度
    brightness_step = (start_brightness - end_brightness) / rounds
    
    total_eroded = 0
    
    for round_num in range(rounds):
        # 当前亮度阈值
        brightness_min = start_brightness - round_num * brightness_step
        
        # 找到透明边界像素
        boundary: List[Tuple[int, int, int]] = []
        
        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]
                if a > 0:
                    # 计算8方向透明邻居数量
                    trans_count = 0
                    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < width and 0 <= ny < height:
                            if pixels[nx, ny][3] == 0:
                                trans_count += 1
                    
                    if trans_count > 0:
                        boundary.append((x, y, trans_count))
        
        # 腐蚀边界上的毛边像素
        eroded = 0
        for x, y, trans_count in boundary:
            r, g, b, a = pixels[x, y]
            
            # 透明邻居越多，阈值越低（更激进）
            effective_min = brightness_min - trans_count * 5
            
            if is_fringe_pixel(r, g, b, a, effective_min):
                pixels[x, y] = (255, 255, 255, 0)
                eroded += 1
        
        total_eroded += eroded
        
        if verbose and eroded > 0:
            print(f"  [腐蚀 {round_num + 1}] 阈值={int(brightness_min)} 清理 {eroded} 个")
        
        # 提前终止：腐蚀5轮后如果清理量很少，停止
        if round_num >= 5 and eroded < 50:
            break
    
    return image, total_eroded


def find_ui_color(
    x: int, y: int,
    pixels: any,
    width: int, height: int,
    max_dist: int = 20
) -> Optional[Tuple[int, int, int]]:
    """
    向内搜索UI实色像素
    
    从毛边像素位置向内搜索，找到最近的非毛边UI颜色
    """
    # 先沿4个主方向搜索（最快）
    for dist in range(1, max_dist + 1):
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx * dist, y + dy * dist
            if 0 <= nx < width and 0 <= ny < height:
                nr, ng, nb, na = pixels[nx, ny]
                if na > 0 and not is_fringe_pixel(nr, ng, nb, na, 100):
                    return (nr, ng, nb)
    
    # 如果主方向没找到，用圆周搜索
    for r in range(2, max_dist + 1):
        for angle in range(0, 360, 45):
            dx = int(r * math.cos(math.radians(angle)))
            dy = int(r * math.sin(math.radians(angle)))
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                nr, ng, nb, na = pixels[nx, ny]
                if na > 0 and not is_fringe_pixel(nr, ng, nb, na, 100):
                    return (nr, ng, nb)
    
    return None


def blend_fringe_pixels(
    image: Image.Image,
    blend_strength: float = 0.9,
    verbose: bool = False
) -> Tuple[Image.Image, int]:
    """
    颜色融合：对残留的极少量毛边像素染色
    
    将毛边颜色与相邻UI颜色混合，融入UI元素
    
    Args:
        image: PIL Image（已做腐蚀）
        blend_strength: 融合强度（0.9 = 90% UI颜色 + 10% 原色）
        verbose: 是否打印进度
    
    Returns:
        (处理后的Image, 融合像素数)
    """
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    width, height = image.size
    pixels = image.load()
    
    # 找到残留的毛边像素
    remaining_fringe: List[Tuple[int, int]] = []
    
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if a > 0 and is_fringe_pixel(r, g, b, a, 100):
                # 检查有透明邻居
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        if pixels[nx, ny][3] == 0:
                            remaining_fringe.append((x, y))
                            break
    
    # 颜色融合
    blended = 0
    for x, y in remaining_fringe:
        r, g, b, a = pixels[x, y]
        ui_color = find_ui_color(x, y, pixels, width, height, max_dist=20)
        
        if ui_color:
            ur, ug, ub = ui_color
            # 混合：blend_strength比例的UI颜色
            new_r = int(r * (1 - blend_strength) + ur * blend_strength)
            new_g = int(g * (1 - blend_strength) + ug * blend_strength)
            new_b = int(b * (1 - blend_strength) + ub * blend_strength)
            pixels[x, y] = (new_r, new_g, new_b, a)
            blended += 1
    
    if verbose:
        print(f"  [融合] 染色 {blended} 个残留毛边")
    
    return image, blended


def remove_background(
    input_path: str,
    output_path: str,
    flood_threshold: int = 250,
    erosion_rounds: int = 15,
    blend_strength: float = 0.9,
    verbose: bool = True
) -> dict:
    """
    去背景完整流程：洪水填充 + 激进腐蚀 + 颜色融合
    
    Args:
        input_path: 输入图片路径
        output_path: 输出图片路径
        flood_threshold: 洪水填充白色阈值（默认250）
        erosion_rounds: 腐蚀轮数（默认15）
        blend_strength: 融合强度（默认0.9）
        verbose: 是否打印进度
    
    Returns:
        处理结果信息
    """
    input_path = Path(input_path)
    output_path = Path(output_path)
    
    # 加载图片
    image = Image.open(input_path)
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    original_size = image.size
    
    if verbose:
        print(f"[去背景] 输入: {input_path}")
        print(f"[去背景] 尺寸: {original_size[0]}x{original_size[1]}")
    
    # 第1步：洪水填充去背景
    image, bg_removed = flood_fill_remove_bg(image, flood_threshold)
    if verbose:
        print(f"  [洪水填充] 清理 {bg_removed} 个背景像素")
    
    # 第2步：多轮激进腐蚀
    image, eroded = aggressive_erosion(
        image,
        rounds=erosion_rounds,
        verbose=verbose
    )
    if verbose:
        print(f"  [腐蚀总计] 清理 {eroded} 个毛边像素")
    
    # 第3步：颜色融合残留
    image, blended = blend_fringe_pixels(image, blend_strength, verbose)
    
    # 保存结果
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path, 'PNG')
    
    if verbose:
        print(f"[去背景] ✓ 输出: {output_path}")
    
    return {
        'success': True,
        'input': str(input_path),
        'output': str(output_path),
        'original_size': original_size,
        'bg_removed': bg_removed,
        'fringe_eroded': eroded,
        'fringe_blended': blended,
        'params': {
            'flood_threshold': flood_threshold,
            'erosion_rounds': erosion_rounds,
            'blend_strength': blend_strength
        }
    }


def batch_process(batch_json: str) -> List[dict]:
    """批量处理"""
    batch_path = Path(batch_json)
    
    with open(batch_path, 'r', encoding='utf-8') as f:
        tasks = json.load(f)
    
    results = []
    
    for task in tasks:
        try:
            result = remove_background(
                input_path=task['input'],
                output_path=task['output'],
                flood_threshold=task.get('flood_threshold', 250),
                erosion_rounds=task.get('erosion_rounds', 15),
                blend_strength=task.get('blend_strength', 0.9),
                verbose=task.get('verbose', False)
            )
            results.append(result)
        except Exception as e:
            results.append({
                'success': False,
                'input': task.get('input'),
                'error': str(e)
            })
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description='UI Background Remover - 洪水填充 + 激进腐蚀 + 颜色融合'
    )
    
    parser.add_argument('--input', '-i', type=str,
                        help='输入图片路径')
    parser.add_argument('--output', '-o', type=str,
                        help='输出图片路径')
    parser.add_argument('--threshold', '-t', type=int, default=250,
                        help='洪水填充白色阈值（默认250）')
    parser.add_argument('--erosion', '-e', type=int, default=15,
                        help='腐蚀轮数（默认15）')
    parser.add_argument('--blend', '-b', type=float, default=0.9,
                        help='融合强度（默认0.9，即90%UI颜色）')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='安静模式，不打印进度')
    parser.add_argument('--batch', type=str,
                        help='批量处理JSON文件')
    
    args = parser.parse_args()
    
    # 批量处理
    if args.batch:
        results = batch_process(args.batch)
        success = sum(1 for r in results if r.get('success'))
        print(f'[批量] 完成: {success}/{len(results)}')
        for r in results:
            if r.get('success'):
                print(f'  ✓ {r["input"]} → {r["output"]}')
            else:
                print(f'  ✗ {r.get("input")}: {r.get("error")}')
        return
    
    # 单图处理
    if not args.input or not args.output:
        parser.error('请提供 --input 和 --output')
    
    remove_background(
        input_path=args.input,
        output_path=args.output,
        flood_threshold=args.threshold,
        erosion_rounds=args.erosion,
        blend_strength=args.blend,
        verbose=not args.quiet
    )


if __name__ == '__main__':
    main()