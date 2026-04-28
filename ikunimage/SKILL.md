---
name: ikunimage
description: |
  ikunimage - 双模型 AI 图片生成器（ikun 专用渠道）。通过 ikun API（api.ikuncode.cc）调用图像模型，支持两种模型可选：
  - NanoBanana2（gemini-3.1-flash-image-preview）：稳定可靠，¥0.125/次
  - GPT-Image-2（gpt-image-2）：价格便宜 ¥0.06/次，但可能不稳定需要多重试
  单渠道设计，用户只需配置一个 API Key 即可使用。支持 10 种宽高比、3 种分辨率（1K/2K/4K）、文字渲染、图生图编辑。
  使用 --model 参数切换模型，或在 setup 时选择默认模型。
  触发条件：
  (1) 用户说 /ikunimage 或要求使用 ikun 渠道生图
  (2) 用户说"ikun 生图"、"用 ikun 画"、"ikun 生成图片"
  (3) 用户说"生成图片"且明确指定使用 ikun
  (4) 用户说"高清生图"、"4K生图"且指定 ikun
  (5) 用户说"图片编辑"、"修改图片"、"图生图"且指定 ikun
  (6) 用户提供图片路径并要求使用 ikun 渠道进行修改
  (7) 用户说"ikun 批量生图"
  (8) 用户说"配置 ikun"、"ikun setup"
---

# ikunimage - 双模型 AI 图片生成器（ikun 渠道）

通过 ikun API 调用图像模型，支持两种模型可选：

## 模型对比

| 模型 | 名称 | 价格 | 稳定性 | 透明背景 | 重试默认 | 超时 | 适用场景 |
|------|------|------|--------|---------|---------|------|---------|
| **gemini-3.1-flash-image-preview** | NanoBanana2 | ¥0.125/次 | ✓ 稳定 | ✗ 不支持（白底） | 3次 | 6-10分钟 | 日常生图，稳定优先，需后续去背景 |
| **gpt-image-2** | GPT-Image-2 | ¥0.06/次 | ⚠ 可能不稳定 | ✓ **支持直出** | 10次 | 9-15分钟 | UI资源直出，省去去背景步骤，成本优先 |

**重要**：
- gpt-image-2 价格便宜一半，但中转站可能不稳定，建议使用 `--retry 10` 并耐心等待
- **gpt-image-2 支持透明背景直出**，生成可直接使用的 PNG UI 资源，省去后续去背景处理

## 透明背景功能（gpt-image-2 专属）

**适用场景**：生成可直接使用的 UI 资源（按钮、面板、卡牌底框等），省去后续 `ui-image-processor` 去背景步骤。

**使用方法**：
```bash
# 方式1：--transparent 简写
~/.hermes/.venv/bin/python ~/.hermes/skills/ikunimage/scripts/generate_ikun.py \
  --model gpt-image-2 --transparent \
  --prompt "游戏卡牌底框，红色边框，无文字" \
  --output ./card_frame.png

# 方式2：--bg transparent 完整写法
~/.hermes/.venv/bin/python ~/.hermes/skills/ikunimage/scripts/generate_ikun.py \
  --model gpt-image-2 --bg transparent \
  --prompt "游戏卡牌底框" --output ./card_frame.png

# 图生图编辑也可使用透明背景
~/.hermes/.venv/bin/python ~/.hermes/skills/ikunimage/scripts/generate_ikun_edit.py \
  --model gpt-image-2 --transparent \
  --input ./draft.png --prompt "修改颜色为蓝色" --output ./blue_frame.png
```

**透明背景提示词自动注入**：
使用 `--transparent` 时，脚本会自动在 prompt 后追加：
```
transparent background PNG, alpha channel, clean edges, ready-to-use UI asset, no background color
```

**NanoBanana2 限制**：
如果对 NanoBanana2 使用 `--transparent`，脚本会输出警告并自动回退到白色背景（添加 `white background` 提示词），生成后需使用 `ui-image-processor` 去背景。

## 全局风格约束（强制）

**所有生成的图片必须严格遵循中国风格**：

