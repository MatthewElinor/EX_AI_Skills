---
name: sts-card-effect
description: >
  Implement individual card effects for Slay the Spire-like roguelike card games. ALWAYS use this skill when creating specific card implementations or writing card effect code. Trigger on phrases: "实现卡牌", "卡牌效果代码", "攻击卡", "技能卡", "能力卡", "写一张卡", "新卡牌". Also trigger when user provides a card name or describes what a card should do. Called by sts-card-system. Provides C# effect templates for Attack, Block, Buff, Debuff, Draw, Exhaust, and Special effects.
model: inherit
---
# STS Card Effect

Implement individual card effects for a Slay the Spire-like roguelike card game.

## Effect Categories

| Category | Purpose | Examples |
|----------|---------|----------|
| Attack | Deal damage to enemies | Strike, Bash, Cleave |
| Block | Grant block to player | Defend, Iron Wave |
| Buff | Apply positive status | Strength, Dexterity |
| Debuff | Apply negative status to enemies | Vulnerable, Weak |
| Special | Unique mechanics | Draw, Exhaust, Copy |

## Effect Template Structure

```csharp
public interface ICardEffect
{
    void Execute(CardContext context);
    string GetDescription();
}

public class CardContext
{
    public Player Player;
    public List<Enemy> Targets;
    public Enemy PrimaryTarget;
    public int BaseValue;
    int MagicNumber;
}
```

## Effect Implementations

### Attack Effect

```csharp
public class AttackEffect : ICardEffect
{
    public int Damage;
    public int Hits = 1;
    public bool Piercing = false;

    public void Execute(CardContext context)
    {
        for (int i = 0; i < Hits; i++)
        {
            int totalDamage = context.Player.ModifyDamage(Damage);

            if (context.PrimaryTarget != null)
            {
                context.PrimaryTarget.TakeDamage(totalDamage, Piercing);
                EventBus.OnDamageDealt?.Invoke(totalDamage);
            }
        }
    }
}
```

### Block Effect

```csharp
public class BlockEffect : ICardEffect
{
    public int BlockAmount;

    public void Execute(CardContext context)
    {
        int totalBlock = context.Player.ModifyBlock(BlockAmount);
        context.Player.GainBlock(totalBlock);
    }
}
```

### Apply Buff Effect

```csharp
public class ApplyBuffEffect : ICardEffect
{
    public BuffType Type;
    public int Stacks;
    public TargetType Target;

    public void Execute(CardContext context)
    {
        if (Target == TargetType.Player)
        {
            context.Player.AddBuff(Type, Stacks);
        }
        else if (Target == TargetType.Enemy)
        {
            foreach (var enemy in context.Targets)
            {
                enemy.AddBuff(Type, Stacks);
            }
        }
    }
}
```

### Draw Effect

```csharp
public class DrawEffect : ICardEffect
{
    public int CardsToDraw;

    public void Execute(CardContext context)
    {
        DeckManager.DrawCards(CardsToDraw);
    }
}
```

### Exhaust Effect

```csharp
public class ExhaustEffect : ICardEffect
{
    public bool ExhaustSelf = true;
    public int ExhaustOther = 0;

    public void Execute(CardContext context)
    {
        if (ExhaustSelf)
        {
            DeckManager.ExhaustCard(context.Card);
        }
    }
}
```

## Card Implementation Examples

### Strike (Basic Attack)

```csharp
public class Card_Strike : CardData
{
    public override void Initialize()
    {
        Name = "打击";
        Type = CardType.Attack;
        Cost = 1;
        Target = TargetType.SingleEnemy;

        Effects.Add(new AttackEffect { Damage = 6 });

        Upgrade = new CardUpgrade
        {
            DamageBonus = 3
        };
    }
}
```

### Bash (Attack + Debuff)

```csharp
public class Card_Bash : CardData
{
    public override void Initialize()
    {
        Name = "痛击";
        Type = CardType.Attack;
        Cost = 2;
        Target = TargetType.SingleEnemy;

        Effects.Add(new AttackEffect { Damage = 8 });
        Effects.Add(new ApplyBuffEffect
        {
            Type = BuffType.Vulnerable,
            Stacks = 2,
            Target = TargetType.Enemy
        });

        Upgrade = new CardUpgrade
        {
            DamageBonus = 2,
            BuffBonus = 1
        };
    }
}
```

### Defend (Basic Block)

```csharp
public class Card_Defend : CardData
{
    public override void Initialize()
    {
        Name = "防御";
        Type = CardType.Skill;
        Cost = 1;
        Target = TargetType.Self;

        Effects.Add(new BlockEffect { BlockAmount = 5 });

        Upgrade = new CardUpgrade
        {
            BlockBonus = 3
        };
    }
}
```

### Iron Wave (Attack + Block)

```csharp
public class Card_IronWave : CardData
{
    public override void Initialize()
    {
        Name = "铁甲波";
        Type = CardType.Attack;
        Cost = 1;
        Target = TargetType.SingleEnemy;

        Effects.Add(new BlockEffect { BlockAmount = 5 });
        Effects.Add(new AttackEffect { Damage = 5 });

        Upgrade = new CardUpgrade
        {
            BlockBonus = 2,
            DamageBonus = 2
        };
    }
}
```

### Inflame (Power - Permanent Buff)

```csharp
public class Card_Inflame : CardData
{
    public override void Initialize()
    {
        Name = "燃烧";
        Type = CardType.Power;
        Cost = 1;
        Target = TargetType.Self;

        Effects.Add(new ApplyBuffEffect
        {
            Type = BuffType.Strength,
            Stacks = 2,
            Target = TargetType.Player
        });

        Upgrade = new CardUpgrade
        {
            BuffBonus = 1
        };
    }
}
```

## Effect Templates

Read `templates/effect-templates.md` for complete effect library.

## Implementation Checklist

When implementing a new card:

1. [ ] Define card data (name, type, cost, target)
2. [ ] Implement effects with correct values
3. [ ] Add upgrade variant
4. [ ] Write Chinese description
5. [ ] Test in combat
6. [ ] Verify balance

## Balance Guidelines

| Cost | Expected Value |
|------|----------------|
| 0 | Minor effect (1-2 block, draw 1) |
| 1 | Standard (5-6 damage, 5 block) |
| 2 | Strong (10-12 damage, major effect) |
| 3 | Very strong (20+ damage, game-changing) |

## References

See game-task-spec for card data JSON format.