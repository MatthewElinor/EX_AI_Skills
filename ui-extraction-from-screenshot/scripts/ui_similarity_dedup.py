#!/usr/bin/env python3
"""
UI相似度去重工具 - 检测并合并样式相似的UI元素

核心算法：
1. 感知哈希（Perceptual Hash）- 相似图片有相似哈希
2. 汉明距离比较 - 哈希差异小的视为相似
3. 分组去重 - 每组保留最优版本

用法：
    python ui_similarity_dedup.py --input-dir ./sprites/ --output-dir ./deduped/
"""

import os
import sys
import argparse
import shutil
from pathlib import Path
from collections import defaultdict

try:
    from PIL import Image
except ImportError:
    print("请安装 Pillow: pip install Pillow")
    sys.exit(1)


def compute_phash(image_path: str, hash_size: int = 16) -> int:
    """
    计算图片的感知哈希（Perceptual Hash）
    
    原理：
    1. 缩小图片到 hash_size+1 × hash_size
    2. 转灰度
    3. 比较相邻像素亮度
    4. 生成二进制哈希
    
    Args:
        image_path: 图片路径
        hash_size: 哈希尺寸，越大越精确（默认16，生成256位哈希）
    
    Returns:
        整数形式的哈希值
    """
    try:
        img = Image.open(image_path)
        
        # 转为 RGBA，确保透明通道处理
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # 创建白色背景合成（透明区域变白）
        background = Image.new('RGBA', img.size, (255, 255, 255, 255))
        img = Image.alpha_composite(background, img)
        
        # 转灰度
        img = img.convert('L')
        
        # 缩小到 (hash_size+1) × hash_size
        img = img.resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
        
        # 计算差分哈希：比较相邻像素
        pixels = list(img.get_flattened_data())
        hash_value = 0
        
        for y in range(hash_size):
            for x in range(hash_size):
                idx = y * (hash_size + 1) + x
                # 当前像素 vs 右边像素
                if pixels[idx] > pixels[idx + 1]:
                    hash_value |= 1 << (y * hash_size + x)
        
        return hash_value
        
    except Exception as e:
        print(f"计算哈希失败 {image_path}: {e}")
        return 0


def hamming_distance(hash1: int, hash2: int) -> int:
    """
    计算两个哈希的汉明距离（不同位的数量）
    """
    return bin(hash1 ^ hash2).count('1')


def find_similar_groups(images: list, threshold: int = 10, hash_size: int = 16) -> dict:
    """
    找出相似的图片组
    
    Args:
        images: 图片路径列表
        threshold: 汉明距离阈值，小于等于此值视为相似（默认10，对于256位哈希约4%差异）
        hash_size: 哈希尺寸
    
    Returns:
        {组ID: [图片路径列表]}
    """
    print(f"\n计算 {len(images)} 张图片的感知哈希...")
    
    # 计算所有图片的哈希
    hashes = {}
    for img_path in images:
        h = compute_phash(img_path, hash_size)
        hashes[img_path] = h
    
    # 分组：使用并查集思想
    groups = defaultdict(list)
    visited = set()
    group_id = 0
    
    for i, img1 in enumerate(images):
        if img1 in visited:
            continue
        
        # 找所有与 img1 相似的图片
        similar = [img1]
        visited.add(img1)
        
        for img2 in images[i+1:]:
            if img2 in visited:
                continue
            
            distance = hamming_distance(hashes[img1], hashes[img2])
            if distance <= threshold:
                similar.append(img2)
                visited.add(img2)
        
        groups[group_id] = similar
        group_id += 1
    
    return dict(groups)


def get_image_quality_score(image_path: str) -> float:
    """
    评估图片质量分数（用于选择保留哪个版本）
    
    评分标准：
    - 分辨率：越大越好
    - 文件大小：越大说明细节越多（不绝对，但可作为参考）
    - 透明度：完全透明或完全不透明的更"干净"
    """
    try:
        img = Image.open(image_path)
        width, height = img.size
        file_size = os.path.getsize(image_path)
        
        # 分辨率分数（归一化到 0-100）
        res_score = min(100, (width * height) / 10000)  # 10000像素=1分
        
        # 文件大小分数（归一化）
        size_score = min(50, file_size / 1000)  # 1KB=1分
        
        return res_score + size_score
        
    except Exception:
        return 0


def select_best_image(images: list) -> str:
    """从相似组中选择质量最好的图片"""
    if len(images) == 1:
        return images[0]
    
    scores = [(img, get_image_quality_score(img)) for img in images]
    scores.sort(key=lambda x: x[1], reverse=True)
    
    return scores[0][0]


