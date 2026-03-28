# EX_AI_Skills

我个人写的一些辅助开发的AI skill（Claude Code Skills）。

## Skills

### 类《杀戮尖塔》Roguelike小游戏开发Skill系列

一套完整的Skill体系，用于辅助开发类《杀戮尖塔》的卡牌Roguelike小游戏，目标平台为TapTap小游戏（WebGL）。

#### 一级Skill（主控）

| Skill | 描述 |
|-------|------|
| **sts-dev-orchestrator** | 主控Skill，协调整个开发流程，管理开发阶段，追踪进度 |
| **taptap-publisher** | TapTap平台集成主控，协调SDK接入、广告集成、上架提交 |

#### 二级Skill（系统）

| Skill | 描述 | 调用 |
|-------|------|------|
| **sts-architecture** | 项目架构设计，定义目录结构和数据Schema | - |
| **sts-data-design** | 游戏数据Schema设计和初始数据集创建 | - |
| **sts-card-system** | 卡牌系统实现（牌库、抽牌、弃牌、效果触发） | sts-card-effect, sts-data-design |
| **sts-relic-system** | 遗物系统实现（获取、被动效果、触发条件） | sts-relic-effect, sts-data-design |
| **sts-map-system** | 地图生成系统（节点、分支、层数） | sts-map-node |
| **sts-event-system** | 事件系统实现（随机事件、选择、结果） | sts-event-script |
| **sts-ui-system** | 游戏UI实现（HUD、菜单、卡牌展示） | - |
| **sts-ai-art** | AI美术生成流程（扁平卡通风格prompt模板） | - |
| **sts-integration** | 系统集成与测试，游戏流程串联 | - |
| **taptap-sdk-integration** | TapTap基础SDK集成 | - |
| **taptap-ad-integration** | TapTap广告SDK集成（激励视频） | - |
| **taptap-submit** | TapTap上架提交准备 | - |

#### 三级Skill（实现）

| Skill | 描述 | 调用者 |
|-------|------|--------|
| **sts-card-effect** | 单张卡牌效果实现 | sts-card-system |
| **sts-relic-effect** | 单个遗物效果实现 | sts-relic-system |
| **sts-event-script** | 单个事件场景脚本 | sts-event-system |
| **sts-map-node** | 地图节点类型实现 | sts-map-system |

### 通用Skill

| Skill | 描述 |
|-------|------|
| **game-task-spec** | 将自然语言描述的游戏开发需求转化为精炼的JSON任务规格文档 |
| **skill-creator** | Skill创建与优化工具，来自Anthropic官方 |

## 开发阶段与Skill调用流程

```
Phase 1: 架构搭建
/sts-dev-orchestrator → /sts-architecture

Phase 2: 卡牌系统
/sts-dev-orchestrator → /sts-card-system → /sts-card-effect, /sts-data-design, /sts-ai-art

Phase 3: 遗物系统
/sts-dev-orchestrator → /sts-relic-system → /sts-relic-effect, /sts-data-design, /sts-ai-art

Phase 4: 地图系统
/sts-dev-orchestrator → /sts-map-system → /sts-map-node

Phase 5: 事件系统
/sts-dev-orchestrator → /sts-event-system → /sts-event-script

Phase 6: UI系统
/sts-dev-orchestrator → /sts-ui-system

Phase 7: 系统集成
/sts-dev-orchestrator → /sts-integration

Phase 8: TapTap上架
/sts-dev-orchestrator → /taptap-publisher → /taptap-sdk-integration, /taptap-ad-integration, /taptap-submit
```

## 技术栈

- **引擎**: Unity WebGL
- **语言**: C#
- **目标平台**: TapTap小游戏
- **美术风格**: 扁平卡通（AI生成）
- **盈利模式**: 激励视频广告

## 目录结构

```
.claude/skills/
├── sts-dev-orchestrator/
├── taptap-publisher/
├── sts-architecture/
├── sts-data-design/
├── sts-card-system/
├── sts-relic-system/
├── sts-map-system/
├── sts-event-system/
├── sts-ui-system/
├── sts-ai-art/
├── sts-integration/
├── taptap-sdk-integration/
├── taptap-ad-integration/
├── taptap-submit/
├── sts-card-effect/
├── sts-relic-effect/
├── sts-event-script/
├── sts-map-node/
├── game-task-spec/
└── skill-creator/
```

## License

MIT