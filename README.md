# EX_AI_Skills

我个人写的一些辅助开发的AI skill（Claude Code Skills）。

## Skills

### UI美术资源生成流水线

一套完整的UI美术资源生产流水线，集成AI生图、去背景、智能切图、相似度去重。

| Skill | 描述 |
|-------|------|
| **ui-resource-generator** | 完整流水线主控，一键生成、去背景、切图 |
| **ui-extraction-from-screenshot** | 从效果图提取UI素材，AI识别→用户选择→提取→去重 |
| **ikunimage** | AI图片生成器（IkunCode API） |
| **ui-image-processor** | UI图片去背景工具 |
| **ui-sprite-extractor** | 智能UI切图工具（连通区域分析） |

#### 流水线架构

```
ui-resource-generator（生成流）
├── ikunimage          → AI生成UI图集
├── ui-image-processor → 白色背景去除
└── ui-sprite-extractor → 智能切图提取

ui-extraction-from-screenshot（提取流）
├── vision分析         → AI识别效果图中的UI元素
├── ikunimage          → AI图生图提取UI图集
├── ui-image-processor → 白色背景去除
├── ui-sprite-extractor → 智能切图提取
└── ui_similarity_dedup → 相似度去重
```

#### 使用方式

```bash
# 生成流（从零生成UI）
/ui-resource-generator

# 提取流（从效果图扒UI）
/ui-extraction-from-screenshot

# 单独使用各模块
/ikunimage            # AI生图
/ui-image-processor   # 去背景
/ui-sprite-extractor  # 切图
```

### 通用Skill

| Skill | 描述 |
|-------|------|
| **game-task-spec** | 将自然语言描述的游戏开发需求转化为精炼的JSON任务规格文档 |
| **skill-creator** | Skill创建与优化工具，来自Anthropic官方 |

## 目录结构

```
.claude/skills/
├── game-task-spec/
└── skill-creator/

（根目录）
├── ui-resource-generator/
│   ├── SKILL.md
│   └── scripts/
│       └── atlas_layout_calculator.py
├── ui-extraction-from-screenshot/
│   ├── SKILL.md
│   └── scripts/
│       └── ui_similarity_dedup.py
├── ikunimage/
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── generate_ikun.py
│   │   └── generate_ikun_edit.py
│   └── references/
│       └── api-reference.md
├── ui-image-processor/
│   ├── SKILL.md
│   └── scripts/
│       └── ui_background_remover.py
└── ui-sprite-extractor/
    └── SKILL.md
```

## 技术要点

### 生成流
- **AI生图**: 使用 IkunCode API，支持 NanoBanana2 (Gemini Flash) 模型
- **去背景**: 洪水填充算法，阈值250，膨胀15像素，混合系数0.9
- **切图**: 连通区域分析，支持透明PNG输入，自动提取独立UI元素
- **布局计算**: 默认间距30像素，容错AI生图尺寸不确定性

### 提取流
- **AI识别**: vision_analyze 分析效果图，识别面板/控件/装饰三类UI元素
- **用户选择**: 支持序号选择、类别选择、排除模式
- **Prompt定制**: 根据用户选择动态生成提取prompt
- **相似度去重**: 感知哈希+汉明距离，阈值10（约4%差异）

## License

MIT