def deduplicate_ui(input_dir: str, output_dir: str, threshold: int = 10, 
                   hash_size: int = 16, copy_mode: bool = True, quiet: bool = False):
    """
    主函数：去重处理
    
    Args:
        input_dir: 输入目录（切图后的UI元素）
        output_dir: 输出目录（去重后的UI元素）
        threshold: 汉明距离阈值（默认10，约4%差异）
        hash_size: 哈希尺寸（默认16）
        copy_mode: True=复制文件，False=移动文件
        quiet: 安静模式
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    if not input_path.exists():
        print(f"错误：输入目录不存在 {input_dir}")
        return
    
    # 支持的图片格式
    image_extensions = {'.png', '.jpg', '.jpeg', '.webp', '.bmp'}
    images = [str(f) for f in input_path.iterdir() if f.suffix.lower() in image_extensions]
    
    if not images:
        print(f"错误：输入目录没有图片文件 {input_dir}")
        return
    
    print(f"找到 {len(images)} 张图片")
    
    # 找相似组
    groups = find_similar_groups(images, threshold, hash_size)
    
    # 统计
    total_groups = len(groups)
    unique_count = sum(1 for g in groups.values() if len(g) == 1)
    similar_groups = {k: v for k, v in groups.items() if len(v) > 1}
    duplicate_count = sum(len(v) - 1 for v in similar_groups.values())
    
    print(f"\n=== 相似度分析结果 ===")
    print(f"总图片数: {len(images)}")
    print(f"唯一元素: {unique_count}")
    print(f"相似组数: {len(similar_groups)}")
    print(f"重复元素: {duplicate_count}")
    print(f"去重后保留: {len(images) - duplicate_count}")
    
    if similar_groups:
        print(f"\n=== 相似组详情 ===")
        for gid, imgs in similar_groups.items():
            print(f"\n组 {gid + 1} ({len(imgs)}张相似):")
            for img in imgs:
                score = get_image_quality_score(img)
                print(f"  - {Path(img).name} (质量分: {score:.1f})")
    
    # 创建输出目录
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 创建重复文件夹（存放被过滤的）
    dup_path = output_path / "_duplicates"
    dup_path.mkdir(parents=True, exist_ok=True)
    
    # 处理
    kept_count = 0
    moved_count = 0
    
    for gid, imgs in groups.items():
        if len(imgs) == 1:
            # 唯一元素，直接复制
            src = imgs[0]
            dst = output_path / Path(src).name
            if copy_mode:
                shutil.copy2(src, dst)
            else:
                shutil.move(src, dst)
            kept_count += 1
        else:
            # 相似组，选最优保留，其他移到重复文件夹
            best = select_best_image(imgs)
            
            # 保留最优
            dst = output_path / Path(best).name
            if copy_mode:
                shutil.copy2(best, dst)
            else:
                shutil.move(best, dst)
            kept_count += 1
            
            # 其他移到重复文件夹
            for img in imgs:
                if img != best:
                    dst = dup_path / Path(img).name
                    if copy_mode:
                        shutil.copy2(img, dst)
                    else:
                        shutil.move(img, dst)
                    moved_count += 1
    
    print(f"\n=== 处理完成 ===")
    print(f"保留到 {output_dir}: {kept_count} 张")
    print(f"重复元素移到 {dup_path}: {moved_count} 张")


def main():
    parser = argparse.ArgumentParser(
        description='UI相似度去重工具 - 检测并合并样式相似的UI元素',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 基础用法
  python ui_similarity_dedup.py -i ./sprites/ -o ./deduped/
  
  # 调整相似度阈值（值越大，判断越宽松）
  python ui_similarity_dedup.py -i ./sprites/ -o ./deduped/ --threshold 15
  
  # 更精确的哈希（更大的hash_size）
  python ui_similarity_dedup.py -i ./sprites/ -o ./deduped/ --hash-size 24
  
  # 移动模式（不保留原文件）
  python ui_similarity_dedup.py -i ./sprites/ -o ./deduped/ --move

参数说明：
  threshold: 汉明距离阈值，默认10。对于16x16=256位哈希，10约等于4%差异。
             - 5-8: 严格，只合并高度相似的
             - 10-15: 默认，平衡
             - 20+: 宽松，可能误判
             
  hash-size: 哈希尺寸，影响精确度。
             - 8: 快速但粗糙（64位哈希）
             - 16: 默认平衡（256位哈希）
             - 24+: 精确但慢（576+位哈希）
        """
    )
    
    parser.add_argument('-i', '--input-dir', required=True, help='输入目录（切图后的UI元素）')
    parser.add_argument('-o', '--output-dir', required=True, help='输出目录（去重后的UI元素）')
    parser.add_argument('-t', '--threshold', type=int, default=10, 
                        help='汉明距离阈值，默认10（约4%%差异）')
    parser.add_argument('--hash-size', type=int, default=16,
                        help='哈希尺寸，默认16（256位哈希）')
    parser.add_argument('--move', action='store_true',
                        help='移动模式（删除原文件），默认复制模式')
    parser.add_argument('-q', '--quiet', action='store_true', help='安静模式')
    
    args = parser.parse_args()
    
    deduplicate_ui(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        threshold=args.threshold,
        hash_size=args.hash_size,
        copy_mode=not args.move,
        quiet=args.quiet
    )


if __name__ == '__main__':
    main()