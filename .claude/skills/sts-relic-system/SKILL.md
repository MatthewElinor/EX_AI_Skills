---
name: sts-relic-system
description: >
  Implement the relic system for Slay the Spire-like roguelike card games. ALWAYS use this skill when building relic management, trigger timing system, or relic effect execution. Trigger on phrases: "遗物系统", "遗物管理", "遗物效果", "触发时机", "被动效果", "遗物触发", "relic", "artifact". Also trigger when discussing passive items or trigger-based effects in games. Called by sts-dev-orchestrator during Phase 3. Implements RelicManager, RelicTriggerSystem, and RelicEffectProcessor.
model: inherit
---
# STS Relic System

Implement the relic mechanics with trigger-based effects for a Slay the Spire-like roguelike card game.

## System Overview

Relics are permanent items that provide passive effects triggered at specific game events.

### Core Components

| Module | Responsibility |
|--------|----------------|
| RelicManager | Hold and manage owned relics |
| RelicTriggerSystem | Subscribe to events and trigger relics |
| RelicEffectProcessor | Execute relic effects |
| RelicUI | Display relic collection |

## Trigger Timing System

### Trigger Types

| Timing | When Fired | Example Relics |
|--------|------------|----------------|
| OnBattleStart | Combat begins | Anchor (start with block), Vajra (start with strength) |
| OnBattleEnd | Combat ends | Burning Blood (heal 6) |
| OnTurnStart | Player turn begins | Happy Flower (energy every 3 turns) |
| OnTurnEnd | Player turn ends | Clock (track turns) |
| OnCardPlayed | Any card played | Shuriken (count attacks) |
| OnAttackPlayed | Attack card specifically | Kunai (count for dex) |
| OnSkillPlayed | Skill card specifically | Ornamental Fan (count for block) |
| OnDamageTaken | Player takes damage | Runic Cube (draw on damage) |
| OnDamageDealt | Player deals damage | Paper Phrog (bonus damage) |
| OnEnemyKilled | Enemy dies | Golden Idol (gold on kill) |
| OnGoldGained | Player gains gold | Sssssnake (bonus gold) |
| OnCardObtained | New card obtained | Courier (upgrade new cards) |
| OnRelicObtained | New relic obtained | Mummified Hand (random relic bonus) |

## Core Classes

### RelicManager

```csharp
public class RelicManager
{
    private List<RelicData> ownedRelics;
    private Dictionary<TriggerTiming, List<RelicData>> relicByTrigger;

    public void AddRelic(RelicData relic);
    public void RemoveRelic(RelicData relic);
    public List<RelicData> GetRelicsForTrigger(TriggerTiming timing);
    public bool HasRelic(string relicId);
    public int GetRelicCount(string relicId);
}
```

### RelicTriggerSystem

```csharp
public class RelicTriggerSystem
{
    private RelicManager relicManager;

    public void Initialize()
    {
        // Subscribe to EventBus events
        EventBus.OnBattleStart += OnBattleStartHandler;
        EventBus.OnTurnStart += OnTurnStartHandler;
        EventBus.OnCardPlayed += OnCardPlayedHandler;
        // ... all triggers
    }

    private void TriggerRelics(TriggerTiming timing, GameContext context)
    {
        var relics = relicManager.GetRelicsForTrigger(timing);
        foreach (var relic in relics)
        {
            RelicEffectProcessor.Process(relic, context);
        }
    }
}
```

### RelicEffectProcessor

```csharp
public class RelicEffectProcessor
{
    public static void Process(RelicData relic, GameContext context)
    {
        switch (relic.EffectType)
        {
            case RelicEffectType.StatBuff:
                ApplyStatBuff(relic, context);
                break;
            case RelicEffectType.Heal:
                HealPlayer(relic, context);
                break;
            case RelicEffectType.Draw:
                DrawCards(relic, context);
                break;
            case RelicEffectType.GainGold:
                GainGold(relic, context);
                break;
            // ... other types
        }
    }
}
```

## Relic Effect Types

| Effect Type | Description | Example |
|-------------|-------------|---------|
| StatBuff | Modify player stats | +1 Strength at battle start |
| Heal | Restore HP | Heal 6 after battle |
| Block | Grant block | Start battle with block |
| Draw | Draw cards | Draw 1 on shuffle |
| Energy | Gain energy | +1 energy every 3 turns |
| Gold | Gain gold | +gold on enemy kill |
| Card | Get card | Random card reward |
| Debuff | Apply to enemies | Vulnerable to all enemies |
| Special | Unique mechanics | Custom effect implementation |

## Relic Tiers

| Tier | Rarity | Power Level |
|------|--------|-------------|
| Starter | Always given | Minor passive effect |
| Common | Frequent drops | Moderate effect |
| Uncommon | Regular drops | Strong effect |
| Rare | Rare drops | Very strong/unique |
| Boss | Boss rewards | Major game-changing |
| Shop | Purchase only | Premium effects |

## UI Components

### Combat Relic Display

- Show owned relics in strip
- Hover shows description
- Click for detailed info
- Active relics highlighted

### Reward Relic Display

- Show 3 relic choices
- Compare descriptions
- Select to claim

## Event Bus Integration

Subscribe to:
- All trigger timing events from EventBus

Fire:
- `OnRelicObtained(relic)` when player gets relic

## Sub-Skill Calls

- `/sts-data-design` - Get relic schema and initial relics
- `/sts-relic-effect` - Implement specific relic effects
- `/sts-ai-art` - Generate relic icons

## Implementation Order

1. RelicData class and loading
2. RelicManager with add/get operations
3. RelicTriggerSystem with EventBus subscriptions
4. RelicEffectProcessor with effect types
5. RelicUI display
6. Connect to combat via triggers
7. Implement initial relics via sts-relic-effect