| 维度 | 强制要求 |
|------|---------|
| **人物** | 中国面孔、东方五官、黑色或深棕色头发（除非用户明确要求其他发色） |
| **服饰** | 中式服装为首选：汉服、旗袍、唐装、中山装、新中式、国潮。现代装也必须符合中国审美 |
| **场景** | 中国场景：江南水乡、古镇、故宫、竹林、茶室、胡同、现代中国都市、中国校园等 |
| **元素** | 中国文化元素：灯笼、折扇、油纸伞、毛笔、茶具、瓷器、梅兰竹菊、祥云、中国结等 |
| **建筑** | 中式建筑：飞檐翘角、白墙黛瓦、园林亭台、现代中国风建筑 |
| **色调** | 偏好中国传统色：朱红、靛蓝、月白、鹅黄、黛绿、藕粉、琥珀、墨色 |
| **文字** | 如需渲染文字，必须使用中文 |
| **氛围** | 融入东方美学意境：留白、含蓄、诗意、雅致 |

**提示词语言**：统一使用中文撰写提示词。

**例外**：当用户明确要求其他风格（如"Persona 5风格"、"赛博朋克风格"）时，按用户要求执行。

## 输出目录与命名规范

| 项目 | 值 |
|------|------|
| **输出目录** | `./outimage/ikunimage/` |
| **扩展名** | `.png` |

**文件命名规则**：`{YYYYMMDD}_{HHMM}_{主题简称}.png`

| 项目 | 规则 |
|------|------|
| **日期格式** | 当日日期，`YYYYMMDD`，如 `20260225` |
| **时间格式** | 当前时间的时分，24小时制，如 `1430` |
| **主题简称** | 从用户描述中提炼 2-6 个汉字，如 `古风仙侠`、`江南水乡` |
| **批量递增** | 同一批次多张同主题时追加序号：`..._主题_01.png`、`..._主题_02.png` |

**示例**：
```
./outimage/ikunimage/20260225_1430_古风仙侠.png
./outimage/ikunimage/20260225_1430_江南水乡_01.png
./outimage/ikunimage/20260225_1430_江南水乡_02.png
```

生成前必须先 `mkdir -p` 确保目录存在，然后将 `--output` 参数指向按规范命名的文件。

---

## 首次使用配置

ikunimage 需要用户提供 ikun 渠道的 API Key。

### 方式 1：交互式配置（推荐）

```bash
~/.hermes/.venv/bin/python ~/.hermes/skills/ikunimage/scripts/generate_ikun.py --setup
```

### 方式 2：手动创建配置文件

```bash
mkdir -p ~/.ikunimage
echo '{"api_key": "sk-你的key"}' > ~/.ikunimage/config.json
```

### 方式 3：环境变量

```bash
export IKUN_API_KEY="sk-你的key"
```

### API Key 加载优先级

1. `--api-key` CLI 参数（最高）
2. `IKUN_API_KEY` 环境变量
3. `~/.ikunimage/config.json` 中的 `api_key`
4. 均无 → 报错退出，提示运行 `--setup`

---

## 文生图工作流

### Step 1: 解析用户需求

从用户描述中提取：
- **prompt**：图片描述（如果太短则润色补充）
- **宽高比**：默认 `1:1`。映射用户意图："竖版" → `9:16`，"横版" → `16:9`，"超宽" → `21:9`
- **分辨率**：默认 `2K`。映射："快速预览" → `1K`，"超高清/4K" → `4K`
- **输出路径**：`./outimage/ikunimage/{YYYYMMDD}_{HHMM}_{主题简称}.png`

### Step 2: 构建提示词

**全部使用中文撰写**，结构：中国面孔主体 + 中式服饰 + 中国场景 + 东方美学风格 + 光影 + 构图 + 约束

提示词模板：
```
[主体]：一位中国年轻女性，东方精致五官，黑色/深棕色头发，[发型]
[服饰]：[中式服装：汉服/旗袍/新中式/国潮等]
[场景]：[中国场景：江南水乡/古镇/故宫/竹林/中国都市等]
[元素]：[中国文化元素：灯笼/折扇/油纸伞/茶具等]
[光影]：[具体光影描述]
[色调]：[中国传统色：朱红/靛蓝/月白/黛绿等]
[氛围]：[东方美学意境：诗意/雅致/含蓄/留白等]
[约束]：无水印，无多余文字，画面干净，构图完整
```

