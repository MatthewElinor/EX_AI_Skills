---
name: sts-map-node
description: >
  Implement individual map node types for Slay the Spire-like roguelike card games. ALWAYS use this skill when creating node behaviors or writing node encounter logic. Trigger on phrases: "地图节点", "节点实现", "战斗节点", "商店节点", "事件节点", "休息节点", "Boss节点", "精英节点", "写一个节点". Also trigger when user describes a node type or asks to implement a specific encounter type. Called by sts-map-system. Provides implementations for Start, Battle, Elite, Event, Shop, Rest, Boss, and Treasure nodes.
model: inherit
---
# STS Map Node

Implement individual map node types for a Slay the Spire-like roguelike card game.

## Node Types

| Node | Symbol | Description | Reward |
|------|--------|-------------|--------|
| Start | ⭐ | Floor entry | None |
| Battle | ⚔ | Normal combat | Gold + Card |
| Elite | 👹 | Harder combat | Gold + Relic |
| Event | ❓ | Random event | Variable |
| Shop | 💰 | Buy cards/relics | Costs gold |
| Rest | 🛏 | Heal or upgrade | HP/Card upgrade |
| Boss | 👿 | Floor boss | Relic + Gold + Cards |
| Treasure | 💎 | Free loot | Relic or Gold |

## Node Base Class

```csharp
public abstract class MapNode
{
    public string Id;
    public NodeType Type;
    public int Floor;
    public List<MapNode> NextNodes;
    public List<MapNode> PreviousNodes;
    public bool IsCompleted;
    public bool IsAvailable;

    public abstract void Enter();
    public abstract void Complete();
    public virtual bool CanEnter() => IsAvailable && !IsCompleted;
}
```

## Node Implementations

### Start Node

```csharp
public class StartNode : MapNode
{
    public override NodeType Type => NodeType.Start;

    public override void Enter()
    {
        // No encounter, just starting point
        IsCompleted = true;
        UnlockNextNodes();
    }

    public override void Complete()
    {
        // Already handled in Enter
    }
}
```

### Battle Node

```csharp
public class BattleNode : MapNode
{
    public override NodeType Type => NodeType.Battle;

    public List<EnemyData> Enemies { get; private set; }
    public int GoldReward { get; private set; }
    public CardRarity CardRarity { get; private set; }

    public override void Enter()
    {
        // Generate enemies based on floor
        Enemies = EnemyGenerator.GetRandomEnemies(Floor);
        GoldReward = CalculateGoldReward(Floor);
        CardRarity = CardRarity.Common;

        // Start combat
        CombatManager.Instance.StartBattle(Enemies);
        CombatManager.OnBattleEnd += OnBattleEnd;
    }

    private void OnBattleEnd(bool victory)
    {
        if (victory)
        {
            Complete();
        }
        else
        {
            GameManager.Instance.GameOver();
        }
    }

    public override void Complete()
    {
        IsCompleted = true;
        UnlockNextNodes();

        // Show reward screen
        RewardManager.ShowRewards(GoldReward, CardRarity);
    }

    private int CalculateGoldReward(int floor)
    {
        return 10 + floor * 5 + Random.Range(-5, 10);
    }
}
```

### Elite Node

```csharp
public class EliteNode : MapNode
{
    public override NodeType Type => NodeType.Elite;

    public EnemyData EliteEnemy { get; private set; }

    public override void Enter()
    {
        EliteEnemy = EnemyGenerator.GetEliteEnemy(Floor);

        // Start harder combat
        CombatManager.Instance.StartBattle(new List<EnemyData> { EliteEnemy });
        CombatManager.OnBattleEnd += OnBattleEnd;
    }

    private void OnBattleEnd(bool victory)
    {
        if (victory)
        {
            Complete();
        }
        else
        {
            GameManager.Instance.GameOver();
        }
    }

    public override void Complete()
    {
        IsCompleted = true;
        UnlockNextNodes();

        // Elite rewards: relic + gold + card
        RewardManager.ShowEliteRewards();
    }
}
```

### Event Node

