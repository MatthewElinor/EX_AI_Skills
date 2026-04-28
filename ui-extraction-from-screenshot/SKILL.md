---
name: ui-extraction-from-screenshot
description: |
  从游戏效果图中提取UI素材的完整流水线。AI识别 → 用户选择 → AI提取 → 去背景 → 切图 → 相似度去重 → 输出独立PNG文件。
  
  核心功能：
  1. AI自动识别效果图中的UI元素（面板、控件、装饰等）
  2. 用户选择要提取的范围
  3. AI图生图提取UI素材
  4. 白色背景去除
  5. 智能切图
  6. 相似UI元素去重
  
  触发条件：
  (1) 用户说 "从效果图提取UI"、"扒UI"、"提取UI素材"
  (2) 用户提供效果图并要求提取其中的UI元素
  (3) 用户说 "UI素材提取"、"游戏UI扒取"
  (4) 用户想从AI生成的效果图获取可用的UI模板
version: 2.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [UI, prompt-engineering, extraction, game-development, pipeline]
    related_skills: [ikunimage, ui-image-processor, ui-sprite-extractor]
    category: creative
---

# ui-extraction-from-screenshot - UI素材提取完整流水线

从游戏效果图中提取UI素材，自动识别、处理并输出独立PNG文件。

---

## 完整工作流

```
游戏效果图.png
        ↓
[Step 0] AI识别UI元素（vision分析）
        ↓
[Step 0] 列出UI元素，用户选择范围
        ↓
[Step 0.5] 选择提取方案（A: NanoBanana2+去背景 / B: gpt-image-2透明直出）
        ↓
┌───────────────────────────────────────────────────────────────┐
│ 方案A: [Step 1] AI提取 → [Step 2] 去背景 → [Step 3] 切图      │
│ 方案B: [Step 1] AI提取(透明) → [Step 3] 切图（跳过去背景）    │
└───────────────────────────────────────────────────────────────┘
        ↓
[Step 4] 相似度去重（ui_similarity_dedup.py）
        ↓
    最终输出文件夹：unique UI elements
```

**方案对比：**

| 方案 | 模型 | 背景 | 步骤数 | 优势 | 适用场景 |
|------|------|------|--------|------|---------|
| **A（推荐）** | NanoBanana2 | 白色 | 5步 | 稳定可靠 | 首次提取、重要UI |
| **B（省步骤）** | gpt-image-2 | 透明 | 4步（跳过去背景） | 省时省钱 | 批量提取、熟练使用 |

---

## Step 0: UI元素识别与选择

**在提取前，先分析效果图，询问用户要提取哪些UI元素。**

### 执行流程

1. **用户提供效果图路径**
2. **Agent 用 vision_analyze 分析效果图**
3. **Agent 列出识别到的UI元素（分类展示）**
4. **用户选择要提取的范围**
5. **根据选择定制提取Prompt**

### Vision 分析命令

```bash
# 使用 vision_analyze 工具
# 问题："识别这张游戏效果图中所有的UI元素，按类型分类列出：面板类、控件类、装饰类。每项包含：名称、位置、简要描述"
```

### 询问用户模板

```
我识别到效果图中有以下UI元素：

【面板类】
  1. 卡牌信息面板（左下角）- 红黑边框，切角设计，含LAP TIME区域
  2. 排名显示框（左上角）- 星芒装饰边框
  3. 小地图/雷达框（右下角）- 几何边框，圆形显示区

【控件类】
  4. 速度表盘（右上角）- 圆形仪表盘，刻度线
  5. 主按钮（底部）- 圆角矩形，可能含文字
  6. 辅助按钮组（右下）- 小型功能按钮

【装饰类】
  7. 星芒火花（多处）- 锐角星形装饰，红白配色
  8. 斜线条（边缘）- 动感线条，斜切设计
  9. 分隔线（面板内）- 红色细线分隔条
  10. 边框装饰（各面板）- 锯齿/切角边框元素

请选择要提取的UI元素：
• 输入序号（如 "1,2,3,7,8" 只提取面板和星芒装饰）
• 输入类别名（如 "面板类" 提取所有面板）
• 输入 "全部" 提取所有元素
• 输入 "排除:序号" 提取除某元素外的全部（如 "排除:5,6" 不提取按钮）
```

### 根据选择定制 Prompt

| 用户选择 | Prompt定制策略 |
|---------|---------------|
| **全部** | 使用标准方案A prompt |
| **部分元素** | 在prompt中明确列出要提取的元素名称 |
| **按类别** | 添加类别限定（如"只提取面板类UI元素"） |
| **排除模式** | 明确说明"不要提取XX元素" |

---

## Step 1: AI提取UI图集

使用 ikunimage 图生图，从效果图中提取UI元素。支持两种方案。

### Step 0.5: 选择提取方案

