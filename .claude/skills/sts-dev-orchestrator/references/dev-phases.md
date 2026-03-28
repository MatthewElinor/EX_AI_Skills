# Development Phases Reference

This document provides detailed task breakdowns and dependencies for each development phase.

## Phase Dependencies Graph

```
Phase 1 (Architecture)
    ↓
Phase 2 (Card) ←→ Phase 3 (Relic) ←→ Phase 4 (Map) ←→ Phase 5 (Event)
    ↓               ↓                   ↓               ↓
Phase 6 (UI) ←───────────────────────────────────────────
    ↓
Phase 7 (Integration)
    ↓
Phase 8 (TapTap Publishing)
```

**Overlap allowed**: Phases 2-5 can run concurrently or overlap
**Strict dependency**: Phase 6 needs 2-5 done, Phase 7 needs 1-6 done, Phase 8 needs 7 done

---

## Phase 1: Architecture Setup

**Duration**: Day 1
**Blocking**: Yes (all other phases depend on schemas)

### Task List

| Task | Description | Output File |
|------|-------------|-------------|
| Directory Structure | Create Unity project folders | `ARCHITECTURE.md` |
| Architecture Pattern | Choose and document pattern | `ARCHITECTURE.md` |
| Card Schema | Define card data JSON structure | `Data/CardSchema.json` |
| Relic Schema | Define relic data JSON structure | `Data/RelicSchema.json` |
| Event Schema | Define event data JSON structure | `Data/EventSchema.json` |
| Interface Design | Define system communication | `Interfaces.md` |

### Directory Structure Template

```
Assets/
├── Scripts/
│   ├── Core/
│   │   ├── GameManager.cs
│   │   ├── EventBus.cs
│   │   └── SaveManager.cs
│   ├── Card/
│   │   ├── CardData.cs
│   │   ├── DeckManager.cs
│   │   ├── CardController.cs
│   │   └── Effects/
│   ├── Relic/
│   │   ├── RelicData.cs
│   │   ├── RelicManager.cs
│   │   └── Effects/
│   ├── Map/
│   │   ├── MapGenerator.cs
│   │   ├── MapNode.cs
│   │   └── Nodes/
│   ├── Event/
│   │   ├── EventManager.cs
│   │   ├── EventData.cs
│   │   └── Scripts/
│   ├── UI/
│   │   ├── Screens/
│   │   └── Components/
│   ├── Combat/
│   │   └── [Existing combat system]
│   └── Platform/
│       └── TapTap/
├── Data/
│   ├── Cards/
│   ├── Relics/
│   ├── Events/
│   └── Enemies/
├── Art/
│   ├── Cards/
│   ├── Relics/
│   ├── UI/
│   └── Characters/
├── Audio/
│   ├── Music/
│   └── SFX/
└── Resources/
```

---

## Phase 2: Card System

**Duration**: Day 2-4
**Parallel with**: Phase 3, 4, 5

### Task List

| Task | Description | Sub-Skill |
|------|-------------|-----------|
| Card Schema | Define card data format | `/sts-data-design` |
| Initial Cards | Create 10+ starter cards | `/sts-data-design` |
| Deck Manager | Implement deck piles | `/sts-card-system` |
| Card Controller | Play flow logic | `/sts-card-system` |
| Effect Engine | Execute card effects | `/sts-card-system` |
| Card Effects | Implement specific cards | `/sts-card-effect` |
| Card Art | Generate art assets | `/sts-ai-art` |

### Card Types to Implement (Minimum)

**Attacks (4)**:
- Strike: 6 damage, 1 energy
- Bash: 8 damage + 2 Vulnerable, 2 energy
- Cleave: 8 damage to ALL, 1 energy
- Pommel Strike: 9 damage + draw 1, 1 energy

**Skills (4)**:
- Defend: 5 block, 1 energy
- Iron Wave: 5 block + 5 damage, 1 energy
- Shrug It Off: 8 block + draw 1, 1 energy
- Armaments: Gain 1 energy, 1 energy

**Powers (2)**:
- Inflame: Gain 2 Strength permanently
- Flex: Gain 2 Strength this turn

---

## Phase 3: Relic System

**Duration**: Day 3-5
**Parallel with**: Phase 2, 4, 5

### Task List

| Task | Description | Sub-Skill |
|------|-------------|-----------|
| Relic Schema | Define relic data format | `/sts-data-design` |
| Initial Relics | Create 8+ starter relics | `/sts-data-design` |
| Relic Manager | Acquire and hold relics | `/sts-relic-system` |
| Trigger System | Game event subscription | `/sts-relic-system` |
| Relic Effects | Implement specific relics | `/sts-relic-effect` |
| Relic Art | Generate art assets | `/sts-ai-art` |

### Trigger Timings

