---
name: ui-resource-generator
description: |
  AI批量生产UI美术资源图的完整流水线。一键生成、去背景、切图。
  
  集成：ikunimage（生图）+ ui-image-processor（去背景）+ ui-sprite-extractor（切图）
  
  触发：用户说 "生成UI资源"、"批量生成UI"、"生产UI图集"、"AI生成UI"
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [ui, game-dev, asset-generation, ikunimage, pipeline]
    related_skills: [ikunimage, ui-image-processor, ui-sprite-extractor]
    category: creative
---

# ui-resource-generator - AI批量UI资源生产流水线

一键生成游戏/应用UI素材：AI生图 → 去背景 → 智能切图 → 输出独立PNG

---

## 快速工作流

```
用户输入: 数量 + 尺寸 + 风格
    ↓
模型选择: 方案A（NanoBanana2+去背景）/ 方案B（gpt-image-2透明直出）
    ↓
布局计算: 行列数 + ikunimage参数
    ↓
┌─────────────────────────────────────────────────────┐
│ 方案A: ikunimage生成白色背景图集 → 去背景 → 切图    │
│ 方案B: ikunimage生成透明背景图集 → 直接切图         │
└─────────────────────────────────────────────────────┘
    ↓
输出: N个独立UI PNG文件
```

**方案对比总结：**

| 方案 | 步骤数 | 优势 | 适用场景 |
|------|--------|------|---------|
| **A** | 4步（生图→去背景→切图） | 稳定可靠 | 重要UI、首次尝试 |
| **B** | 3步（生图→切图） | 省时省钱 | 批量生成、熟练使用 |

---

## 执行步骤

### Step 1: 询问数量

直接询问用户：
> "请选择要生成的UI资源数量（建议多生成几个方便筛选）："
> - 10个小型UI（按钮/图标）
> - 5个中型UI（窗口框/标题栏）
> - 3个大型UI（对话框/卡牌）
> - 自定义数量

### Step 2: 询问尺寸（重要！）

**必须明确：宽 × 高（先宽后高）**

> "单个UI元素尺寸？（宽×高，最大1024×1024）："
> - 小型：宽100×高30（按钮）
> - 中型：宽200×高100（窗口框）
> - 大型：宽300×高200（对话框）
> - 自定义（请明确：宽×高）

**常见尺寸参考：**
- 按钮：宽大高小（如 120×30、150×50）
- 卡牌：高大宽小（如 150×250、200×300）
- 窗口框：接近方形（如 200×150）

### Step 3: 计算布局

```bash
~/.hermes/.venv/bin/python ~/.hermes/skills/creative/ui-resource-generator/scripts/atlas_layout_calculator.py \
  --count {数量} --width {宽} --height {高} --json
```

输出包含：
- `cols/rows`: 排列行列数
- `ikunimage.aspect_ratio/size`: 生图参数
- `actual_count`: 实际可容纳数量（可能被调整）

**默认间距30像素**，提高AI生图尺寸不确定性的容错。

### Step 4: 选择生成方案（重要决策）

询问用户选择生成方案：

> "请选择生成方案："
> - **方案A（推荐）**：NanoBanana2 + 后续去背景（稳定可靠，¥0.125/次）
> - **方案B（省步骤）**：gpt-image-2 透明背景直出（省去去背景步骤，¥0.06/次，可能不稳定）

**方案对比：**

| 方案 | 模型 | 背景 | 流程 | 价格 | 稳定性 |
|------|------|------|------|------|--------|
| **A（推荐）** | NanoBanana2 | 白色 | 生图→去背景→切图 | ¥0.125/次 | ✓ 稳定 |
| **B（省步骤）** | gpt-image-2 | 透明 | 生图→切图（跳过去背景） | ¥0.06/次 | ⚠ 可能不稳定，需更多重试 |

**方案B优势**：
- 省去 `ui-image-processor` 去背景步骤，直接进入切图
- gpt-image-2 价格便宜一半
- 适合批量生成UI资源

**方案B注意事项**：
- gpt-image-2 可能不稳定，建议使用 `--retry 10`
- 如失败率高可切换到方案A

### Step 5: 询问UI类型和风格

询问：
- **UI类型**：按钮、窗口框、卡牌、装饰元素、综合
- **美术风格**：P5风格、赛博朋克、扁平化、游戏卡通、图生图（提供参考图）

### Step 6: 头脑风暴细化

根据UI类型追问细节：

| UI类型 | 细化问题 |
|--------|----------|
| 按钮 | 形状（圆角/尖角/胶囊）？用途？立体感？ |
| 窗口框 | 标题栏？九宫格边框宽度？分隔线？ |
| 卡牌 | 头像区域？属性区域？正面/背面？ |

### Step 7: 构建提示词并生成

**根据选择的方案构建提示词：**

