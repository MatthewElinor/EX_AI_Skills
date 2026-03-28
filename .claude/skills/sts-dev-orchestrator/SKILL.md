---
name: sts-dev-orchestrator
description: >
  Master orchestrator for developing Slay the Spire-like roguelike card games. ALWAYS use this skill when the user mentions ANY of these contexts: starting game development ("开始开发", "启动项目"), continuing development ("继续开发", "下一步"), checking progress ("开发进度", "当前状态"), or discussing overall game development plan. Also trigger when user mentions roguelike, card game, Slay the Spire, deckbuilder, or similar game genres in a development context. This skill coordinates all 8 development phases and automatically invokes appropriate sub-skills. Do NOT trigger for general programming questions unrelated to game development.
model: inherit
---
# STS Dev Orchestrator

Master skill that orchestrates the entire development workflow for a Slay the Spire-like roguelike card game. It manages development phases, tracks progress, and automatically invokes the appropriate sub-skills at each stage.

## Project Context

- **Target**: Web-based mini-game for TapTap platform
- **Engine**: Unity WebGL
- **Timeline**: 1-2 weeks
- **Core Features**: Card system, Relic system, Map system, Event system
- **Monetization**: TapTap ad SDK (rewarded video ads)

## Workflow

### Phase 0: Initialize or Resume

1. Check if `.sts-dev-state.json` exists in project root
2. If exists: read current state, determine current phase
3. If not exists: create initial state file, start from Phase 1

**Progress File Location**: Project root directory, `.sts-dev-state.json`

### Phase Execution Loop

For each phase, the orchestrator:
1. Presents the phase goals to user
2. Calls the appropriate sub-skills
3. Tracks completion of phase tasks
4. Updates progress file when phase completes
5. Moves to next phase or prompts user for decision

## Development Phases

### Phase 1: Architecture Setup (Day 1)

**Goals**: Establish project structure and data schemas

**Tasks**:
- Define project directory structure
- Design code architecture pattern
- Create data schemas (Card, Relic, Event)
- Define system interfaces

**Calls**: `/sts-architecture`

**Completion Criteria**: `ARCHITECTURE.md` and data schemas created

---

### Phase 2: Card System (Day 2-4)

**Goals**: Implement complete card mechanics

**Tasks**:
- Design card data schema and initial card set
- Implement deck management (draw, discard, exhaust piles)
- Implement card play flow (selection → energy → effect → discard)
- Create card effect templates
- Generate card art assets

**Calls**:
- `/sts-data-design` (card schema)
- `/sts-card-system` (core implementation)
- `/sts-card-effect` (individual cards)
- `/sts-ai-art` (card art)

**Completion Criteria**: Basic card system functional, 10+ initial cards implemented

---

### Phase 3: Relic System (Day 3-5)

**Goals**: Implement relic mechanics with trigger system

**Tasks**:
- Design relic data schema and initial relic set
- Implement relic acquisition and management
- Create trigger timing system
- Implement relic effects
- Generate relic art assets

**Calls**:
- `/sts-data-design` (relic schema)
- `/sts-relic-system` (core implementation)
- `/sts-relic-effect` (individual relics)
- `/sts-ai-art` (relic art)

**Completion Criteria**: Relic system functional, 8+ initial relics implemented

---

### Phase 4: Map System (Day 4-6)

**Goals**: Implement procedurally generated map

**Tasks**:
- Design map generation algorithm
- Implement node types (battle, elite, event, shop, rest, boss)
- Create branching path logic
- Build map UI

**Calls**:
- `/sts-map-system` (core implementation)
- `/sts-map-node` (node implementations)

**Completion Criteria**: Map generation working, all node types functional

---

### Phase 5: Event System (Day 5-7)

**Goals**: Implement random event scenarios

**Tasks**:
- Design event data schema
- Create event pool and selection logic
- Write individual event scripts
- Build event UI (text, choices, outcomes)

**Calls**:
- `/sts-data-design` (event schema)
- `/sts-event-system` (core implementation)
- `/sts-event-script` (individual events)

**Completion Criteria**: Event system functional, 6+ events implemented

---

### Phase 6: UI System (Day 6-8)

**Goals**: Complete all game UI

**Tasks**:
- Main menu
- Combat UI (hand, energy, enemy, player status)
- Map UI
- Shop UI
- Reward UI
- Game result UI

**Calls**: `/sts-ui-system`

**Completion Criteria**: All UI screens functional

---

### Phase 7: Integration (Day 8-10)

**Goals**: Connect all systems, implement full game loop

**Tasks**:
- System integration testing
- Save/load system
- Game flow: Start → Map → Battle → Event → Boss → End
- Bug fixing

**Calls**: `/sts-integration`

**Completion Criteria**: Complete game loop playable

---

### Phase 8: TapTap Publishing (Day 9-11)

**Goals**: Platform integration and submission

**Tasks**:
- WebGL package optimization
- TapTap SDK integration
- Ad SDK integration (rewarded video)
- Prepare submission materials
- Submit for review

**Calls**: `/taptap-publisher`

**Completion Criteria**: Game submitted to TapTap

---

## Progress File Format

The `.sts-dev-state.json` tracks development state:

```json
{
  "project_name": "STS-like Roguelike",
  "start_date": "YYYY-MM-DD",
  "current_phase": 1,
  "phases": [
    {
      "id": 1,
      "name": "Architecture Setup",
      "status": "in_progress",
      "completed_tasks": [],
      "pending_tasks": ["architecture", "schemas", "interfaces"],
      "notes": ""
    }
  ],
  "last_updated": "YYYY-MM-DD HH:MM"
}
```

**Status values**: `pending`, `in_progress`, `completed`, `blocked`

## Key Behaviors

1. **Always read progress first**: Before any action, check `.sts-dev-state.json`
2. **Present options to user**: Don't auto-advance phases without confirmation
3. **Track dependencies**: Phase 2-5 can overlap, Phase 6 depends on 2-5, Phase 7 depends on 1-6, Phase 8 depends on 7
4. **Handle blockers**: If a task is blocked, note it and suggest alternatives
5. **Provide summaries**: After each phase, summarize what was accomplished

## Sub-Skill Invocation

Call sub-skills using the Skill tool:
- `/sts-architecture` → System architecture design
- `/sts-card-system` → Card system implementation
- `/sts-relic-system` → Relic system implementation
- `/sts-map-system` → Map generation system
- `/sts-event-system` → Event system implementation
- `/sts-ui-system` → UI implementation
- `/sts-integration` → System integration
- `/taptap-publisher` → Platform publishing

## User Interaction

- Start: "Let's begin development. We're at Phase 1: Architecture Setup."
- Resume: "Welcome back! Current phase: [X]. [Status summary]."
- Progress check: "Here's our progress: [list phases with status]"
- Phase complete: "Phase [X] complete! [Summary]. Ready for Phase [Y]?"
- Blocked: "Phase [X] is blocked: [reason]. Suggested action: [suggestion]"