分辨率详情和提示词技巧参见 [references/api-reference.md](references/api-reference.md)。

### Step 3: 运行脚本

**使用默认模型（NanoBanana2）**：
```bash
~/.hermes/.venv/bin/python ~/.hermes/skills/ikunimage/scripts/generate_ikun.py \
  --prompt "描述内容" \
  --aspect-ratio 16:9 \
  --size 2K \
  --output ./outimage/ikunimage/YYYYMMDD_HHMM_主题简称.png \
  --retry 3
```

**使用 gpt-image-2（便宜但需多重试）**：
```bash
~/.hermes/.venv/bin/python ~/.hermes/skills/ikunimage/scripts/generate_ikun.py \
  --model gpt-image-2 \
  --prompt "描述内容" \
  --aspect-ratio 16:9 \
  --size 2K \
  --output ./outimage/ikunimage/YYYYMMDD_HHMM_主题简称.png \
  --retry 10
```

### Step 4: 展示结果

**生成成功输出格式**:

```
━━━ 图片 #N ━━━
引擎：ikunimage (NanoBanana2)
比例：[aspect_ratio] → [实际分辨率]
分辨率等级：[1K/2K/4K]

提示词：
[完整提示词]

文件：[保存路径]

调整建议：
- [可调方向]
━━━━━━━━━━━━
```

- 失败：显示错误信息，建议检查 API Key 或调整提示词

---

## 图生图 / 编辑工作流

上传本地图片 + 文字编辑描述，AI 理解原图内容后生成修改后的新图片。

### 支持的图片格式

JPG / JPEG / PNG / WebP / GIF，推荐图片大小 < 4MB。

### 编辑类型示例

| 编辑类型 | 提示词示例 |
|---------|-----------|
| **添加元素** | "在人物旁边添加一只白色的猫" |
| **修改背景** | "将背景改为日落时分的海滩，保持人物不变" |
| **风格转换** | "将这张照片转换为水彩画风格，保持原有构图" |
| **服饰更换** | "将人物的服装改为红色汉服" |
| **季节变换** | "将场景改为冬天下雪的景象" |
| **文字添加** | "在图片顶部添加中文标题「春日物语」" |

### Step 1: 确认输入

从用户输入中提取：
- **输入图片路径**：用户提供的本地图片路径
- **编辑描述**：用户想要的修改内容
- **宽高比**：默认 `1:1`，或根据原图推断

### Step 2: 构建编辑提示词

**提示词结构**：`模仿输入图的风格，[具体编辑描述]`

**重要经验**：图生图时**不要添加额外的美术风格描述**（如"赛博朋克、霓虹、深蓝色背景"等），AI 会自动从输入图中提取风格特征。添加额外风格描述反而可能导致风格偏离。

**正确示例**：
```
模仿输入图的风格，生成赛车游戏 LaunchWindow 主菜单界面效果图。中心显示游戏标题「公路之星」，下方有「新游戏」和「继续游戏」两个按钮
```

**错误示例**（风格描述过多）：
```
将界面改为 LaunchWindow 主菜单界面。保持赛博朋克霓虹风格不变，深蓝色背景+青色发光线条。中心显示游戏标题...（风格描述太多会导致偏离输入图风格）
```

### Step 3: 运行脚本

```bash
~/.hermes/.venv/bin/python ~/.hermes/skills/ikunimage/scripts/generate_ikun_edit.py \
  --input /path/to/original.jpg \
  --prompt "编辑描述" \
  --aspect-ratio 3:4 \
  --output ./outimage/ikunimage/YYYYMMDD_HHMM_编辑主题.png \
  --retry 3
```

### Step 4: 展示结果

