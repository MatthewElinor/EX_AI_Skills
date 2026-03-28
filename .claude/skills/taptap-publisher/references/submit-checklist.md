# TapTap Submission Checklist

Use this checklist before submitting your game to TapTap.

## Pre-Submission Phase

### Technical Verification

- [ ] WebGL build completed successfully
- [ ] Build size under 30 MB (compressed)
- [ ] Game runs without crashes for 30+ minutes
- [ ] FPS maintained above 30 during gameplay
- [ ] Memory usage under 200 MB
- [ ] Initial load time under 10 seconds
- [ ] All game screens accessible and functional
- [ ] Save/load system works correctly
- [ ] Game loop complete (start → play → end)

### SDK Verification

- [ ] TapTap SDK initialized correctly
- [ ] App ID and keys configured properly
- [ ] User login works (if implemented)
- [ ] Share function works (if implemented)
- [ ] Ad SDK initialized
- [ ] Rewarded video ads load successfully
- [ ] Ads display correctly
- [ ] Rewards granted after ad completion
- [ ] Ad cooldown/frequency limits implemented
- [ ] No ad-related crashes

### Content Verification

- [ ] All text in Chinese (if targeting Chinese market)
- [ ] No prohibited content (violence, gambling, etc.)
- [ ] Age rating appropriate for content
- [ ] No unlicensed copyrighted content
- [ ] Privacy policy available (if collecting data)

---

## Materials Preparation

### Game Description (Chinese)

Template:
```
【游戏名称】是一款【类型】卡牌游戏。

【核心玩法描述】（例如：玩家通过收集卡牌和遗物，在随机生成的地图中挑战各种敌人）

【特色亮点】（例如：丰富多样的卡牌组合、策略性战斗、随机事件）

适合喜欢【类型】游戏的玩家，快来体验吧！
```

Example for STS-like game:
```
《卡牌冒险》是一款Roguelike卡牌战斗游戏。

玩家将扮演冒险者，通过收集和升级卡牌、获取神秘遗物，在随机生成的地图中挑战各种敌人。每次冒险都是全新的体验，不同的卡牌组合带来无限策略可能。

核心特色：
- 丰富的卡牌系统，支持多种流派
- 遗物系统提供永久增益
- 随机事件增添趣味与挑战
- 精美的扁平卡通美术风格

适合喜欢策略卡牌和Roguelike游戏的玩家，快来开启你的冒险！
```

### Screenshots Requirements

**Required screenshots (5-10)**:
1. Main menu screen
2. Combat screen (showing cards and enemy)
3. Map screen (showing nodes and paths)
4. Reward screen (card selection)
5. Shop screen
6. Event screen
7. Relic display
8. Game result screen

**Technical specs**:
- Resolution: 1280x720 recommended
- Format: PNG or JPG
- No UI mockups - must be actual game screens

### App Icon

**Requirements**:
- Size: 512x512 pixels
- Format: PNG with transparency optional
- Style: Simple, recognizable at small sizes
- No heavy text - icon should be visual

**Design tips**:
- Use main character or key game element
- Bold colors for visibility
- Test visibility at small sizes (64x64)

---

## Submission Process

### Developer Portal Steps

1. Log in to developer.taptap.cn
2. Create new application
3. Fill basic info:
   - Game name
   - Category (卡牌/策略)
   - Age rating
4. Upload materials:
   - APK/WebGL package
   - Screenshots
   - App icon
   - Description
5. Configure SDK:
   - Enter App ID
   - Set up ad placements
6. Submit for review

### Review Waiting Period

**Timeline**: 1-3 business days initial review

**Status tracking**:
- Check portal daily for status updates
- Respond to any feedback within 24 hours
- If rejected, fix issues and resubmit

---

## Post-Submission

### If Approved

- Game goes live within 24 hours
- Monitor analytics dashboard
- Respond to user reviews
- Plan first update based on feedback

### If Rejected

Common rejection reasons and fixes:

| Reason | Fix |
|--------|-----|
| Technical issues | Debug crashes, improve performance |
| Content violation | Remove prohibited content |
| Missing materials | Add required screenshots/info |
| Ad placement issue | Move ads to allowed placements |
| Copyright issue | Remove or license content |

**Resubmission**: Fix all issues, resubmit with explanation of changes

---

## Live Game Maintenance

### First Week Priorities

1. Monitor crash reports
2. Respond to user feedback
3. Fix critical bugs quickly
4. Optimize based on performance data

### Update Planning

- Schedule regular updates
- Add new cards/relics/events
- Balance adjustments based on data
- Seasonal events for engagement

### Analytics to Track

- Daily active users
- Average session length
- Ad engagement rate
- Retention rate (day 1, 7, 30)
- User reviews sentiment