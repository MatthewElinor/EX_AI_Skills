---
name: sts-ui-system
description: >
  Implement game UI screens and components for Slay the Spire-like roguelike card games. ALWAYS use this skill when building menus, combat UI, map UI, shop UI, reward UI, or any visual interface. Trigger on phrases: "UI系统", "游戏界面", "战斗UI", "菜单", "商店UI", "主菜单", "HUD", "UI设计", "界面开发". Called by sts-dev-orchestrator during Phase 6. Implements MainMenu, CombatUI, MapUI, ShopUI, EventUI, RewardUI, GameOverUI screens.
model: inherit
---
# STS UI System

Implement all game UI screens and components for a Slay the Spire-like roguelike card game.

## UI Screens

| Screen | Purpose | Key Components |
|--------|---------|----------------|
| MainMenu | Game entry | Title, Start, Settings, Exit |
| Combat | Main gameplay | Hand, Energy, Enemy, Player status |
| Map | Path selection | Nodes, Current position, Paths |
| Shop | Buy/remove items | Card offers, Relic offers, Remove |
| Event | Event encounter | Art, Text, Options |
| Reward | Post-combat loot | Card choices, Gold, Relic |
| GameOver | End game | Result, Stats, Restart |
| Settings | Configuration | Audio, Display, Language |

## Core Components

### UIManager

```csharp
public class UIManager : MonoBehaviour
{
    private Dictionary<ScreenType, UIScreen> screens;
    private UIScreen currentScreen;

    public void ShowScreen(ScreenType type);
    public void HideScreen(ScreenType type);
    public UIScreen GetScreen(ScreenType type);
}
```

### UIScreen Base

```csharp
public abstract class UIScreen : MonoBehaviour
{
    public virtual void Show();
    public virtual void Hide();
    public virtual void Refresh();
}
```

## Screen Details

### MainMenu

```
┌─────────────────────────────┐
│         GAME TITLE          │
│                             │
│     [  开始游戏  ]           │
│     [  设置    ]             │
│     [  退出    ]             │
│                             │
│       Version 1.0           │
└─────────────────────────────┘
```

Components:
- GameLogo (title art)
- StartButton
- SettingsButton
- ExitButton
- VersionText

### Combat UI

```
┌──────────────────────────────────────────┐
│  [Enemy Display Area]                    │
│  Enemy HP: ████████░░ 80/100             │
│                                          │
│  [Player Status]                         │
│  HP: ██████████ 70/80    Block: ███ 12   │
│  Energy: ●●● 3/3                         │
│                                          │
│  ────────────────────────────────────    │
│  [Hand Area - 5 cards displayed]         │
│                                          │
│              [结束回合]                   │
└──────────────────────────────────────────┘
```

Components:
- EnemyDisplay (sprite, HP bar, intents)
- PlayerStatus (HP, block, energy orb)
- HandDisplay (5 card slots)
- EndTurnButton
- DeckCountIndicator (draw/discard piles)
- RelicDisplayStrip

### Map UI

```
┌──────────────────────────────────────┐
│  Floor 1                              │
│                                       │
│    ⭐ ─── ⚔ ─── 👹 ─── 👿             │
│         │                              │
│         ❓                              │
│                                       │
│  [Current: ⚔ Battle Node]             │
│  [Enter Node]                         │
└──────────────────────────────────────┘
```

Components:
- MapVisualization (nodes, paths)
- FloorIndicator
- CurrentNodeHighlight
- NodeDetailPanel
- EnterButton

### Shop UI

```
┌────────────────────────────────────────┐
│  💰 Gold: 150                          │
│                                        │
│  === CARDS ===                         │
│  [Card 1] [Card 2] [Card 3]            │
│  50g      75g      100g                │
│                                        │
│  === RELICS ===                        │
│  [Relic 1]                             │
│  150g                                  │
│                                        │
│  === SERVICES ===                      │
│  [Remove Card] 75g                     │
│                                        │
│  [Leave Shop]                          │
└────────────────────────────────────────┘
```

Components:
- GoldDisplay
- CardOfferRow (3 cards with prices)
- RelicOfferRow
- RemoveCardButton
- LeaveButton

### Event UI

```
┌────────────────────────────────────────┐
│  [Event Art/Image]                     │
│                                        │
│  === 大鱼 ===                          │
│  你在河边遇到一条巨大的鱼...            │
│                                        │
│  [支付50金币获得稀有卡牌]               │
│  [支付30金币获得普通遗物]               │
│  [离开]                                │
└────────────────────────────────────────┘
```

Components:
- EventArtDisplay
- EventTitle
- EventDescription
- OptionButtons (2-4)

### Reward UI

```
┌────────────────────────────────────────┐
│  === 战斗胜利 ===                       │
│                                        │
│  获得 25 金币                          │
│                                        │
│  选择一张卡牌:                          │
│  [Card 1] [Card 2] [Card 3] [Skip]     │
│                                        │
│  获得遗物: [Relic]                      │
│                                        │
│  [继续]                                │
└────────────────────────────────────────┘
```

Components:
- VictoryTitle
- GoldDisplay
- CardChoiceRow (3 cards + skip)
- RelicDisplay
- ContinueButton

## UI Animation Effects

- Card hover: scale up, glow
- Card drag: follow cursor, dim others
- Button hover: color shift
- Screen transition: fade/slide
- Damage numbers: float and fade
- Block indicator: shield pulse

## UI Art Style

Flat cartoon style:
- Bold colors, simple shapes
- Rounded buttons
- Card borders with slight glow
- Energy orb with gradient
- Clean typography

## Implementation Order

1. UIManager singleton
2. UIScreen base class
3. MainMenu screen
4. Combat UI components
5. HandDisplay with interaction
6. Map screen
7. Shop screen
8. Event screen
9. Reward screen
10. GameOver screen
11. Settings screen
12. Transitions and animations