| Timing | When it fires |
|--------|---------------|
| OnBattleStart | Battle begins |
| OnBattleEnd | Battle ends |
| OnTurnStart | Player turn begins |
| OnTurnEnd | Player turn ends |
| OnCardPlayed | Any card played |
| OnAttackPlayed | Attack card played |
| OnSkillPlayed | Skill card played |
| OnDamageTaken | Player takes damage |
| OnDamageDealt | Player deals damage |
| OnEnemyKilled | Enemy dies |
| OnGoldGained | Player gains gold |
| OnCardObtained | Player gets new card |
| OnRelicObtained | Player gets new relic |

### Initial Relics (Minimum 8)

| Relic | Effect | Trigger |
|-------|--------|---------|
| Burning Blood | Heal 6 after battle | OnBattleEnd |
| Anchor | Start with 1 block | OnBattleStart |
| Vajra | Start with 1 strength | OnBattleStart |
| Bag of Marbles | Apply 1 Vulnerable to enemies | OnBattleStart |
| Happy Flower | Gain 1 energy every 3 turns | OnTurnStart |
| Shuriken | +1 strength after 3 attacks | OnAttackPlayed |
| Kunai | +1 dexterity after 3 skills | OnSkillPlayed |
| Wrist Blade | +4 damage to first attack | OnBattleStart |

---

## Phase 4: Map System

**Duration**: Day 4-6
**Parallel with**: Phase 2, 3, 5

### Task List

| Task | Description | Sub-Skill |
|------|-------------|-----------|
| Map Generator | Procedural layout | `/sts-map-system` |
| Node Types | Implement each type | `/sts-map-node` |
| Branching | Path choice logic | `/sts-map-system` |
| Map UI | Visualization and selection | `/sts-ui-system` |

### Map Structure

```
Floor 1 (3-4 nodes): Start → [Battle/Event/Shop] → [Battle/Elite/Event] → Boss
Floor 2 (4-5 nodes): More variety
Floor 3 (5-6 nodes): More elites, harder fights
Floor 4: Final Boss
```

### Node Types

| Node | Symbol | Description |
|------|--------|-------------|
| Start | ⭐ | Beginning of each floor |
| Battle | ⚔ | Normal combat |
| Elite | 👹 | Harder combat, relic reward |
| Event | ❓ | Random event |
| Shop | 💰 | Buy cards, relics, remove cards |
| Rest | 🛏 | Heal or upgrade card |
| Boss | 👿 | Floor boss |
| Treasure | 💎 | Free relic/gold |

---

## Phase 5: Event System

**Duration**: Day 5-7
**Parallel with**: Phase 2, 3, 4

### Task List

| Task | Description | Sub-Skill |
|------|-------------|-----------|
| Event Schema | Define event data format | `/sts-data-design` |
| Event Manager | Pool and selection | `/sts-event-system` |
| Event Scripts | Write specific events | `/sts-event-script` |
| Event UI | Text, choices, outcomes | `/sts-ui-system` |

### Event Types

| Type | Description | Example |
|------|-------------|---------|
| Trade | Gold for reward | "Pay 50 gold for rare card" |
| Risk | Random outcome | "Mystery box: 50% relic, 50% damage" |
| Choice | Multiple options | "Fight elite OR heal 20 HP" |
| Story | Flavor with minor reward | "Help traveler: gain 10 gold" |

### Initial Events (Minimum 6)

| Event | Type | Options |
|-------|------|---------|
| Big Fish | Trade | Pay gold for card OR leave |
| Shrine | Choice | Heal OR gain energy OR gain gold |
| Mysterious Portal | Risk | Enter (random outcome) OR leave |
| Card Trader | Trade | Pay gold for specific card |
| Beggar | Story | Give gold → gain blessing |
| Elite Challenge | Choice | Fight elite for relic OR skip |

---

## Phase 6: UI System

**Duration**: Day 6-8
**Depends on**: Phase 2-5 complete

### UI Screens

| Screen | Components |
|--------|------------|
| MainMenu | Title, Start, Settings, Exit |
| Combat | Hand, Energy orb, Enemy display, Player status, End turn |
| Map | Node visualization, Current position, Path lines |
| Shop | Card offers, Relic offers, Card removal, Gold display |
| Event | Event art, Text box, Choice buttons |
| Reward | Card choices, Gold, Relic |
| GameOver | Victory/Defeat message, Stats, Restart |

---

## Phase 7: Integration

**Duration**: Day 8-10
**Depends on**: All previous phases

### Integration Tasks

1. Connect card system to combat
2. Connect relic triggers to game events
3. Connect map to node encounters
4. Connect events to rewards
5. Implement save/load
6. Full game loop test
7. Bug tracking and fixes

---

## Phase 8: TapTap Publishing

**Duration**: Day 9-11
**Depends on**: Phase 7

### Publishing Tasks

1. WebGL build optimization
2. TapTap SDK initialization
3. Ad SDK integration
4. Test ad placements
5. Prepare store assets
6. Write game description
7. Submit for review