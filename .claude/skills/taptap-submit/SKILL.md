---
name: taptap-submit
description: >
  Prepare and submit game to TapTap mini-game platform. ALWAYS use this skill when: preparing submission materials, writing game description in Chinese, taking screenshots, or submitting for review. Trigger on phrases: "提交TapTap", "上架准备", "审核提交", "上架资料", "游戏描述", "提交审核", "应用图标", "截图", "游戏介绍". Called by taptap-publisher. Provides checklist for WebGL build, game description template, and submission process guidance.
model: inherit
---
# TapTap Submit

Prepare all materials and submit game to TapTap mini-game platform.

## Submission Materials Checklist

### Required Materials

1. **WebGL Build Package**
   - Optimized, compressed
   - Size under 30 MB (recommended)
   - All functionality working

2. **Game Description** (Chinese, 200-500 characters)
   - Genre and core gameplay
   - Key features
   - Target audience

3. **Screenshots** (5-10 images)
   - Main gameplay screens
   - Combat, map, shop, etc.
   - 1280x720 or similar resolution

4. **App Icon**
   - 512x512 pixels
   - PNG format
   - Simple, recognizable design

### Optional Materials

1. **Trailer Video** (30-60 seconds)
2. **Update Log**
3. **Developer Contact Info**

## Game Description Template

See `templates/game-description.md` for template.

### Template Structure

```
【游戏名称】是一款【类型】游戏。

【核心玩法描述】（一句话概括玩法）

【特色亮点】（3-5个要点）

适合喜欢【相关类型】的玩家，快来体验吧！
```

### Example for STS-like Game

```
《卡牌冒险》是一款Roguelike卡牌战斗游戏。

玩家通过收集和升级卡牌、获取神秘遗物，在随机生成的地图中挑战各种敌人。每次冒险都是全新的体验，不同的卡牌组合带来无限策略可能。

核心特色：
- 丰富的卡牌系统，支持多种流派玩法
- 遗物系统提供永久增益，增强策略深度
- 随机事件增添趣味与挑战
- 精美的扁平卡通美术风格

适合喜欢策略卡牌和Roguelike游戏的玩家，快来开启你的冒险之旅！
```

## Screenshots Guide

### Required Screenshots

| # | Screen | Purpose |
|---|--------|---------|
| 1 | Main Menu | Entry point |
| 2 | Combat (full) | Core gameplay |
| 3 | Hand/Cards | Card mechanics |
| 4 | Map | Progression system |
| 5 | Shop | Economy system |
| 6 | Event | Event system |
| 7 | Reward | Loot system |
| 8 | Victory | End state |

### Screenshot Requirements

- Actual gameplay (not mockups)
- Clear UI visibility
- No placeholder art
- Chinese text visible

## Submission Form

See `templates/submit-form.md` for complete form.

### Form Fields

```
基本信息:
- 游戏名称: _______________
- 游戏类型: 卡牌 / 策略 / Roguelike
- 适用年龄: 12+ / 16+

游戏描述:
- 简介: (200-500字)
- 详细介绍: (可选，500-2000字)

开发者信息:
- 开发者名称: _______________
- 联系邮箱: _______________
- 官网/社区: (可选)

上架资料:
- APK/WebGL包: [上传]
- 应用图标: [上传]
- 截图: [上传5-10张]
- 宣传视频: (可选)

SDK配置:
- App ID: _______________
- 广告配置: (在广告后台设置)
```

## Submission Process

### Step 1: Final Build Check

- [ ] WebGL build runs without errors
- [ ] All features functional
- [ ] SDK and ads working
- [ ] Save/load working
- [ ] No placeholder content

### Step 2: Prepare Materials

- [ ] Write game description
- [ ] Capture screenshots
- [ ] Create app icon
- [ ] Optimize build package

### Step 3: Developer Portal

1. Log in to developer.taptap.cn
2. Create new application
3. Fill all required fields
4. Upload materials
5. Configure SDK settings
6. Submit for review

### Step 4: Track Review

- Monitor portal for status
- Address feedback promptly
- Resubmit if needed

## Post-Submission

### If Approved

- Game goes live within 24 hours
- Announce on social media
- Monitor user reviews
- Plan first update

### If Rejected

Common reasons:
- Technical issues
- Content violations
- Missing materials
- Ad placement issues

Fix all issues and resubmit with explanation.

## Templates

- `templates/game-description.md` - Description template
- `templates/submit-form.md` - Complete form template