```csharp
public class EventNode : MapNode
{
    public override NodeType Type => NodeType.Event;

    private EventData currentEvent;

    public override void Enter()
    {
        // Get random event
        currentEvent = EventManager.GetRandomEvent(Floor);

        // Show event UI
        UIManager.ShowEventScreen(currentEvent);
        EventManager.OnEventComplete += OnEventComplete;
    }

    private void OnEventComplete()
    {
        Complete();
    }

    public override void Complete()
    {
        IsCompleted = true;
        UnlockNextNodes();

        EventManager.OnEventComplete -= OnEventComplete;
    }
}
```

### Shop Node

```csharp
public class ShopNode : MapNode
{
    public override NodeType Type => NodeType.Shop;

    public List<CardData> CardsForSale { get; private set; }
    public List<RelicData> RelicsForSale { get; private set; }
    public int RemoveCost { get; private set; }

    public override void Enter()
    {
        // Generate shop inventory
        CardsForSale = GenerateCardOffers();
        RelicsForSale = GenerateRelicOffers();
        RemoveCost = CalculateRemoveCost();

        // Show shop UI
        UIManager.ShowShopScreen(this);
        ShopManager.OnShopExit += OnShopExit;
    }

    private void OnShopExit()
    {
        Complete();
    }

    public override void Complete()
    {
        IsCompleted = true;
        UnlockNextNodes();
    }

    private List<CardData> GenerateCardOffers()
    {
        // 3 cards: 1 common, 1 uncommon, 1 rare
        var cards = new List<CardData>();
        cards.Add(CardPool.GetRandomCard(CardRarity.Common));
        cards.Add(CardPool.GetRandomCard(CardRarity.Uncommon));
        cards.Add(CardPool.GetRandomCard(CardRarity.Rare));
        return cards;
    }
}
```

### Rest Node

```csharp
public class RestNode : MapNode
{
    public override NodeType Type => NodeType.Rest;

    public override void Enter()
    {
        // Show rest options
        UIManager.ShowRestScreen(this);
    }

    public void ChooseHeal()
    {
        int healAmount = (int)(GameManager.Instance.Player.MaxHP * 0.3f);
        GameManager.Instance.Player.Heal(healAmount);
        Complete();
    }

    public void ChooseUpgrade()
    {
        // Show card upgrade selection
        UIManager.ShowUpgradeScreen();
        UpgradeManager.OnUpgradeComplete += OnUpgradeComplete;
    }

    private void OnUpgradeComplete()
    {
        Complete();
        UpgradeManager.OnUpgradeComplete -= OnUpgradeComplete;
    }

    public override void Complete()
    {
        IsCompleted = true;
        UnlockNextNodes();
    }
}
```

### Boss Node

```csharp
public class BossNode : MapNode
{
    public override NodeType Type => NodeType.Boss;

    public EnemyData BossEnemy { get; private set; }

    public override void Enter()
    {
        BossEnemy = EnemyGenerator.GetBoss(Floor);

        // Start boss battle
        CombatManager.Instance.StartBossBattle(BossEnemy);
        CombatManager.OnBattleEnd += OnBattleEnd;
    }

    private void OnBattleEnd(bool victory)
    {
        if (victory)
        {
            Complete();
        }
        else
        {
            GameManager.Instance.GameOver();
        }
    }

    public override void Complete()
    {
        IsCompleted = true;

        // Boss rewards: boss relic + gold + rare card
        RewardManager.ShowBossRewards();

        // Check if final boss
        if (Floor >= 4)
        {
            GameManager.Instance.Victory();
        }
        else
        {
            GameManager.Instance.NextFloor();
        }
    }
}
```

## Node Generation

```csharp
public static class NodeFactory
{
    public static MapNode CreateNode(NodeType type, int floor)
    {
        return type switch
        {
            NodeType.Start => new StartNode { Floor = floor },
            NodeType.Battle => new BattleNode { Floor = floor },
            NodeType.Elite => new EliteNode { Floor = floor },
            NodeType.Event => new EventNode { Floor = floor },
            NodeType.Shop => new ShopNode { Floor = floor },
            NodeType.Rest => new RestNode { Floor = floor },
            NodeType.Boss => new BossNode { Floor = floor },
            _ => throw new ArgumentException($"Unknown node type: {type}")
        };
    }
}
```

## Implementation Checklist

1. [ ] Define node type and symbol
2. [ ] Implement Enter() logic
3. [ ] Implement Complete() logic
4. [ ] Define rewards/encounters
5. [ ] Connect to other systems
6. [ ] Test node flow
7. [ ] Verify balance