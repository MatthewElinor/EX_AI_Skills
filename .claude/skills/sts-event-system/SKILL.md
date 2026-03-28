---
name: sts-event-system
description: >
  Implement the random event system for Slay the Spire-like roguelike card games. ALWAYS use this skill when building event management, event pool selection, event UI, or outcome execution. Trigger on phrases: "事件系统", "随机事件", "事件选择", "事件UI", "事件池", "游戏事件", "event system", "random event". Also trigger when discussing choice-based scenarios or text events. Called by sts-dev-orchestrator during Phase 5. Implements EventManager, EventUI, and EventResultProcessor.
model: inherit
---
# STS Event System

Implement the random event system for a Slay the Spire-like roguelike card game.

## System Overview

Events are random encounters offering choices with risks and rewards. They add variety and strategic decisions outside of combat.

## Event Types

| Type | Description | Example |
|------|-------------|---------|
| Trade | Exchange resources | Pay gold for card/relic |
| Risk | Random outcome | Mystery box with chance of good/bad |
| Choice | Multiple options | Fight elite OR heal |
| Story | Flavor with minor effect | Help traveler, gain small reward |

## Core Classes

### EventManager

```csharp
public class EventManager
{
    private List<EventData> eventPool;
    private EventData currentEvent;

    public EventData GetRandomEvent(int floor);
    public void StartEvent(EventData event);
    public void SelectOption(int optionIndex);
    public void EndEvent();
}

public class EventData
{
    public string Id;
    public string Name;
    public EventType Type;
    public string Description;
    public string ImagePath;
    public List<EventOption> Options;
}
```

### EventOption

```csharp
public class EventOption
{
    public string Text;
    public Dictionary<string, int> Costs;  // gold, hp, etc.
    public Dictionary<string, object> Rewards;  // card, relic, gold, etc.
    public float Weight;  // for Risk events
}
```

### EventResultProcessor

```csharp
public class EventResultProcessor
{
    public void ProcessOption(EventOption option);

    private void ApplyCosts(Dictionary<string, int> costs);
    private void ApplyRewards(Dictionary<string, object> rewards);
    private EventResult ResolveRiskEvent(EventData event);
}
```

## Event Flow

```
1. Enter event node on map
2. EventManager selects event
3. Show event UI (image + text + options)
4. Player reads and chooses
5. Process costs if applicable
6. Process rewards
7. Show outcome
8. Return to map
```

## Event Pool Management

### Pool Composition

- Events organized by type
- Some events floor-specific
- Certain events require conditions
- Pool refreshes on new run

### Selection Logic

```csharp
public EventData GetRandomEvent(int floor)
{
    // Filter by floor requirements
    var eligible = eventPool.Where(e => CanAppear(e, floor));

    // Weight by type distribution
    var weights = eligible.Select(e => GetWeight(e, floor));

    // Random weighted selection
    return WeightedRandom.Select(eligible, weights);
}
```

## UI Components

### Event Screen

- Event artwork/illustration
- Title and description
- Option buttons (2-4)
- Cost indicators on options
- Reward preview

### Outcome Display

- Result text
- Gained/lost items
- Transition back to map

## Event Examples

### Trade Event: Big Fish

```
Title: 大鱼
Description: 你在河边遇到一条巨大的鱼，它似乎想和你交换...
Options:
  1. "支付50金币获得一张稀有卡牌" (50 gold → rare card)
  2. "支付30金币获得一个普通遗物" (30 gold → common relic)
  3. "离开" (no cost, no reward)
```

### Risk Event: Mysterious Portal

```
Title: 神秘传送门
Description: 一扇发光的传送门出现在你面前，你感觉到里面有强大的力量...
Options:
  1. "进入传送门" (random: 50% relic, 30% gold, 20% damage)
  2. "离开" (safe)
```

### Choice Event: Shrine

```
Title: 神殿
Description: 你发现一座古老的神殿，三种祭坛散发着不同的光芒...
Options:
  1. "治疗祭坛 - 恢复25%生命" (heal 25% HP)
  2. "力量祭坛 - 获得1点永久力量" (+1 strength)
  3. "财富祭坛 - 获得30金币" (30 gold)
```

## Sub-Skill Calls

- `/sts-data-design` - Get event schema
- `/sts-event-script` - Create individual events

## Event Bus Integration

Fire:
- `OnEventStarted(event)`
- `OnEventOptionSelected(option)`
- `OnEventCompleted(event)`

## Implementation Order

1. EventData class and loading
2. EventManager with pool and selection
3. EventResultProcessor with cost/reward logic
4. EventUI screen
5. Connect to map node entry
6. Create initial events via sts-event-script

## References

Read `references/event-examples.md` for more event designs.