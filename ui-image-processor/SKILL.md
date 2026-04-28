---
name: ui-image-processor
description: |
  UI图片去背景工具 - 专门处理AI生成的UI图集白色背景和毛边问题。
  
  核心算法（已验证完美效果）：
  1. 洪水填充 - 从图片边缘删除白色背景，保留UI内部白色
  2. 15轮激进腐蚀 - 亮度阈值220→80递减，把毛边压到最小
  3. 颜色融合 - 残留像素染色融入相邻UI颜色
  
  专门解决：AI生成深蓝主题导致的"偏蓝白"毛边问题
  
  触发条件：
  (1) 用户说 "去背景"、"去白底"、"透明背景"、"remove background"
  (2) 用户提到白色毛边问题、毛边清理
  (3) 用户需要处理UI图集的背景问题
  
  注意：切图功能已移至 ui-sprite-extractor skill
---

# ui-image-processor - UI图片去背景工具

专门处理AI生成的UI图集，完美解决白色毛边问题。

---

## 适用场景

| 生成方案 | 是否需要此工具 | 说明 |
|---------|---------------|------|
| **NanoBanana2 白底** | ✓ 需要 | AI输出白色背景，需去背景处理 |
| **gpt-image-2 透明直出** | ✗ 可跳过 | AI直接输出透明PNG，无需去背景 |

**gpt-image-2 透明背景直出**时，可跳过此步骤，直接使用 `ui-sprite-extractor` 切图。

---

## 核心算法原理

### 问题：AI生成的毛边

AI生成UI图集时，主题颜色会混入边缘：
- 深蓝主题 → 偏蓝白毛边（RGB≈(239,242,255)，B通道最大）
- 导致边缘出现"稀碎的白毛边"

### 解决方案：三步流程

```
第1步：洪水填充
├── 从图片四边开始，删除与边缘相连的白色
└── 保留UI内部白色（被边框包围）

第2步：15轮激进腐蚀
├── 亮度阈值 220→80 递减
├── 透明邻居越多 → 阈值越低（更激进）
└── 把毛边压到最小（只剩极少量残留）

第3步：颜色融合
├── 残留像素搜索相邻UI颜色
├── 90% UI颜色 + 10% 原色 → 染色融合
└── 边缘干净平滑
```

---

## 快速使用

### 基础用法

```bash
~/.hermes/.venv/bin/python ~/.hermes/skills/ui-image-processor/scripts/ui_background_remover.py \
  --input /path/to/ui_atlas.png \
  --output /path/to/ui_atlas_clean.png
```

### 参数调整

```bash
# 更激进的腐蚀（处理顽固毛边）
python ui_background_remover.py -i input.png -o output.png --erosion 20

# 调整融合强度
python ui_background_remover.py -i input.png -o output.png --blend 0.95

# 安静模式
python ui_background_remover.py -i input.png -o output.png --quiet
```

---

## 参数速查

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--input` / `-i` | 必需 | 输入图片路径 |
| `--output` / `-o` | 必需 | 输出图片路径 |
| `--threshold` / `-t` | 250 | 洪水填充白色阈值 |
| `--erosion` / `-e` | 15 | 腐蚀轮数（越多越干净） |
| `--blend` / `-b` | 0.9 | 融合强度（越高越接近UI色） |
| `--quiet` / `-q` | - | 安静模式 |

---

## 依赖

- Python 3.8+
- Pillow（PIL）

```bash
~/.hermes/.venv/bin/pip install Pillow
```

---

## 实测效果

| 步骤 | 清理数量 |
|------|----------|
| 洪水填充 | 472,647 个背景像素 |
| 腐蚀15轮 | 29,172 个毛边像素 |
| 颜色融合 | 43 个残留像素染色 |

**最终效果：边缘干净平滑，无毛边残留**