询问用户：
> "请选择提取方案："
> - **方案A（推荐）**：NanoBanana2 + 后续去背景（稳定可靠，¥0.125/次）
> - **方案B（省步骤）**：gpt-image-2 透明背景直出（省去去背景步骤，¥0.06/次，可能不稳定）

### 最佳Prompt（方案A：白色背景提取）

**全部提取**：
```
从这张游戏界面效果图中提取所有UI素材元素。

提取要求：
- 把图中所有UI面板、按钮、框体、装饰元素都单独分离出来
- 去除所有文字和数字，保留空白框体
- 去除背景中的赛车、场景等非UI内容
- 所有UI元素水平排列在白色背景上，按游戏UI图集的标准格式输出

输出：2048x2048像素的UI素材图集，白色背景
```

**部分提取示例**（只提取面板和装饰）：
```
从这张游戏界面效果图中提取以下UI素材元素：卡牌信息面板、排名显示框、小地图框、星芒火花、斜线条装饰。

提取要求：
- 把指定的UI元素单独分离出来
- 去除所有文字和数字，保留空白框体
- 去除背景内容和未选中的UI元素
- 所有提取的元素水平排列在白色背景上

输出：2048x2048像素的UI素材图集，白色背景
```

### 最佳Prompt（方案B：透明背景提取）

**注意**：方案B无需添加 "white background"，使用 `--transparent` 参数自动注入透明背景提示词。

**全部提取**（透明背景）：
```
从这张游戏界面效果图中提取所有UI素材元素。

提取要求：
- 把图中所有UI面板、按钮、框体、装饰元素都单独分离出来
- 去除所有文字和数字，保留空白框体
- 去除背景中的赛车、场景等非UI内容
- 所有UI元素水平排列在图集上，按游戏UI图集的标准格式输出

输出：2048x2048像素的UI素材图集
```

### 执行命令

**方案A（NanoBanana2 白底）**：
```bash
mkdir -p ./outimage/ikunimage/

~/.hermes/.venv/bin/python ~/.hermes/skills/ikunimage/scripts/generate_ikun_edit.py \
  --input /path/to/screenshot.png \
  --prompt "提取prompt内容..." \
  --output ./outimage/ikunimage/ui_atlas_{timestamp}.png \
  --retry 3
```

**方案B（gpt-image-2 透明背景）**：
```bash
~/.hermes/.venv/bin/python ~/.hermes/skills/ikunimage/scripts/generate_ikun_edit.py \
  --model gpt-image-2 --transparent \
  --input /path/to/screenshot.png \
  --prompt "提取prompt内容（无需 white background）..." \
  --output ./outimage/ikunimage/ui_atlas_{timestamp}.png \
  --retry 10
```

---

## Step 2: 去背景（仅方案A需要）

**方案B（透明背景直出）跳过此步骤，直接进入 Step 3 切图。**

去除AI生成的白色背景和毛边。

### 适用场景

| 方案 | 是否需要去背景 | 输入 |
|------|---------------|------|
| **A** | ✓ 需要 | 白色背景图集 |
| **B** | ✗ 跳过 | 直接用透明背景图集切图 |

### 执行命令

```bash
~/.hermes/.venv/bin/python ~/.hermes/skills/ui-image-processor/scripts/ui_background_remover.py \
  --input ./outimage/ikunimage/ui_atlas.png \
  --output ./outimage/ikunimage/ui_atlas_clean.png \
  --threshold 250 --erosion 15 --blend 0.9
```

### 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--threshold` | 250 | 白色阈值，越高越严格（240-255） |
| `--erosion` | 15 | 腐蚀轮数，越多越干净（10-25） |
| `--blend` | 0.9 | 边缘融合强度（0.8-0.95） |

---

## Step 3: 智能切图

将图集切分为独立的UI元素。

### 输入区分

| 方案 | 输入文件 | 说明 |
|------|---------|------|
| **A** | `ui_atlas_clean.png`（去背景后的图集） | 需先完成 Step 2 去背景 |
| **B** | `ui_atlas.png`（原始透明背景图集） | 直接切图，无需去背景 |

### 执行命令

**方案A（去背景后切图）**：
```bash
~/.hermes/.venv/bin/python ~/.hermes/skills/ui-sprite-extractor/scripts/sprite_extractor.py \
  --input ./outimage/ikunimage/ui_atlas_clean.png \
  --output-dir ./outimage/ikunimage/sprites/ \
  --min-area 500 --gap 30 --padding 4 \
  --prefix "ui"
```

**方案B（透明图集直接切图）**：
```bash
~/.hermes/.venv/bin/python ~/.hermes/skills/ui-sprite-extractor/scripts/sprite_extractor.py \
  --input ./outimage/ikunimage/ui_atlas.png \
  --output-dir ./outimage/ikunimage/sprites/ \
  --min-area 500 --gap 30 --padding 4 \
  --prefix "ui"
```

