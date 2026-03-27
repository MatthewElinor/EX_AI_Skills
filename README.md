# EX_AI_Skills

我个人写的一些辅助开发的AI skill（Claude Code Skills）。

## Skills

### game-task-spec

将自然语言描述的游戏开发需求转化为精炼的 JSON 任务规格文档，供 AI Agent 直接执行。

- 输入：自然语言描述的游戏开发任务
- 输出：结构化 JSON 文档（含需求、架构、约束、测试计划等）
- 智能推测缺失的游戏开发细节，不确定时向用户确认
- 支持两种处理方式：立即执行 或 保存到 `~/.game-task-specs/`

### skill-creator

来自 [Anthropic 官方](https://github.com/anthropics/skills) 的 Skill 创建与优化工具，用于创建、测试和迭代改进 Claude Code Skills。