**方案A（白色背景）提示词模板：**
```
Game UI atlas sheet, {count} UI elements arranged in {cols} columns and {rows} rows,
each element approximately {width}x{height} pixels,
white background,
{ui_types},
{style_description},
elements evenly spaced with clear separation,
no text, no labels, pure UI elements only
```

**方案B（透明背景）提示词模板：**
```
Game UI atlas sheet, {count} UI elements arranged in {cols} columns and {rows} rows,
each element approximately {width}x{height} pixels,
{ui_types},
{style_description},
elements evenly spaced with clear separation,
no text, no labels, pure UI elements only
```

> **注意**：方案B使用 `--transparent` 参数，脚本会自动注入透明背景提示词，无需手动添加 "white background"

**方案A（NanoBanana2 白底）生成命令：**
```bash
~/.hermes/.venv/bin/python ~/.hermes/skills/ikunimage/scripts/generate_ikun.py \
  --prompt "{提示词}" \
  --aspect-ratio {aspect_ratio} \
  --size {size} \
  --output /home/agentuser/outimage/ikunimage/ui_atlas_{timestamp}.png
```

**方案B（gpt-image-2 透明背景）生成命令：**
```bash
~/.hermes/.venv/bin/python ~/.hermes/skills/ikunimage/scripts/generate_ikun.py \
  --model gpt-image-2 --transparent \
  --retry 10 \
  --prompt "{提示词}" \
  --aspect-ratio {aspect_ratio} \
  --size {size} \
  --output /home/agentuser/outimage/ikunimage/ui_atlas_{timestamp}.png
```

### Step 8: 去背景（仅方案A）

**方案B跳过此步骤，直接进入切图。**

```bash
~/.hermes/.venv/bin/python ~/.hermes/skills/ui-image-processor/scripts/ui_background_remover.py \
  --input {生成的图集} \
  --output {图集}_clean.png \
  --threshold 250 --erosion 15 --blend 0.9
```

### Step 9: 智能切图

**方案A 输入：去背景后的图集**
**方案B 输入：原始生成的透明背景图集（直接切图）**

```bash
~/.hermes/.venv/bin/python ~/.hermes/skills/ui-sprite-extractor/scripts/sprite_extractor.py \
  --input {去背景后的图集或原始透明图集} \
  --output-dir {输出目录}/ \
  --min-area 500 --gap 30 --padding 4 \
  --prefix "ui"
```

### Step 10: 展示结果

- 显示输出目录路径
- 展示几个切出的UI元素（MEDIA:路径）
- 列出所有生成的文件

---

## Pitfalls（常见问题）

| 问题 | 解决方案 |
|------|----------|
| **AI生成的元素尺寸超出预期** | 默认间距30像素已提高容错，必要时可手动调大 |
| **元素粘连无法切分** | 加大 `--gap` 参数，或在提示词中强调 "well separated" |
| **白色背景未完全去除** | 检查提示词是否包含 "white background"，调高 `--threshold` |
| **毛边残留** | 增加 `--erosion` 轮数（如20轮） |
| **尺寸搞反了** | 坚持问"宽×高"，按钮是"宽大高小" |
| **切图数量不对** | AI生图随机性导致，调整 `--min-area` 过滤噪点 |
| **ikunimage超时** | 2K图约30-60秒，超时可重试 |

---

## Verification Steps

生成完成后检查：

1. **图集尺寸**：是否符合ikunimage输出范围（1024-2048）
2. **去背景效果**：检查边缘是否干净，无残留白边
3. **切图数量**：与预期数量是否接近（AI随机性允许偏差）
4. **单个元素尺寸**：是否在合理范围内（允许超出预期20%）

---

## 参数速查

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `spacing` | 30 | UI元素间距（像素） |
| `min_area` | 500 | 切图最小面积阈值 |
| `gap` | 30 | 切图合并阈值 |
| `padding` | 4 | 切图边界填充 |
| `threshold` | 250 | 去背景白色阈值 |
| `erosion` | 15 | 毛边腐蚀轮数 |
| `blend` | 0.9 | 边缘融合强度 |

---

## 布局计算快速参考

| UI尺寸 | 10个 | 20个 | 50个 |
|--------|------|------|------|
| 100×30 | 1536×1024 | 1536×1024 | 2048×2048 |
| 120×30 | 1536×1024 | 1536×1024 | 2048×2048 |
| 200×100 | 1536×1024 | 2048×2048 | 超限→54个 |
| 300×200 | 2048×2048 | 超限→54个 | 超限→54个 |

---

## 依赖技能

- **ikunimage**: AI生图（NanoBanana2 或 gpt-image-2）
  - NanoBanana2：稳定，白色背景，需后续去背景
  - gpt-image-2：便宜，支持透明背景直出，可跳过去背景步骤
- **ui-image-processor**: 去背景（洪水填充+腐蚀+融合）—— 仅方案A需要
- **ui-sprite-extractor**: 智能切图（连通区域分析）