### 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--min-area` | 500 | 最小面积阈值，过滤噪点 |
| `--gap` | 30 | 合并阈值，防止元素被错误拆分 |
| `--padding` | 4 | 切割边界填充（像素） |
| `--prefix` | sprite | 输出文件名前缀 |

---

## Step 4: 相似度去重

**核心功能：检测并合并样式相似的UI元素**

AI提取的UI图集常有重复：
- 同一个按钮提取出多个相似版本
- 同一个面板被多次识别
- 样式几乎相同的装饰元素

### 算法原理

```
1. 感知哈希（Perceptual Hash）
   └─ 每张图片生成256位哈希，相似图片有相似哈希
   
2. 汉明距离比较
   └─ 计算哈希差异位数，差异 ≤ 阈值 = 相似
   
3. 质量评分选择
   └─ 分辨率 + 文件大小，保留质量最好的版本
```

### 执行命令

```bash
~/.hermes/.venv/bin/python ~/.hermes/skills/creative/ui-extraction-from-screenshot/scripts/ui_similarity_dedup.py \
  --input-dir ./outimage/ikunimage/sprites/ \
  --output-dir ./outimage/ikunimage/final_ui/
```

### 参数调整

```bash
# 严格去重（只合并高度相似的）
--threshold 5

# 宽松去重（合并更多相似元素）
--threshold 15

# 更精确的哈希（大尺寸图片）
--hash-size 24

# 移动模式（不保留原文件）
--move
```

### 参数速查表

| 参数 | 默认值 | 说明 | 推荐范围 |
|------|--------|------|----------|
| `--threshold` | 10 | 汉明距离阈值（约4%差异） | 5-8严格，10-15平衡，20+宽松 |
| `--hash-size` | 16 | 哈希尺寸 | 8快速，16平衡，24精确 |
| `--move` | 复制模式 | 是否移动原文件 | 默认复制，加--move则移动 |

### 输出结构

```
final_ui/
├── ui_001.png          # 唯一UI元素
├── ui_003.png          # 唯一UI元素
├── ui_007.png          # 唯一UI元素
└── _duplicates/        # 重复元素文件夹
    ├── ui_002.png      # 与ui_001相似，已过滤
    ├── ui_004.png      # 与ui_003相似，已过滤
    └── ui_005.png
```

---

## 一键完整流程脚本

```bash
#!/bin/bash
# ui_extraction_pipeline.sh

SCREENSHOT="$1"
FINAL_DIR="$2"
WORK_DIR="./outimage/ikunimage/ui_work_$(date +%Y%m%d_%H%M%S)"

mkdir -p "$WORK_DIR"

echo "=== Step 1: AI提取 ==="
~/.hermes/.venv/bin/python ~/.hermes/skills/ikunimage/scripts/generate_ikun_edit.py \
  --input "$SCREENSHOT" \
  --prompt "从这张游戏界面效果图中提取所有UI素材元素。提取要求：- 把图中所有UI面板、按钮、框体、装饰元素都单独分离出来 - 去除所有文字和数字，保留空白框体 - 去除背景中的赛车、场景等非UI内容 - 所有UI元素水平排列在白色背景上，按游戏UI图集的标准格式输出 输出：2048x2048像素的UI素材图集，白色背景" \
  --output "$WORK_DIR/ui_atlas.png" \
  --retry 3

echo "=== Step 2: 去背景 ==="
~/.hermes/.venv/bin/python ~/.hermes/skills/ui-image-processor/scripts/ui_background_remover.py \
  --input "$WORK_DIR/ui_atlas.png" \
  --output "$WORK_DIR/ui_atlas_clean.png"

echo "=== Step 3: 切图 ==="
~/.hermes/.venv/bin/python ~/.hermes/skills/ui-sprite-extractor/scripts/sprite_extractor.py \
  --input "$WORK_DIR/ui_atlas_clean.png" \
  --output-dir "$WORK_DIR/sprites/" \
  --min-area 500 --gap 30 --padding 4 \
  --prefix "ui"

echo "=== Step 4: 去重 ==="
~/.hermes/.venv/bin/python ~/.hermes/skills/creative/ui-extraction-from-screenshot/scripts/ui_similarity_dedup.py \
  --input-dir "$WORK_DIR/sprites/" \
  --output-dir "$FINAL_DIR/"

echo "✅ 完成！最终UI素材: $FINAL_DIR"
ls -la "$FINAL_DIR"
```

---

## Verification Steps（验证检查）

提取完成后检查：

