---
name: sts-architecture
description: >
  Design Unity project architecture for Slay the Spire-like roguelike card games. ALWAYS use this skill when: starting a new project, setting up code structure, defining directory layout, planning system interfaces, or creating data schemas. Trigger on phrases: "项目架构", "目录结构", "代码架构", "初始化项目", "新建项目", "项目结构", "Unity项目", "架构设计". Called by sts-dev-orchestrator during Phase 1. Produces ARCHITECTURE.md, CLASSES.md, Interfaces.md, and data schema JSON files.
model: inherit
---
# STS Architecture Designer

Design the complete Unity project architecture for a Slay the Spire-like roguelike card game.

## Output Deliverables

This skill produces these files:

| File | Purpose |
|------|---------|
| `ARCHITECTURE.md` | Overall architecture documentation |
| `CLASSES.md` | Core class design sketches |
| `Interfaces.md` | System communication contracts |
| `Data/CardSchema.json` | Card data structure definition |
| `Data/RelicSchema.json` | Relic data structure definition |
| `Data/EventSchema.json` | Event data structure definition |

## Architecture Pattern Recommendation

**Component-Based Architecture** (recommended for Unity)

Why:
- Fits Unity's GameObject-Component model
- Allows modular system design
- Easy to add/remove features
- Testable individual components

### Core Layers

```
┌─────────────────────────────────────┐
│           UI Layer                   │
│  (Screens, Components, Animations)   │
├─────────────────────────────────────┤
│        Game Logic Layer              │
│  (Card, Relic, Map, Event Systems)   │
├─────────────────────────────────────┤
│        Data Layer                    │
│  (JSON configs, ScriptableObjects)   │
├─────────────────────────────────────┤
│        Core Layer                    │
│  (GameManager, EventBus, SaveSystem) │
└─────────────────────────────────────┘
```

## Directory Structure

Create this Unity project structure:

```
Assets/
├── Scripts/
│   ├── Core/
│   │   ├── GameManager.cs          // Game state management
│   │   ├── EventBus.cs             // System-wide event bus
│   │   ├── SaveManager.cs          // Save/load functionality
│   │   └── GameSettings.cs         // Global settings
│   │
│   ├── Card/
│   │   ├── CardData.cs             // Card data structure
│   │   ├── DeckManager.cs          // Draw/discard/exhaust piles
│   │   ├── CardController.cs       // Card play logic
│   │   ├── CardEffectProcessor.cs  // Effect execution
│   │   └── Effects/                // Individual effect scripts
│   │
│   ├── Relic/
│   │   ├── RelicData.cs            // Relic data structure
│   │   ├── RelicManager.cs         // Relic collection
│   │   ├── RelicTriggerSystem.cs   // Trigger timing handler
│   │   └── Effects/                // Individual relic scripts
│   │
│   ├── Map/
│   │   ├── MapGenerator.cs         // Procedural generation
│   │   ├── MapNode.cs              // Node base class
│   │   ├── MapData.cs              // Map state data
│   │   └── Nodes/                  // Node type implementations
│   │
│   ├── Event/
│   │   ├── EventManager.cs         // Event pool and execution
│   │   ├── EventData.cs            // Event data structure
│   │   └── Scripts/                // Event scenario scripts
│   │
│   ├── UI/
│   │   ├── UIManager.cs            // Screen management
│   │   ├── Screens/                // UI screen controllers
│   │   └── Components/             // Reusable UI components
│   │
│   ├── Combat/
│   │   └── [Existing combat code]  // User's existing system
│   │
│   └── Platform/
│       └── TapTap/                 // Platform integration
│
├── Data/
│   ├── Cards/                      // Card JSON configs
│   ├── Relics/                     // Relic JSON configs
│   ├── Events/                     // Event JSON configs
│   ├── Enemies/                    // Enemy JSON configs
│   └── Balance/                    // Balance parameters
│
├── Art/
│   ├── Cards/                      // Card artwork
│   ├── Relics/                     // Relic artwork
│   ├── UI/                         // UI elements
│   └── Characters/                 // Character sprites
│
├── Audio/
│   ├── Music/                      // Background music
│   └── SFX/                        // Sound effects
│
└── Resources/                      // Addressable resources
```

## EventBus Design

Central communication hub for system decoupling:

```csharp
public static class EventBus
{
    // Battle events
    public static event Action OnBattleStart;
    public static event Action OnBattleEnd;
    public static event Action OnTurnStart;
    public static event Action OnTurnEnd;

    // Card events
    public static event Action<CardData> OnCardPlayed;
    public static event Action<CardData> OnCardDrawn;
    public static event Action<CardData> OnCardDiscarded;

    // Combat events
    public static event Action<int> OnDamageDealt;
    public static event Action<int> OnDamageTaken;
    public static event Action<Enemy> OnEnemyKilled;

    // Resource events
    public static event Action<int> OnGoldGained;
    public static event Action<int> OnEnergyChanged;
    public static event Action<RelicData> OnRelicObtained;

    // Trigger methods
    public static void TriggerBattleStart() => OnBattleStart?.Invoke();
    // ... etc
}
```

## Data Schema Design

Schemas for Card, Relic, and Event data are defined by `/sts-data-design` skill. Use that skill when creating detailed data structures.

### Data Loading Strategy

**Recommended**: JSON + Runtime Cache

```
JSON files → DataLoader → Runtime Dictionary → System access
```

Why:
- Easy to edit (no Unity recompile)
- Hot-reload during development
- Easy balancing without code changes
- Works well with Addressables

## Interface Definitions

Define contracts between systems:

```csharp
// Card system interfaces
public interface ICardEffect
{
    void Execute(CardContext context);
}

public interface IDeckManager
{
    List<CardData> DrawCards(int count);
    void DiscardCard(CardData card);
    void ExhaustCard(CardData card);
}

// Relic system interfaces
public interface IRelicEffect
{
    TriggerTiming Timing { get; }
    void OnTrigger(GameContext context);
}

// Map system interfaces
public interface IMapNode
{
    NodeType Type { get; }
    void Enter();
    bool CanEnter { get; }
}
```

## Workflow

1. **Ask about existing combat system**: Confirm integration points
2. **Generate directory structure**: Create Unity folders
3. **Write architecture docs**: ARCHITECTURE.md, CLASSES.md
4. **Define data schemas**: Card, Relic, Event JSON schemas
5. **Create interface definitions**: System contracts
6. **Set up EventBus**: Event definitions

## Integration with User's Combat System

Ask user:
- What interfaces does their combat system expose?
- How should cards/relics connect to combat?
- What events should combat fire?

Document integration points in `Interfaces.md`.