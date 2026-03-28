---
name: sts-integration
description: >
  Integrate all game systems and implement the complete game loop for Slay the Spire-like roguelike card games. ALWAYS use this skill when: connecting systems, implementing save/load, testing full gameplay, debugging integration issues, or connecting combat to cards/relics. Trigger on phrases: "系统集成", "游戏流程", "存档系统", "整合测试", "游戏循环", "save/load", "game loop", "系统集成测试". Called by sts-dev-orchestrator during Phase 7. Implements GameManager, SaveManager, and complete game flow.
model: inherit
---
# STS Integration

Integrate all game systems and implement the complete game loop for a Slay the Spire-like roguelike card game.

## Integration Points

### System Connections

| System | Connects To | Integration Method |
|--------|-------------|-------------------|
| Card System | Combat | Card effects → damage/block |
| Relic System | All Systems | EventBus triggers |
| Map System | Combat/Event/Shop | Node entry handlers |
| Event System | Rewards | Outcome processing |
| UI System | All Systems | Screen transitions |
| Combat | Card/Relic | Effect execution |

## Game Loop Flow

```
┌─────────────────────────────────────────────────────┐
│                     MAIN MENU                        │
│                  [Start Game]                        │
└───────────────────────┬─────────────────────────────┘
                        │
                        ↓
┌─────────────────────────────────────────────────────┐
│                  GAME START                          │
│  - Initialize player stats                           │
│  - Load starter deck                                 │
│  - Create run seed                                   │
└───────────────────────┬─────────────────────────────┘
                        │
                        ↓
┌─────────────────────────────────────────────────────┐
│                     MAP                              │
│  - Display floor map                                 │
│  - Player selects node                               │
│  - Enter node encounter                              │
└───────────────────────┬─────────────────────────────┘
                        │
          ┌─────────────┼─────────────┬─────────────┐
          │             │             │             │
          ↓             ↓             ↓             ↓
      ┌───────┐    ┌───────┐    ┌───────┐    ┌───────┐
      │BATTLE │    │EVENT  │    │SHOP   │    │REST   │
      └───────┘    └───────┘    └───────┘    └───────┘
          │             │             │             │
          ↓             ↓             ↓             ↓
      ┌───────┐    ┌───────┐    ┌───────┐    ┌───────┐
      │REWARD │    │RETURN │    │RETURN │    │RETURN │
      └───────┘    └───────┘    └───────┘    └───────┘
          │             │             │             │
          └─────────────┴─────────────┴─────────────┘
                        │
                        ↓
                [Next Node or Boss?]
                        │
          ┌─────────────┴─────────────┐
          │                           │
          ↓                           ↓
      ┌─────────┐               ┌───────────┐
      │BOSS     │               │NEXT FLOOR │
      │BATTLE   │               │(New Map)  │
      └─────────┘               └───────────┘
          │                           │
          ↓                           │
      ┌─────────┐                     │
      │BOSS     │                     │
      │REWARD   │                     │
      └─────────┘                     │
          │                           │
          └───────────────────────────┘
                        │
                        ↓
              [More Floors?]
                        │
          ┌─────────────┴─────────────┐
          │                           │
          ↓                           ↓
      ┌───────────────┐         ┌───────────┐
      │FINAL BOSS     │         │NEXT FLOOR │
      │(Floor 4)      │         │           │
      └───────────────┘         └───────────┘
          │                           │
          ↓                           ↓
      ┌───────────────┐               │
      │VICTORY/DEFEAT │               │
      └───────────────┘               │
          │                           │
          └───────────────────────────┘
                        │
                        ↓
              ┌─────────────────┐
              │   GAME OVER     │
              │   [Restart]     │
              └─────────────────┘
```

## Core Integration Classes

### GameManager

```csharp
public class GameManager
{
    public static GameManager Instance;

    public GameState CurrentState;
    public PlayerData Player;
    public MapData CurrentMap;
    public int CurrentFloor;

    public void StartNewRun();
    public void ContinueRun();
    public void EndRun(bool victory);
    public void EnterNode(MapNode node);
    public void CompleteNode();
    public void NextFloor();
}
```

### SaveManager

```csharp
public class SaveManager
{
    public void SaveRun(GameState state);
    public GameState LoadRun();
    public void DeleteRun();
    public bool HasSaveData();
}
```

## Save Data Structure

```json
{
  "run_id": "uuid",
  "seed": 12345,
  "current_floor": 2,
  "current_node": "node_3",
  "player": {
    "hp": 65,
    "max_hp": 80,
    "gold": 150,
    "deck": ["strike", "defend", "bash", ...],
    "relics": ["burning_blood", "anchor", ...]
  },
  "map_state": {
    "nodes_completed": ["node_1", "node_2"],
    "available_paths": [...]
  },
  "timestamp": "2024-01-15T10:30:00"
}
```

## EventBus Final Design

Complete event list for all systems:

```csharp
public static class EventBus
{
    // Game flow
    public static event Action OnGameStart;
    public static event Action OnRunEnd;
    public static event Action<int> OnFloorStart;
    public static event Action<int> OnFloorEnd;

    // Combat
    public static event Action OnBattleStart;
    public static event Action OnBattleEnd;
    public static event Action OnTurnStart;
    public static event Action OnTurnEnd;

    // Card
    public static event Action<CardData> OnCardPlayed;
    public static event Action<CardData> OnCardDrawn;
    public static event Action<CardData> OnCardDiscarded;
    public static event Action<CardData> OnCardExhausted;
    public static event Action<CardData> OnCardObtained;

    // Damage
    public static event Action<int> OnDamageDealt;
    public static event Action<int> OnDamageTaken;
    public static event Action<EnemyData> OnEnemyKilled;

    // Resources
    public static event Action<int> OnGoldGained;
    public static event Action<int> OnGoldSpent;
    public static event Action<int> OnEnergyChanged;
    public static event Action<int> OnHPChanged;

    // Relic
    public static event Action<RelicData> OnRelicObtained;

    // Map
    public static event Action<MapNode> OnNodeEntered;
    public static event Action<MapNode> OnNodeCompleted;
}
```

## Integration Testing Checklist

### System Connection Tests

- [ ] Cards deal damage to enemies in combat
- [ ] Cards grant block to player
- [ ] Relics trigger on correct events
- [ ] Relic effects apply correctly
- [ ] Map nodes transition to correct encounters
- [ ] Events process choices correctly
- [ ] Shop transactions work
- [ ] Rest node heal/upgrade works
- [ ] Rewards grant correct items
- [ ] UI screens transition smoothly

### Game Flow Tests

- [ ] Start → First map appears
- [ ] Battle → Reward → Return to map
- [ ] Event → Outcome → Return to map
- [ ] Shop → Purchase → Return to map
- [ ] Rest → Heal/Upgrade → Return to map
- [ ] Boss → Victory → Next floor
- [ ] Defeat → Game Over screen
- [ ] Victory → Game Over with stats

### Save/Load Tests

- [ ] Save creates file
- [ ] Load restores state
- [ ] Continue from save works
- [ ] New run clears save

## Bug Tracking

Use this format to track integration bugs:

| ID | System | Description | Status | Fix |
|----|--------|-------------|--------|-----|
| 1 | Card | Effect not triggering | Fixed | Add EventBus call |
| 2 | Relic | Trigger timing wrong | Open | Check subscription order |

## Implementation Order

1. GameManager with state management
2. EventBus complete implementation
3. System connection validation
4. SaveManager with JSON serialization
5. Game loop sequence testing
6. Bug fixing and polish
7. Final playthrough test

## References

Read `references/integration-checklist.md` for complete testing guide.