| 检查项 | 验证方法 | 合格标准 |
|--------|----------|----------|
| **图集尺寸** | `identify ui_atlas.png` | 1024-2048范围内 |
| **去背景效果** | 打开ui_atlas_clean.png检查 | 边缘干净，无白边残留 |
| **切图数量** | `ls sprites/ | wc -l` | 与预期数量接近（AI随机性允许偏差） |
| **元素尺寸** | 检查几个切出的png | 在合理范围内（允许超出预期20%） |
| **去重效果** | 检查_duplicates文件夹 | 无误判（必要元素未被误删） |
| **文字去除** | 打开几个最终png检查 | 无残留文字/数字 |

---

## Pitfalls（常见问题与解决方案）

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| **提取的元素尺寸不一致** | AI生图随机性 | 正常现象，后续切图去重会处理 |
| **提取出的UI重复太多** | AI多次识别同一元素 | 调高 `--threshold` 到15-20 |
| **相似UI被错误合并** | 去重阈值过宽 | 调低 `--threshold` 到5-8 |
| **切图数量过多** | 噪点过多 | 增加 `--min-area` 到1000+ |
| **元素粘连无法切分** | AI排列间距不足 | 加大 `--gap` 到40+ |
| **白色背景未完全去除** | 阈值设置不当 | 调高 `--threshold` 到255 |
| **毛边残留** | 腐蚀轮数不足 | 增加 `--erosion` 到20-25 |
| **UI内部白色被误删** | 洪水填充参数不当 | 调低 `--threshold` 到245 |

---

## 常见陷阱与设计矛盾

### 陷阱1：AI"重新绘制"而非"提取"

**问题描述**：模型可能不理解"提取"概念，而是重新生成类似风格的UI，导致与原图风格偏差。

**解决方案**：
- 在prompt中强调"从这张图提取"而非"生成"
- 明确列出要提取的元素名称和位置
- 使用方案A prompt（已验证最佳）

### 陷阱2：复杂效果图提取不完整

**问题描述**：效果图过于复杂（大量特效、遮挡），AI难以完整识别所有UI元素。

**解决方案**：
- Step 0 识别阶段详细分析，确保用户了解有哪些元素
- 复杂图可分多次提取（先提取主要面板，再提取装饰）
- 无法提取的元素可用 ui-resource-generator 单独生成

### 陷阱3：去重阈值设置不当

**问题描述**：阈值太高导致不同样式被误合并，阈值太低导致相同样式未合并。

**解决方案**：
- 默认 threshold=10 是平衡值
- 先用默认值测试，检查 _duplicates 文件夹
- 如有误判：调低阈值
- 如去重不足：调高阈值

### 陷阱4：输出文件命名混乱

**问题描述**：多次提取后文件名冲突，难以管理。

**解决方案**：
- 使用时间戳命名工作目录
- Step 0 阶段记录提取内容，生成命名规则
- 最终输出按UI类型重命名（如 panel_card.png, decor_star.png）

---

## 实验结论

**方案A（直接提取型）效果最佳**

| 要素 | 为什么有效 |
|------|-----------|
| **"提取"概念** | 比"生成"、"参照"更准确传达任务意图 |
| **去文字明确** | "去除所有文字和数字，保留空白框体"具体清晰 |
| **去背景明确** | "去除背景中的赛车、场景等非UI内容" |
| **图集格式强调** | "按游戏UI图集的标准格式输出"让模型理解行业规范 |

实验日期：2026-04-26
测试模型：NanoBanana2 (gemini-3.1-flash-image-preview)

---

## 依赖技能与脚本

| 技能/脚本 | 功能 | 路径 |
|----------|------|------|
| **ikunimage** | AI图生图 | `~/.hermes/skills/ikunimage/` |
| **ui-image-processor** | 去背景 | `~/.hermes/skills/ui-image-processor/` |
| **ui-sprite-extractor** | 智能切图 | `~/.hermes/skills/ui-sprite-extractor/` |
| **ui_similarity_dedup.py** | 相似度去重 | `scripts/ui_similarity_dedup.py` |

---

## 参数总速查表

### Step 1 (ikunimage)

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--input` | 必填 | 效果图路径 |
| `--prompt` | 必填 | 提取prompt |
| `--output` | 必填 | 输出图集路径 |
| `--retry` | 3 | 重试次数 |

### Step 2 (去背景)

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--threshold` | 250 | 白色阈值 |
| `--erosion` | 15 | 腐蚀轮数 |
| `--blend` | 0.9 | 融合强度 |

### Step 3 (切图)

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--min-area` | 500 | 最小面积 |
| `--gap` | 30 | 合并阈值 |
| `--padding` | 4 | 边界填充 |
| `--prefix` | sprite | 文件名前缀 |

### Step 4 (去重)

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--threshold` | 10 | 汉明距离阈值 |
| `--hash-size` | 16 | 哈希尺寸 |
| `--move` | 复制 | 文件处理模式 |