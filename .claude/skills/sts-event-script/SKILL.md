---
name: sts-event-script
description: >
  Write individual event scenarios for Slay the Spire-like roguelike card games. ALWAYS use this skill when creating event stories, designing event options, or writing event JSON data. Trigger on phrases: "编写事件", "事件剧本", "事件选项", "事件JSON", "写一个事件", "新事件", "事件场景", "设计事件". Also trigger when user describes an event scenario or provides event theme. Called by sts-event-system. Provides JSON templates for Trade, Risk, Choice, and Story event types.
model: inherit
---
# STS Event Script

Write individual event scenarios for a Slay the Spire-like roguelike card game.

## Event Types

| Type | Description | Risk Level |
|------|-------------|------------|
| Trade | Exchange resources for rewards | Low |
| Risk | Random outcomes | High |
| Choice | Multiple options with tradeoffs | Medium |
| Story | Flavor text with minor effect | Low |

## Event Data Structure

```json
{
  "id": "event_id",
  "name": "事件名称",
  "type": "Trade|Risk|Choice|Story",
  "description": "事件描述文本...",
  "image": "path/to/event/image.png",
  "options": [
    {
      "text": "选项文本",
      "cost": {
        "gold": 50,
        "hp": 0
      },
      "reward": {
        "card_rarity": "Rare",
        "relic_tier": "Common",
        "gold": 0,
        "heal": 0
      },
      "requirement": {
        "min_gold": 50
      }
    }
  ]
}
```

## Event Scripts

### Trade Event: Big Fish

```json
{
  "id": "big_fish",
  "name": "大鱼",
  "type": "Trade",
  "description": "你在河边遇到一条巨大的鱼，它用智慧的眼神看着你。它似乎想和你交换什么东西...",
  "image": "events/big_fish.png",
  "options": [
    {
      "text": "支付50金币获得一张稀有卡牌",
      "cost": { "gold": 50 },
      "reward": { "card_rarity": "Rare" },
      "requirement": { "min_gold": 50 }
    },
    {
      "text": "支付30金币获得一个普通遗物",
      "cost": { "gold": 30 },
      "reward": { "relic_tier": "Common" },
      "requirement": { "min_gold": 30 }
    },
    {
      "text": "离开",
      "cost": {},
      "reward": {}
    }
  ]
}
```

### Risk Event: Mysterious Portal

```json
{
  "id": "mysterious_portal",
  "name": "神秘传送门",
  "type": "Risk",
  "description": "一扇发光的传送门出现在你面前，你感觉到里面有强大的力量，但也充满危险...",
  "image": "events/portal.png",
  "options": [
    {
      "text": "进入传送门",
      "cost": {},
      "reward": {},
      "risk_outcomes": [
        { "weight": 40, "reward": { "relic_tier": "Rare" }, "text": "你发现了一个珍贵的遗物！" },
        { "weight": 30, "reward": { "gold": 50 }, "text": "你发现了一袋金币！" },
        { "weight": 20, "cost": { "hp": 10 }, "text": "传送门突然崩塌，你受到了伤害。" },
        { "weight": 10, "reward": { "card_rarity": "Rare", "gold": 30 }, "text": "真是幸运！你获得了一张稀有卡牌和金币！" }
      ]
    },
    {
      "text": "离开这里",
      "cost": {},
      "reward": {}
    }
  ]
}
```

### Choice Event: Shrine

```json
{
  "id": "shrine",
  "name": "神殿",
  "type": "Choice",
  "description": "你发现一座古老的神殿，三种祭坛散发着不同的光芒。你可以选择一种祝福...",
  "image": "events/shrine.png",
  "options": [
    {
      "text": "生命祭坛 - 恢复25%最大生命值",
      "cost": {},
      "reward": { "heal_percent": 25 }
    },
    {
      "text": "力量祭坛 - 获得1点永久力量",
      "cost": {},
      "reward": { "permanent_strength": 1 }
    },
    {
      "text": "财富祭坛 - 获得30金币",
      "cost": {},
      "reward": { "gold": 30 }
    }
  ]
}
```

### Story Event: Traveler

```json
{
  "id": "traveler",
  "name": "旅行者",
  "type": "Story",
  "description": "一位疲惫的旅行者向你求助。他说他被强盗抢走了所有财物，现在无处可去...",
  "image": "events/traveler.png",
  "options": [
    {
      "text": "给他10金币",
      "cost": { "gold": 10 },
      "reward": { "heal": 5 },
      "requirement": { "min_gold": 10 }
    },
    {
      "text": "给他一张卡牌",
      "cost": { "random_card": 1 },
      "reward": { "gold": 15 }
    },
    {
      "text": "抱歉，我也自身难保",
      "cost": {},
      "reward": {}
    }
  ]
}
```

### Elite Challenge Event

```json
{
  "id": "elite_challenge",
  "name": "精英挑战",
  "type": "Choice",
  "description": "一位战士挡住了你的去路。他提出：如果你能击败他，他会给你一个珍贵的遗物作为奖励。",
  "image": "events/elite_challenge.png",
  "options": [
    {
      "text": "接受挑战",
      "cost": {},
      "reward": {},
      "encounter": "elite_battle",
      "encounter_reward": { "relic_tier": "Rare", "gold": 30 }
    },
    {
      "text": "绕道而行",
      "cost": {},
      "reward": {}
    }
  ]
}
```

## Event Writing Guidelines

### Description Rules

1. Set the scene clearly
2. Create atmosphere
3. Make choices feel meaningful
4. Keep it concise (2-4 sentences)

### Balance Guidelines

| Event Type | Risk/Reward Ratio |
|------------|-------------------|
| Trade | Equal value exchange |
| Risk | Higher variance, possible loss |
| Choice | Meaningful tradeoffs |
| Story | Minor effects, flavor focus |

## Implementation Checklist

1. [ ] Write event ID and name
2. [ ] Choose event type
3. [ ] Write description
4. [ ] Create 2-4 options
5. [ ] Define costs and rewards
6. [ ] Add requirements (if any)
7. [ ] Test event flow
8. [ ] Verify balance