```
━━━ 编辑 #N ━━━
引擎：ikunimage (NanoBanana2 图生图)
输入：[输入图片路径]
比例：[aspect_ratio]

编辑描述：
[完整编辑提示词]

文件：[保存路径]

调整建议：
- [可调方向]
━━━━━━━━━━━━
```

---

## 批量生成

当用户需要一次生成多张图片时，使用并发批量模式。

### 文生图批量

**Step 1: 准备批量任务 JSON 文件**

```json
[
  {
    "prompt": "提示词内容1",
    "aspect_ratio": "3:4",
    "size": "2K",
    "output": "./outimage/ikunimage/20260225_1430_主题_01.png",
    "transparent": true
  },
  {
    "prompt": "提示词内容2",
    "aspect_ratio": "3:4",
    "size": "2K",
    "output": "./outimage/ikunimage/20260225_1430_主题_02.png"
  }
]
```

> `transparent` 字段可选，默认使用全局 `--transparent` 参数设置。

**Step 2: 执行**

```bash
# 使用默认白色背景
~/.hermes/.venv/bin/python ~/.hermes/skills/ikunimage/scripts/generate_ikun.py \
  --batch /tmp/ikun_batch.json \
  --workers 2 \
  --retry 3

# 全局透明背景（仅 gpt-image-2）
~/.hermes/.venv/bin/python ~/.hermes/skills/ikunimage/scripts/generate_ikun.py \
  --model gpt-image-2 --transparent \
  --batch /tmp/ikun_batch.json \
  --workers 2 \
  --retry 10
```

### 图生图批量

```json
[
  {
    "input": "/path/to/photo1.jpg",
    "prompt": "将背景改为雪景",
    "aspect_ratio": "3:4",
    "output": "./outimage/ikunimage/20260225_1430_雪景编辑_01.png",
    "transparent": true
  }
]
```

```bash
~/.hermes/.venv/bin/python ~/.hermes/skills/ikunimage/scripts/generate_ikun_edit.py \
  --model gpt-image-2 --transparent \
  --batch /tmp/ikun_edit_batch.json \
  --workers 2 \
  --retry 10
```

---

## 参数速查表

### 文生图 (generate_ikun.py)

| 参数 | 可选值 | 默认值 | 模式 |
|------|--------|--------|------|
| `--setup` | 无 | - | 配置 |
| `--api-key` | API Key 字符串 | 从配置加载 | 通用 |
| `--model` / `-m` | gemini-3.1-flash-image-preview, gpt-image-2 | NanoBanana2 | 通用 |
| `--prompt` / `-p` | 图片描述文本 | 必填（单图） | 单图 |
| `--aspect-ratio` / `-ar` | 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3, 21:9, 5:4, 4:5 | 1:1 | 单图 |
| `--size` / `-s` | 1K, 2K, 4K | 2K | 单图 |
| `--output` / `-o` | 文件路径 | output.png | 单图 |
| `--batch` / `-b` | JSON 文件路径 | 无 | 批量 |
| `--workers` / `-w` | 正整数 | 自动（默认 2） | 批量 |
| `--retry` / `-r` | 0-20 | NanoBanana2=3, gpt-image-2=10 | 通用 |
| `--transparent` / `-t` | 无 | False（白色背景） | 通用 |
| `--bg` | transparent, white | False | 通用 |

> `--prompt` 和 `--batch` 互斥，必须二选一。
> `--retry` 默认值根据模型稳定性自动调整：稳定模型 3 次，不稳定模型 10 次。
> `--transparent` 仅 gpt-image-2 支持，NanoBanana2 会自动回退到白色背景。

### 图生图 (generate_ikun_edit.py)

