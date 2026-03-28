---
name: sts-map-system
description: >
  Implement the procedurally generated map system for Slay the Spire-like roguelike card games. ALWAYS use this skill when building map generation, node placement, branching paths, or floor progression. Trigger on phrases: "地图系统", "地图生成", "节点布局", "地图UI", "随机地图", "地图节点", "路径选择", "map generation", "procedural map". Called by sts-dev-orchestrator during Phase 4. Implements MapGenerator, MapNode, and MapUI components.
model: inherit
---
# STS Map System

Implement the procedurally generated map for a Slay the Spire-like roguelike card game.

## System Overview

The map consists of multiple floors with connected nodes. Players choose their path from start to boss, encountering battles, events, shops, and rest points.

## Map Structure

```
Floor 1 (4 nodes):
    Start → [Battle/Event] → [Battle/Elite/Shop] → Boss

Floor 2 (5 nodes):
    Start → [3 branches] → [convergence] → Boss

Floor 3 (6 nodes):
    Start → [4 branches] → [elite cluster] → Boss

Floor 4: Final Boss
```

### Node Types

| Node | Symbol | Description | Reward |
|------|--------|-------------|--------|
| Start | ⭐ | Floor entry point | None |
| Battle | ⚔ | Normal enemy | Gold + card |
| Elite | 👹 | Stronger enemy | Gold + relic |
| Event | ❓ | Random event | Variable |
| Shop | 💰 | Buy cards/relics | None (costs gold) |
| Rest | 🛏 | Heal OR upgrade card | HP or card upgrade |
| Boss | 👿 | Floor boss | Relic + gold + cards |
| Treasure | 💎 | Free loot | Relic or gold |

## Core Classes

### MapGenerator

```csharp
public class MapGenerator
{
    public MapData GenerateFloor(int floorNumber);

    private List<MapNode> GenerateNodes(int floor);
    private void ConnectNodes(List<MapNode> nodes);
    private void PlaceNodeTypes(List<MapNode> nodes, int floor);
    private void EnsureBossPath(List<MapNode> nodes);
}

public class MapData
{
    public int FloorNumber;
    public List<MapNode> Nodes;
    public int CurrentNodeIndex;
    public MapNode StartNode;
    public MapNode BossNode;
}
```

### MapNode

```csharp
public class MapNode
{
    public string Id;
    public NodeType Type;
    public int Floor;
    public List<MapNode> NextNodes;
    public List<MapNode> PreviousNodes;
    public bool IsCompleted;
    public bool CanEnter;

    public void Enter();
    public void Complete();
}
```

## Generation Algorithm

### Floor 1

```
1. Create 4 rows (Start → 2 → 3 → Boss)
2. Row 2: 2-3 nodes, mix of Battle/Event
3. Row 3: 1-2 nodes, can have Elite/Shop
4. Connect all possible paths
5. Ensure at least 2 valid routes to Boss
```

### Floor 2-3

```
1. More nodes per row
2. Branching paths (2-4 parallel nodes)
3. Convergence points before Boss
4. More Elite encounters
5. Rest nodes more common
```

### Node Type Distribution

Per floor (approximate):
- Battle: 60-70%
- Elite: 10-15%
- Event: 10-15%
- Shop: 5-10%
- Rest: 5-10%

## Map UI Components

### Map Screen

- Node visualization with icons
- Current position highlighted
- Available paths shown
- Completed nodes dimmed
- Node details on hover/click

### Path Selection

- Click available node to proceed
- Show preview of encounter
- Confirm before entering

## Node Encounter Flow

```
1. Player selects next node
2. Transition animation
3. Enter node type handler
4. Complete encounter
5. Return to map
6. Unlock next nodes
```

## Sub-Skill Calls

- `/sts-map-node` - Implement specific node type behaviors

## Event Bus Integration

Fire:
- `OnMapNodeEntered(node)`
- `OnMapNodeCompleted(node)`
- `OnFloorCompleted(floor)`
- `OnMapGenerated(floor)`

## Implementation Order

1. MapNode base class
2. MapGenerator with floor algorithms
3. Node type distribution logic
4. Path validation
5. MapUI visualization
6. Node entry/exit handlers
7. Connect to game flow

## References

Read `references/map-generation-algorithm.md` for detailed generation logic.