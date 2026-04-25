---
name: ui-sprite-extractor
description: |
  智能识别UI图集并自适应切图工具。
  
  核心算法：
  1. 连通区域分析（Connected Component Labeling）- 找到所有非透明像素的连通块
  2. 边界框计算 - 每个连通块的最小包围矩形
  3. 智能合并 - 合并距离过近的区域（防止UI元素被错误拆分）
  4. 自适应切割 - 根据边界框裁剪并输出独立png
  
  适用于：AI生成的UI图集、游戏UI资源提取、任意排列的sprite sheet
  
  触发条件：
  (1) 用户说 "切图"、"切割UI"、"提取sprite"、"split sprites"
  (2) 用户说 "UI图集切图"、"提取UI元素"
  (3) 用户需要从一张图集里抠出各个独立UI元素
  
  注意：去背景功能请使用 ui-image-processor skill
---

# ui-sprite-extractor - 智能UI图集切图工具

从一张UI图集里自动识别并提取每个独立的UI元素，输出为单独的png文件。

---

## 核心算法

```
输入: UI图集（png，带透明通道）
     ↓
第1步: 连通区域分析
├── 使用 Union-Find 算法
├── 找到所有非透明像素的连通块
└── 每个连通块 = 一个潜在UI元素
     ↓
第2步: 过滤噪点
├── 计算每个连通块的面积
└── 移除面积 < min_area 的区域
     ↓
第3步: 智能合并
├── 检测距离过近的区域
├── 合并阈值 gap 像素内的区域
└── 防止UI元素被错误拆分
     ↓
第4步: 自适应切割
├── 计算每个区域的边界框
├── 添加 padding 边距
└── 裁剪并保存为独立png
     ↓
输出: sprite_001.png, sprite_002.png, ...
```

---

## 快速使用

### 基础用法

```bash
~/.hermes/.venv/bin/python ~/.hermes/skills/ui-sprite-extractor/scripts/sprite_extractor.py \
  --input /path/to/ui_atlas.png \
  --output-dir ./sprites/
```

### 调整参数

```bash
# 过滤小噪点（默认50像素）
python sprite_extractor.py -i atlas.png -o ./sprites/ --min-area 100

# 合并距离更近的区域（默认3像素）
python sprite_extractor.py -i atlas.png -o ./sprites/ --gap 10

# 增加切割边距（默认2像素）
python sprite_extractor.py -i atlas.png -o ./sprites/ --padding 5

# 自定义文件名前缀
python sprite_extractor.py -i atlas.png -o ./sprites/ --prefix "button"
```

### 完整参数示例

```bash
python sprite_extractor.py \
  -i ui_atlas.png \
  -o ./extracted_ui/ \
  --min-area 100 \
  --gap 5 \
  --padding 4 \
  --min-alpha 20 \
  --prefix "ui" \
  -q
```

---

## 参数速查

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `-i` / `--input` | 必需 | 输入图片路径 |
| `-o` / `--output-dir` | 必需 | 输出目录 |
| `--min-area` | 50 | 最小面积阈值，过滤噪点（像素数） |
| `--gap` | 3 | 合并阈值，合并距离过近的区域（像素） |
| `--padding` | 2 | 切割边界填充（像素） |
| `--min-alpha` | 10 | 最小透明度阈值（0-255） |
| `--prefix` | sprite | 输出文件名前缀 |
| `-q` / `--quiet` | - | 安静模式 |

---

## 使用场景

### 场景1：AI生成的UI图集

AI生成的UI图集通常包含多个独立UI元素，排列不一定整齐：

```bash
# 先去背景（如果需要）
python ~/.hermes/skills/ui-image-processor/scripts/ui_background_remover.py \
  -i raw_atlas.png -o clean_atlas.png

# 再切图
python ~/.hermes/skills/ui-sprite-extractor/scripts/sprite_extractor.py \
  -i clean_atlas.png -o ./ui_sprites/
```

### 场景2：游戏资源提取

从现有的sprite sheet提取独立元素：

```bash
python sprite_extractor.py \
  -i game_ui.png \
  -o ./game_sprites/ \
  --min-area 200 \
  --gap 5 \
  --prefix "game_ui"
```

### 场景3：精细调整

```bash
# UI元素间距很小，需要更小的gap
python sprite_extractor.py -i atlas.png -o ./sprites/ --gap 1

# 有很多小噪点，需要更大的min-area
python sprite_extractor.py -i atlas.png -o ./sprites/ --min-area 200

# 需要更大的切割边距
python sprite_extractor.py -i atlas.png -o ./sprites/ --padding 10
```

---

## 算法细节

### 连通区域分析

使用 **Union-Find（并查集）** 算法，时间复杂度接近 O(n)，其中 n 是图片像素数。

```
1. 遍历每个非透明像素
2. 检查右边和下边的邻居
3. 如果邻居也是非透明，合并到同一个连通块
4. 最终得到所有独立的连通区域
```

### 智能合并

某些UI元素可能由多个不相连的部分组成（如阴影、特效），需要合并：

```
1. 按面积排序，优先保留大区域
2. 检查每个区域是否与其他区域距离 < gap
3. 如果距离够近，合并边界框
4. 递归直到没有可合并的区域
```

---

## 依赖

- Python 3.8+
- Pillow（PIL）

```bash
~/.hermes/.venv/bin/pip install Pillow
```

---

## 与 ui-image-processor 配合使用

| Skill | 功能 | 使用时机 |
|-------|------|----------|
| **ui-image-processor** | 去背景 | 先处理白底和毛边 |
| **ui-sprite-extractor** | 切图 | 再提取独立UI元素 |

**典型工作流：**

```
原始UI图集.png
    ↓
[ui-image-processor] 去背景
    ↓
透明背景UI图集.png
    ↓
[ui-sprite-extractor] 切图
    ↓
sprite_001.png, sprite_002.png, ...
```