| 参数 | 可选值 | 默认值 | 模式 |
|------|--------|--------|------|
| `--setup` | 无 | - | 配置 |
| `--api-key` | API Key 字符串 | 从配置加载 | 通用 |
| `--model` / `-m` | gemini-3.1-flash-image-preview, gpt-image-2 | NanoBanana2 | 通用 |
| `--input` / `-i` | 输入图片路径 | 必填（单图） | 单图 |
| `--prompt` / `-p` | 编辑描述文本 | 必填（单图） | 单图 |
| `--aspect-ratio` / `-ar` | 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3, 21:9, 5:4, 4:5 | 1:1 | 单图 |
| `--output` / `-o` | 输出文件路径 | output.png | 单图 |
| `--batch` / `-b` | JSON 文件路径 | 无 | 批量 |
| `--workers` / `-w` | 正整数 | 自动（默认 2） | 批量 |
| `--retry` / `-r` | 0-20 | NanoBanana2=3, gpt-image-2=10 | 通用 |
| `--transparent` / `-t` | 无 | False（白色背景） | 通用 |
| `--bg` | transparent, white | False | 通用 |

> `--input`/`--prompt` 和 `--batch` 互斥。
> gpt-image-2 图生图使用 OpenAI `/v1/images/edits` 接口，可能需要更长超时。
> `--transparent` 仅 gpt-image-2 支持，NanoBanana2 会自动回退到白色背景。

---

## 用户追加修改

用户可在生成后要求调整：
- "光线换成逆光" → 修改光影段重新生成
- "背景改成户外" → 修改背景 + 环境光重新生成
- "换成竖版" → 仅更换 aspect_ratio 重新生成
- "换 4K" → 使用 4K 分辨率重新生成

### 图生图追加修改

- "再加一只猫" → 修改编辑描述重新生成
- "背景再暗一些" → 调整编辑描述中的光影/色调部分
- "换成横版" → 仅更换 aspect_ratio 重新生成
- "用另一张图" → 替换 --input 参数

## UI元素模板生成工作流

当需要提取游戏UI元素（如卡牌底框、按钮、面板等）时，**推荐直接生成独立模板**，而非从复杂合成图中裁剪提取。

### 原因
- 合成图中的UI元素可能被特效、阴影、其他元素遮挡
- 背景复杂导致抠图困难
- 单独生成的模板干净、背景纯色，方便后续处理

### 模板生成提示词要点
```
[类型]：游戏卡牌底框/按钮/面板UI模板
[风格]：保持与主图一致的风格（如Persona 5红黑波普艺术）
[形状]：横向圆角矩形，宽高比约X:Y
[配色]：边框颜色 + 内部白色填充区域
[装饰]：风格标志性几何元素（如P5的尖角、星形火花）
[约束]：无文字，无图案，纯底框模板，白色背景，适合抠图
```

### 示例命令
```bash
~/.hermes/.venv/bin/python ~/.hermes/skills/ikunimage/scripts/generate_ikun.py \
  --prompt "横向长条形游戏卡牌底框UI模板，Persona 5风格，红黑配色，波普艺术风格。圆角矩形边框，内部纯白色填充区域，边框有几何装饰元素，无文字无图案，白色背景方便抠图" \
  --aspect-ratio 16:9 \
  --size 2K \
  --output ./outimage/ikunimage/card_frame_template.png
```

---

## 注意事项

- 单渠道（ikun），无多渠道切换，重试在同渠道内进行（指数退避）
- **模型选择**：NanoBanana2 稳定但贵，gpt-image-2 便宜但可能不稳定
- **gpt-image-2 不稳定**：建议 `--retry 10`，超时更长（9-15分钟），耐心等待
- Cloudflare代理超时：可能出现 HTTP 524 超时错误，自动重试会处理
- **批量并发数**：建议不超过 2，并发过高容易触发 Cloudflare 524 超时
- 图片过大（> 4MB）会导致上传变慢或超时，建议压缩后再上传
- 编辑提示词中明确说"保持XX不变"可以提高保留原图元素的准确率
- 依赖：需在 Hermes 虚拟环境中安装 httpx 和 Pillow：
  ```bash
  ~/.hermes/.venv/bin/pip install httpx Pillow
  ```

---

## 常见陷阱与解决方案

### 陷阱1：图生图时形状约束与风格参考冲突

**问题描述**：当输入图片有强烈风格特征（如P5的锯齿边缘、不规则形状），但prompt中添加了冲突的形状约束（如"规整矩形"、"圆角矩形"），AI会优先响应形状约束，导致**完全丢失风格参考**。

