---
name: sts-card-system
description: >
  Implement the complete card system for Slay the Spire-like roguelike card games. ALWAYS use this skill when building deck management, card play flow, hand UI, or card effect execution. Trigger on phrases: "卡牌系统", "牌库管理", "抽牌", "弃牌", "手牌", "卡牌效果", "deck", "card", "draw", "discard". Also trigger when discussing deck building, card mechanics, or card game systems. Called by sts-dev-orchestrator during Phase 2. This skill implements DeckManager, CardController, CardEffectProcessor, and HandUI components.
model: inherit
---
# STS Card System

Implement the complete card mechanics for a Slay the Spire-like roguelike card game.

## System Components

### Core Modules

| Module | Responsibility |
|--------|----------------|
| DeckManager | Manage draw/discard/exhaust piles |
| CardController | Handle card selection and play |
| CardEffectProcessor | Execute card effects |
| HandUI | Display and interact with hand |
| CardFactory | Create card instances from data |

## Deck Flow

```
┌─────────────┐     Draw      ┌─────────────┐
│   Draw Pile │ ────────────→ │    Hand     │
│   (Deck)    │               │  (5 cards)  │
└─────────────┘               └─────────────┘
      ↑                              │
      │                         Play │
      │ Shuffle                     │
      │                              ↓
┌─────────────┐               ┌─────────────┐
│ Discard Pile│ ───────────── │ Exhaust Pile│
│  (Played)   │    End Turn   │  (Removed)  │
└─────────────┘               └─────────────┘
```

## Core Class Designs

### DeckManager

```csharp
public class DeckManager
{
    private List<CardData> drawPile;
    private List<CardData> discardPile;
    private List<CardData> exhaustPile;
    private List<CardData> hand;

    public void Initialize(List<CardData> deck);
    public List<CardData> DrawCards(int count);
    public void DiscardCard(CardData card);
    public void ExhaustCard(CardData card);
    public void ShuffleDiscardIntoDraw();
    public void EndTurnDiscardAll();
}
```

### CardController

```csharp
public class CardController
{
    public bool CanPlayCard(CardData card, int currentEnergy);
    public void PlayCard(CardData card, List<Enemy> targets);
    public void SelectCard(CardData card);
    public void CancelSelection();
}
```

### CardEffectProcessor

```csharp
public class CardEffectProcessor
{
    public void ProcessEffects(CardData card, CardContext context);

    private void ExecuteAttack(AttackEffect effect, CardContext context);
    private void ExecuteBlock(BlockEffect effect, CardContext context);
    private void ExecuteBuff(BuffEffect effect, CardContext context);
    private void ExecuteSpecial(SpecialEffect effect, CardContext context);
}
```

## Card Play Flow

### Play Sequence

1. Player selects card from hand
2. Check if playable (energy available, valid targets)
3. Highlight valid targets if needed
4. Player confirms target(s)
5. Deduct energy
6. Execute effects in order
7. Fire EventBus events
8. Move card to discard pile (or exhaust)

### Effect Execution Order

```
1. Pre-effects (trigger before main)
2. Main effects (attack/block/buff/debuff)
3. Post-effects (draw/discard/etc)
4. Trigger relics (OnCardPlayed)
```

## Card Types and Effects

### Attack Cards

Effects:
- Damage (single/multi-target/multi-hit)
- Apply debuff (Vulnerable/Weak)
- Special damage (piercing, scaling)

### Skill Cards

Effects:
- Block (flat/scaling)
- Draw cards
- Gain energy
- Heal
- Special utility

### Power Cards

Effects:
- Permanent stat buff (Strength/Dexterity)
- Ongoing effects (thorns, regen)
- Card modifiers

### Status Cards

Effects:
- Negative effects (Dazed, Burn)
- Cannot be played normally
- Auto-trigger or discard effect

## UI Components

### Hand Display

- 5 cards visible at once
- Card hover shows details
- Drag to play
- Energy indicator on each card
- Valid target highlighting

### Card Detail Panel

- Full card art
- Effect breakdown
- Upgrade preview (if applicable)

## Event Bus Integration

Fire these events:
- `OnCardDrawn(card)`
- `OnCardPlayed(card)`
- `OnCardDiscarded(card)`
- `OnCardExhausted(card)`
- `OnCardObtained(card)` (rewards)
- `OnDeckShuffled()`

## Sub-Skill Calls

- `/sts-data-design` - Get card schema and initial cards
- `/sts-card-effect` - Implement specific card effects
- `/sts-ai-art` - Generate card art

## Implementation Order

1. CardData class and loading
2. DeckManager with basic operations
3. CardController with play logic
4. CardEffectProcessor with effect types
5. HandUI with interaction
6. Connect to combat system
7. Implement initial cards via sts-card-effect

## References

Read `references/card-mechanics.md` for detailed mechanics.
Read `references/deck-flow-diagram.md` for visual flow.