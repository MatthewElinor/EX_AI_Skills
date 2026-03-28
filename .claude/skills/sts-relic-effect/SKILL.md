---
name: sts-relic-effect
description: >
  Implement individual relic effects for Slay the Spire-like roguelike card games. ALWAYS use this skill when creating specific relic implementations or writing relic effect code. Trigger on phrases: "实现遗物", "遗物效果代码", "遗物触发", "写一个遗物", "新遗物", "被动效果实现". Also trigger when user provides a relic name or describes what a relic should do. Called by sts-relic-system. Provides C# templates for OnBattleStart, OnTurnStart, OnCardPlayed, OnDamageDealt and other trigger timings.
model: inherit
---
# STS Relic Effect

Implement individual relic effects for a Slay the Spire-like roguelike card game.

## Trigger Timings

| Timing | When it Fires | Example Relics |
|--------|---------------|----------------|
| OnBattleStart | Combat begins | Anchor, Vajra |
| OnBattleEnd | Combat ends | Burning Blood |
| OnTurnStart | Player turn begins | Happy Flower |
| OnTurnEnd | Player turn ends | Clock |
| OnCardPlayed | Any card played | Shuriken |
| OnAttackPlayed | Attack card | Kunai |
| OnSkillPlayed | Skill card | Ornamental Fan |
| OnDamageTaken | Player hurt | Runic Cube |
| OnDamageDealt | Player attacks | Paper Phrog |
| OnEnemyKilled | Enemy dies | Golden Idol |
| OnGoldGained | Gain gold | Sssssnake |

## Relic Effect Template

```csharp
public abstract class RelicEffect
{
    public abstract TriggerTiming Timing { get; }
    public abstract void OnTrigger(RelicContext context);
}

public class RelicContext
{
    public Player Player;
    public Enemy Enemy;
    public CardData Card;
    public int Value; // damage amount, gold gained, etc.
}
```

## Relic Implementations

### Burning Blood (Heal After Battle)

```csharp
public class Relic_BurningBlood : RelicEffect
{
    public override TriggerTiming Timing => TriggerTiming.OnBattleEnd;

    public override void OnTrigger(RelicContext context)
    {
        context.Player.Heal(6);
        // Show effect: "+6 HP"
    }
}
```

### Anchor (Start with Block)

```csharp
public class Relic_Anchor : RelicEffect
{
    public override TriggerTiming Timing => TriggerTiming.OnBattleStart;

    public override void OnTrigger(RelicContext context)
    {
        context.Player.GainBlock(1);
        // Show effect: "+1 Block"
    }
}
```

### Vajra (Start with Strength)

```csharp
public class Relic_Vajra : RelicEffect
{
    public override TriggerTiming Timing => TriggerTiming.OnBattleStart;

    public override void OnTrigger(RelicContext context)
    {
        context.Player.AddBuff(BuffType.Strength, 1);
        // Show effect: "+1 Strength"
    }
}
```

### Shuriken (Count Attacks for Strength)

```csharp
public class Relic_Shuriken : RelicEffect
{
    private int attackCount = 0;

    public override TriggerTiming Timing => TriggerTiming.OnAttackPlayed;

    public override void OnTrigger(RelicContext context)
    {
        attackCount++;
        if (attackCount >= 3)
        {
            context.Player.AddBuff(BuffType.Strength, 1);
            attackCount = 0;
            // Show effect: "+1 Strength"
        }
    }
}
```

### Happy Flower (Energy Every 3 Turns)

```csharp
public class Relic_HappyFlower : RelicEffect
{
    private int turnCount = 0;

    public override TriggerTiming Timing => TriggerTiming.OnTurnStart;

    public override void OnTrigger(RelicContext context)
    {
        turnCount++;
        if (turnCount >= 3)
        {
            context.Player.GainEnergy(1);
            turnCount = 0;
            // Show effect: "+1 Energy"
        }
    }
}
```

### Golden Idol (Gold on Kill)

```csharp
public class Relic_GoldenIdol : RelicEffect
{
    public override TriggerTiming Timing => TriggerTiming.OnEnemyKilled;

    public override void OnTrigger(RelicContext context)
    {
        context.Player.GainGold(10);
        // Show effect: "+10 Gold"
    }
}
```

### Bag of Marbles (Vulnerable on Battle Start)

```csharp
public class Relic_BagOfMarbles : RelicEffect
{
    public override TriggerTiming Timing => TriggerTiming.OnBattleStart;

    public override void OnTrigger(RelicContext context)
    {
        foreach (var enemy in CombatManager.Instance.Enemies)
        {
            enemy.AddBuff(BuffType.Vulnerable, 1);
        }
        // Show effect: "Enemies +1 Vulnerable"
    }
}
```

### Clockwork Beetle (Time-based Effect)

```csharp
public class Relic_ClockworkBeetle : RelicEffect
{
    private int turnCount = 0;

    public override TriggerTiming Timing => TriggerTiming.OnTurnStart;

    public override void OnTrigger(RelicContext context)
    {
        turnCount++;
        if (turnCount % 2 == 0) // Every even turn
        {
            // Grant temporary block
            context.Player.GainBlock(4);
        }
    }
}
```

## Relic Data Structure

```csharp
public class RelicData
{
    public string Id;
    public string Name;
    public string Description;
    public RelicTier Tier;
    public RelicEffect Effect;
    public string IconPath;
}

public enum RelicTier
{
    Starter,    // Given at start
    Common,     // Frequent drops
    Uncommon,   // Regular drops
    Rare,       // Rare drops
    Boss        // Boss rewards
}
```

## Implementation Checklist

When implementing a new relic:

1. [ ] Define trigger timing
2. [ ] Implement OnTrigger logic
3. [ ] Set appropriate tier
4. [ ] Write clear description
5. [ ] Add visual effect trigger
6. [ ] Test with relevant scenarios
7. [ ] Verify balance

## Balance Guidelines

| Tier | Power Level | Example Effects |
|------|-------------|-----------------|
| Starter | Minor | Heal 6, +1 block on start |
| Common | Moderate | Gold on kill, draw on shuffle |
| Uncommon | Strong | Energy gain, damage boost |
| Rare | Very Strong | Unique mechanics, game-changing |
| Boss | Major | Significant permanent advantage |

## Templates

Read `templates/trigger-templates.md` for more effect patterns.