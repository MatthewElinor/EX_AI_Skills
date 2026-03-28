---
name: sts-ai-art
description: >
  Generate AI art prompts and manage art assets for Slay the Spire-like roguelike card games. ALWAYS use this skill when generating card art, relic icons, UI elements, or character art via AI tools like Midjourney or Stable Diffusion. Trigger on phrases: "AI美术", "生成图片", "卡牌美术", "遗物美术", "美术资源", "AI生成", "Midjourney", "Stable Diffusion", "扁平卡通", "game art". Called by sts-card-system and sts-relic-system. Provides optimized prompts for flat cartoon style.
model: inherit
---
# STS AI Art Generator

Manage AI art generation workflow for game assets with optimized prompts for flat cartoon style.

## Art Style: Flat Cartoon

**Core Style Keywords**:
- flat design
- cartoon style
- simple shapes
- bold colors
- minimal details
- centered composition
- clean lines
- game asset
- white background

**Color Palette**:
- Primary: Bright saturated colors
- Accent: Contrasting highlights
- Background: White or light gray
- Shadows: Minimal, flat style

## Prompt Templates

### Card Art Prompts

Read `templates/card-art-prompts.md` for full templates.

**Basic Template**:
```
[SUBJECT], flat cartoon style game card art, simple shapes, bold colors, centered composition, minimal details, white background, vibrant colors, clean lines, no perspective, game asset style --ar 3:4
```

**Attack Card**:
```
[CHARACTER/WEAPON] attacking, dynamic pose, flat cartoon style game card art, simple shapes, bold [COLOR] and [SECONDARY COLOR], centered composition, action lines, minimal details, white background, game asset --ar 3:4
```

**Skill Card**:
```
[EFFECT/SYMBOL], flat cartoon style game card art, simple geometric shapes, bold [COLOR], centered composition, glowing effect, minimal details, white background, game UI asset --ar 3:4
```

**Power Card**:
```
[POWER SYMBOL/ICON], flat cartoon style game card art, circular design, bold [COLOR] with glow, centered composition, mystical feel, minimal details, white background --ar 3:4
```

### Relic Art Prompts

Read `templates/relic-art-prompts.md` for full templates.

**Basic Template**:
```
[RELIC OBJECT], flat cartoon style game relic icon, simple geometric shapes, bold colors, centered composition, minimal details, white background, glowing effect, game UI asset --ar 1:1
```

**Examples**:
- Burning Blood: `red crystal drop, flat cartoon style game relic icon, glowing red, centered composition, minimal details, white background --ar 1:1`
- Anchor: `golden anchor, flat cartoon style game relic icon, bold brown and gold, centered composition, minimal details, white background --ar 1:1`
- Shuriken: `three pointed shuriken, flat cartoon style game relic icon, silver metallic, centered composition, minimal details, white background --ar 1:1`

### UI Element Prompts

**Energy Orb**:
```
energy orb, glowing sphere, flat cartoon style game UI element, gradient blue to white, centered composition, minimal details, game asset --ar 1:1
```

**Block Shield**:
```
shield icon, flat cartoon style game UI element, bold blue, centered composition, minimal details, white background --ar 1:1
```

**Menu Button**:
```
game button frame, flat cartoon style UI element, rounded rectangle, bold [COLOR], minimal details --ar 4:1
```

## Art Generation Workflow

### Step 1: Prepare Prompt List

For each asset type:
1. List all needed assets
2. Determine subject and colors
3. Apply template
4. Save prompts to file

### Step 2: Generate with AI Tool

Using Midjourney:
```
/imagine [prompt]
```

Using Stable Diffusion:
```
[prompt] -s 50 -W 512 -H 512
```

### Step 3: Select and Export

1. Generate 4-8 variants per prompt
2. Select best match for style
3. Export at needed resolution
4. Clean up edges if needed

### Step 4: Organize Assets

Naming convention:
```
card_[id]_art.png      // Card artwork
relic_[id]_icon.png    // Relic icon
ui_[component].png     // UI element
```

Storage:
```
Assets/Art/
├── Cards/
│   ├── card_strike_art.png
│   ├── card_defend_art.png
│   └── ...
├── Relics/
│   ├── relic_burning_blood.png
│   ├── relic_anchor.png
│   └── ...
├── UI/
│   ├── ui_energy_orb.png
│   ├── ui_block_icon.png
│   └── ...
```

## Quality Checklist

After generation, verify:
- [ ] Style matches flat cartoon aesthetic
- [ ] Colors are bold and vibrant
- [ ] Composition is centered
- [ ] Background is clean (white/light)
- [ ] Details are minimal but recognizable
- [ ] Size is appropriate for use
- [ ] No unwanted artifacts

## Batch Generation

For efficient generation:
1. Create prompt list file
2. Generate in batches (10-20 at once)
3. Review all outputs together
4. Select and organize
5. Clean/refine if needed

## Color Assignments

### Card Colors by Type

| Type | Primary Color | Accent |
|------|---------------|--------|
| Attack | Red/Orange | Dark red |
| Skill | Blue/Cyan | Dark blue |
| Power | Purple/Magenta | Gold |
| Status | Gray/Dark | None |

### Rarity Colors

| Rarity | Border Glow |
|--------|-------------|
| Common | White/Silver |
| Uncommon | Blue |
| Rare | Gold |
| Legendary | Purple |

## Templates

Read:
- `templates/card-art-prompts.md` - Full card prompt list
- `templates/relic-art-prompts.md` - Full relic prompt list
- `templates/style-guide.md` - Visual style reference