**案例**：
- 输入：RaceWindow效果图（P5红黑波普风格、锯齿边缘）
- Prompt："规整矩形按钮，支持九宫格切分..."
- 结果：生成的是RPG金属风格（金黑配色），完全偏离P5风格

**解决方案**：
1. 如果需要保留风格 + 改变形状，用**文生图**而非图生图，在prompt中完整描述风格和形状
2. 如果需要图生图，prompt中不要添加与原图风格冲突的形状描述
3. 测试对比：可并行生成多个方案（如方案A保持形状、方案B保持风格），让用户选择

### 陷阱2：图生图时改变原图分辨率/宽高比

**问题描述**：图生图时使用 `--aspect-ratio` 参数会改变输出分辨率。如果原图是 16:9 横版（如1376×768），但使用了 3:4 竖版参数，输出会变成 896×1200，与原图尺寸完全不符。

**案例**：
- 原图：v9效果图 1376×768（16:9）
- 使用 `--aspect-ratio 3:4`
- 输出：v10变成 896×1200（竖版），用户抱怨分辨率被改了

**解决方案**：
1. 图生图前先用 `file` 命令或 PIL 检查原图分辨率和宽高比
2. 使用与原图一致的 `--aspect-ratio` 参数
3. 或者在prompt中明确强调"保持原图分辨率不变"

### 陷阱3："简化"≠"完全重设计"

**问题描述**：用户说"简化按钮装饰"时，AI可能理解为"重新设计按钮"，导致把核心造型也改了（如把动态多边形按钮改成普通矩形）。

**案例**：
- 用户："简化菜单栏按钮设计，不要过多的装饰"
- AI理解：把动态多边形按钮改成简洁几何矩形
- 用户反馈："按钮改的太过分了，原来的动态多边形那么帅，现在丑死了"

**解决方案**：
1. prompt中明确强调"保持XX造型不变，只简化装饰"
2. 区分：**造型**（shape/轮廓） vs **装饰**（decorations/光效/花纹）
3. 用户说"简化"时，追问或确认：是简化装饰还是改变造型？
4. 迭代时用上一版满意版本作为base，不要跳跃太大

### 陷阱4：九宫格切分 vs 不规则形状的设计矛盾

**问题描述**：九宫格(Sliced)拉伸要求UI元素是**规整的矩形/圆角矩形**（切分9个区域：4角+4边+中心）。但P5等风格的核心特征是**锯齿边缘、斜切平行四边形、不规则形状**，两者**互斥**。

**解决方案**：生成前向用户澄清选择：
- **方案A**：规整圆角矩形 + 风格化装饰（边框上添加尖角、速度线等），可九宫格拉伸，但视觉冲击力较弱
- **方案B**：生成两套（一套规整用于拉伸、一套不规则用于静态展示）
- **方案C**：放弃九宫格，全部不规则形状，每种尺寸单独切图

### 陷阱5：UI图集元素数量难以精确控制

**问题描述**：Prompt中指定"10种按钮、10种窗口框..."，AI生成时可能数量不足或过多，排列也不一定整齐。

**解决方案**：
1. 在prompt中强调"整齐排列、间距清晰、方便裁切"
2. 生成后检查数量，不足时可追加单独生成缺失元素
3. 大型复杂图集可拆分为多张单类型图集（如单独一张按钮图集、单独一张窗口框图集）

### 陷阱6：UI图集白色背景处理

**问题描述**：AI生成的UI图集背景通常是白色，但游戏项目中PNG需要透明背景。传统阈值法会误删UI内部的白色填充（如对话框的白色内容区域）。

**解决方案**：使用 `ui-image-processor` skill 的洪水填充法去背景：
- 只删除与图片边缘相连的白色区域（背景底图）
- 保留UI元素内部的白色填充（被边框包围的白色）
- 自动清理白色毛边（二次边界扫描）

```bash
# 去背景 + 自动切图
~/.hermes/.venv/bin/python ~/.hermes/skills/ui-image-processor/scripts/ui_sprite_splitter.py \
  --input UI图集.png --output-dir ./sprites/ --auto --remove-bg
```