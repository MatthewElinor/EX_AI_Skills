---
name: sts-data-design
description: >
  Design game data schemas and create initial data sets for Slay the Spire-like roguelike card games. ALWAYS use this skill when: defining data structures ("数据结构", "数据Schema"), creating card/relic/event data files ("设计卡牌", "设计遗物", "编写事件数据"), or balancing game values ("数值平衡", "游戏平衡"). Trigger on phrases: "卡牌数据", "遗物数据", "事件数据", "JSON Schema", "数据格式", "初始卡牌", "初始遗物". Called by sts-card-system and sts-relic-system for data definitions. Produces CardSchema.json, RelicSchema.json, EventSchema.json, and initial data sets.
model: inherit
---
# STS Data Designer

Design data schemas and create initial game data for cards, relics, and events.

## Responsibilities

1. Define JSON schemas for game data types
2. Create initial data sets (starter cards, relics, events)
3. Provide balance guidelines and templates
4. Ensure data consistency and completeness

## Output Files

| File | Content |
|------|---------|
| `Data/CardSchema.json` | Card data structure definition |
| `Data/RelicSchema.json` | Relic data structure definition |
| `Data/EventSchema.json` | Event data structure definition |
| `Data/Cards/StarterDeck.json` | Initial player cards |
| `Data/Cards/CardPool.json` | All available cards |
| `Data/Relics/StarterRelics.json` | Initial relics pool |
| `Data/Events/EventPool.json` | All event scenarios |
| `BalanceGuidelines.md` | Value ranges and balance rules |

## Data Schemas

### Card Schema

Read detailed schema from `templates/card-schema.json`

Key fields:
```json
{
  "id": "strike",
  "name": "打击",
  "type": "Attack",
  "rarity": "Common",
  "cost": 1,
  "target": "Single",
  "effects": [...],
  "description": "造成6点伤害。",
  "upgrade": {...}
}
```

### Relic Schema

Read detailed schema from `templates/relic-schema.json`

Key fields:
```json
{
  "id": "burning_blood",
  "name": "燃烧之血",
  "tier": "Starter",
  "trigger": "OnBattleEnd",
  "effect": {...},
  "description": "战斗结束时恢复6点生命值。"
}
```

### Event Schema

Read detailed schema from `templates/event-schema.json`

Key fields:
```json
{
  "id": "big_fish",
  "name": "大鱼",
  "type": "Trade",
  "options": [
    {
      "text": "支付50金币获得一张稀有卡牌",
      "cost": {"gold": 50},
      "reward": {"card_rarity": "Rare"}
    }
  ]
}
```

## Workflow

### Card Design Process

1. Determine card purpose (attack, skill, power)
2. Set base values (cost, damage, block)
3. Add effects with parameters
4. Write upgrade variant
5. Balance against similar cards
6. Add Chinese description

### Relic Design Process

1. Define trigger timing
2. Set effect type and magnitude
3. Determine tier (Starter/Common/Uncommon/Rare)
4. Write clear description
5. Consider synergies

### Event Design Process

1. Set event type (Trade/Risk/Choice/Story)
2. Create 2-4 options
3. Define costs and rewards per option
4. Add flavor text
5. Balance risk/reward

## Balance Guidelines

### Quick Reference

**Card Cost vs Power**:
- Cost 0: Minor effect (1-2 block, draw 1)
- Cost 1: Standard effect (5-6 damage, 5 block)
- Cost 2: Strong effect (10-12 damage, 12 block, multi-hit)
- Cost 3: Very strong (20+ damage, major effect)

**Damage Balance**:
- Single target: 6-12 per energy
- Multi-target: 5-8 per target per energy
- Multi-hit: 3-5 per hit

**Block Balance**:
- Base block: 5 per energy
- Enhanced: 8-12 per energy

**Relic Power by Tier**:
- Starter: Minor passive (heal 6, start with 1 strength)
- Common: Moderate passive (gold on kill, draw 1 on shuffle)
- Uncommon: Strong passive (energy gain, damage boost)
- Rare: Major effect (unique mechanics)

## Initial Data Sets

### Starter Deck (10 cards)

| Card | Type | Cost | Effect |
|------|------|------|--------|
| Strike | Attack | 1 | 6 damage |
| Strike | Attack | 1 | 6 damage |
| Strike | Attack | 1 | 6 damage |
| Strike | Attack | 1 | 6 damage |
| Defend | Skill | 1 | 5 block |
| Defend | Skill | 1 | 5 block |
| Defend | Skill | 1 | 5 block |
| Defend | Skill | 1 | 5 block |
| Bash | Attack | 2 | 8 damage + 2 Vulnerable |

### Card Pool Examples

**Common Attacks**:
- Cleave: 8 damage to ALL, 1 energy
- Pommel Strike: 9 damage + draw 1, 1 energy
- Iron Wave: 5 block + 5 damage, 1 energy

**Common Skills**:
- Shrug It Off: 8 block + draw 1, 1 energy
- Armaments: Gain 1 energy, 1 energy
- True Grit: 7 block, exhaust 1 random, 1 energy

**Uncommon Powers**:
- Inflame: Gain 2 Strength, 1 energy
- Flex: Gain 2 Strength this turn, 0 energy

### Starter Relics Pool

| Relic | Tier | Effect |
|------|------|--------|
| Burning Blood | Starter | Heal 6 after battle |
| Anchor | Common | Start combat with 1 block |
| Vajra | Common | Start combat with 1 strength |
| Bag of Marbles | Uncommon | Enemies start with 1 Vulnerable |

### Event Pool Examples

| Event | Type | Key Option |
|------|------|------------|
| Big Fish | Trade | 50 gold → rare card |
| Shrine | Choice | Heal OR energy OR gold |
| Mysterious Portal | Risk | Random outcome |
| Card Trader | Trade | Gold → specific card |

## JSON Writing Rules

1. Always include `id` as unique identifier
2. Use lowercase snake_case for IDs
3. Include both English `id` and Chinese `name`
4. Every card must have `upgrade` variant
5. Effects use standardized format
6. Descriptions in Chinese, action-oriented