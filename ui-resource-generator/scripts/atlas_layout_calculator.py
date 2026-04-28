#!/usr/bin/env python3
"""
UI图集布局计算器

根据用户需求的UI数量和单个尺寸，智能计算最优的图集布局。

使用方法：
  python atlas_layout_calculator.py --count 10 --width 100 --height 30
  
输出：
  JSON格式的布局信息，包含行列数、图集尺寸、间距等
"""

import argparse
import json

# ikunimage支持的标准尺寸
SUPPORTED_SIZES = [1024, 1536, 2048]

# 最大图集尺寸
MAX_ATLAS = 2048

# 默认间距（加大以提高AI生图容错）
DEFAULT_SPACING = 30


def get_ikunimage_params(width, height):
    """
    根据图集尺寸计算ikunimage参数
    
    ikunimage支持：
    - aspect_ratio: 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3, 21:9, 5:4, 4:5
    - size: 1K, 2K, 4K
    
    Args:
        width: 图集宽度
        height: 图集高度
    
    Returns:
        dict: {'aspect_ratio': str, 'size': str}
    """
    # 计算宽高比
    ratio = width / height
    
    # 选择最接近的aspect_ratio
    aspect_ratios = {
        '1:1': 1.0,
        '4:3': 4/3,
        '3:4': 3/4,
        '3:2': 1.5,
        '2:3': 2/3,
        '16:9': 16/9,
        '9:16': 9/16,
        '5:4': 1.25,
        '4:5': 0.8,
        '21:9': 21/9,
    }
    
    best_ar = '1:1'
    best_diff = float('inf')
    
    for ar_name, ar_value in aspect_ratios.items():
        diff = abs(ratio - ar_value)
        if diff < best_diff:
            best_diff = diff
            best_ar = ar_name
    
    # 根据尺寸选择size
    # ikunimage的size大致对应：1K~1024, 2K~2048, 4K~4096（但最大2048）
    max_dim = max(width, height)
    if max_dim <= 1024:
        size = '1K'
    elif max_dim <= 2048:
        size = '2K'
    else:
        size = '4K'
    
    return {'aspect_ratio': best_ar, 'size': size}


def align_to_supported(size):
    """将尺寸对齐到ikunimage支持的值"""
    for s in SUPPORTED_SIZES:
        if size <= s:
            return s
    return SUPPORTED_SIZES[-1]


def calculate_atlas_layout(count, width, height, spacing=DEFAULT_SPACING):
    """
    计算最优图集布局
    
    Args:
        count: UI数量
        width: 单个UI宽度（≤1024）
        height: 单个UI高度（≤1024）
        spacing: UI元素间距（像素）
    
    Returns:
        dict: 布局信息
    """
    # 验证单个UI尺寸
    if width > 1024 or height > 1024:
        return {
            'error': '单个UI尺寸不能超过1024×1024',
            'valid': False
        }
    
    # 计算单个UI占用空间（含间距）
    cell_w = width + spacing
    cell_h = height + spacing
    
    # 计算最大可容纳数量
    max_cols = MAX_ATLAS // cell_w
    max_rows = MAX_ATLAS // cell_h
    max_count = max_cols * max_rows
    
    if max_cols == 0 or max_rows == 0:
        return {
            'error': f'单个UI尺寸({width}×{height})加上间距后超过图集最大尺寸',
            'valid': False
        }
    
    # 如果要求数量超过最大容量，取最大容量
    actual_count = min(count, max_count)
    
    if actual_count < count:
        print(f"⚠️ 数量调整：{count} → {actual_count}（图集容量限制）")
    
    # 计算最优行列数（尽量接近正方形布局，减少空白）
    best_cols = 1
    best_rows = actual_count
    best_ratio = float('inf')
    
    for cols in range(1, max_cols + 1):
        rows = (actual_count + cols - 1) // cols  # 向上取整
        if rows > max_rows:
            continue
        # 优先选择行数较少的布局（更紧凑）
        ratio = rows * 100 + abs(cols - rows)
        if ratio < best_ratio:
            best_ratio = ratio
            best_cols = cols
            best_rows = rows
    
    # 计算图集尺寸（含边距）
    raw_width = best_cols * cell_w + spacing
    raw_height = best_rows * cell_h + spacing
    
    # 对齐到ikunimage支持的尺寸
    atlas_width = align_to_supported(raw_width)
    atlas_height = align_to_supported(raw_height)
    
    # 计算ikunimage参数
    ikun_params = get_ikunimage_params(atlas_width, atlas_height)
    
    return {
        'valid': True,
        'input': {
            'count': count,
            'width': width,
            'height': height,
            'spacing': spacing
        },
        'output': {
            'cols': best_cols,
            'rows': best_rows,
            'atlas_width': atlas_width,
            'atlas_height': atlas_height,
            'actual_count': actual_count,
            'spacing': spacing
        },
        'ikunimage': ikun_params,
        'prompt_info': {
            'arrangement': f"{best_cols} columns and {best_rows} rows",
            'element_size': f"{width}×{height}",
            'atlas_size': f"{atlas_width}×{atlas_height}",
            'aspect_ratio': ikun_params['aspect_ratio'],
            'size': ikun_params['size']
        }
    }


def main():
    parser = argparse.ArgumentParser(description='UI图集布局计算器')
    parser.add_argument('--count', '-c', type=int, required=True,
                        help='UI数量')
    parser.add_argument('--width', '-w', type=int, required=True,
                        help='单个UI宽度')
    parser.add_argument('--height', '-H', type=int, required=True,
                        help='单个UI高度')
    parser.add_argument('--spacing', '-s', type=int, default=DEFAULT_SPACING,
                        help=f'间距（默认{DEFAULT_SPACING}像素）')
    parser.add_argument('--json', '-j', action='store_true',
                        help='输出JSON格式')
    
    args = parser.parse_args()
    
    result = calculate_atlas_layout(
        count=args.count,
        width=args.width,
        height=args.height,
        spacing=args.spacing
    )
    
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if not result['valid']:
            print(f"❌ {result['error']}")
            return 1
        
        print("=" * 50)
        print("📐 UI图集布局计算结果")
        print("=" * 50)
        print(f"输入：{args.count}个UI，每个{args.width}×{args.height}像素")
        print(f"间距：{args.spacing}像素")
        print("-" * 50)
        print(f"布局：{result['output']['cols']}列 × {result['output']['rows']}行")
        print(f"图集尺寸：{result['output']['atlas_width']}×{result['output']['atlas_height']}像素")
        print(f"实际数量：{result['output']['actual_count']}个")
        
        if result['output']['actual_count'] < args.count:
            print(f"⚠️  注意：数量被调整为{result['output']['actual_count']}（容量限制）")
        
        print("-" * 50)
        print("📝 生图提示词片段：")
        print(f"   arrangement: \"{result['prompt_info']['arrangement']}\"")
        print(f"   element size: \"{result['prompt_info']['element_size']}\"")
        print(f"   atlas size: \"{result['prompt_info']['atlas_size']}\"")
        print("-" * 50)
        print("🎨 ikunimage参数：")
        print(f"   aspect_ratio: {result['ikunimage']['aspect_ratio']}")
        print(f"   size: {result['ikunimage']['size']}")
        print("=" * 50)
    
    return 0 if result['valid'] else 1


if __name__ == '__main__':
    import sys
    sys.exit(main())