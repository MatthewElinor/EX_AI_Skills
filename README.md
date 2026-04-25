# EX_AI_Skills

我个人写的一些辅助开发的AI skill（Claude Code Skills）。

## Skills

### UI美术资源生成流水线

一套完整的UI美术资源生产流水线，集成AI生图、去背景、智能切图。

| Skill | 描述 |
|-------|------|
| **ui-resource-generator** | 完整流水线主控，一键生成、去背景、切图 |
| **ikunimage** | AI图片生成器（IkunCode API） |
| **ui-image-processor** | UI图片去背景工具 |
| **ui-sprite-extractor** | 智能UI切图工具（连通区域分析） |

#### 流水线架构

```
ui-resource-generator（主控）
├── ikunimage          → AI生成UI图集
├── ui-image-processor → 白色背景去除
└── ui-sprite-extractor → 智能切图提取
```

#### 使用方式

```bash
# 完整流水线（推荐）
/ui-resource-generator

# 单独使用各模块
/ikunimage            # AI生图
/ui-image-processor  # 去背景
/ui-sprite-extractor # 切图
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

- **AI生图**: 使用 IkunCode API，支持 NanoBanana2 (Gemini Flash) 模型
- **去背景**: 洪水填充算法，阈值250，膨胀15像素，混合系数0.9
- **切图**: 连通区域分析，支持透明PNG输入，自动提取独立UI元素
- **布局计算**: 默认间距30像素，容错AI生图尺寸不确定性

## License

MIT