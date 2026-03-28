# Visual Style Guide

Flat cartoon style guidelines for game art assets.

## Core Style Definition

**Flat Cartoon Style**:
- Simple, clean shapes with minimal detail
- Bold, saturated colors
- No gradients or complex shading
- Clear silhouettes
- Playful, game-friendly aesthetic

## Color Palette

### Primary Colors

| Color | Hex | Usage |
|-------|-----|-------|
| Red | #E74C3C | Attack cards, damage, danger |
| Blue | #3498DB | Skill cards, block, defense |
| Purple | #9B59B6 | Power cards, magic effects |
| Green | #27AE60 | Health, healing, buffs |
| Gold | #F1C40F | Rewards, special, rare |
| Orange | #E67E22 | Energy, fire, power |

### Neutral Colors

| Color | Hex | Usage |
|-------|-----|-------|
| White | #FFFFFF | Backgrounds, highlights |
| Light Gray | #ECF0F1 | Secondary backgrounds |
| Dark Gray | #2C3E50 | Text, outlines |
| Black | #1A1A1A | Deep shadows, emphasis |

### Rarity Colors

| Rarity | Glow Color |
|--------|------------|
| Common | #95A5A6 (gray) |
| Uncommon | #3498DB (blue) |
| Rare | #F1C40F (gold) |
| Legendary | #9B59B6 (purple) |

## Shape Language

### Basic Shapes

- **Circles**: Friendly, soft, healing, energy
- **Squares**: Stable, solid, defense, block
- **Triangles**: Dynamic, aggressive, attack, danger

### Complexity Level

```
Level 1 (Simple):     Level 2 (Medium):    Level 3 (Detailed):
   ⬤                      🔮                     🏰
 Circle              Circle + Glow          Complex silhouette
```

**Recommended**: Level 1-2 for most game assets

## Composition Rules

### Centered Subject
```
┌─────────────────┐
│                 │
│     [SUBJECT]   │  ← Subject in center
│                 │
└─────────────────┘
```

### No Perspective
- All subjects facing forward
- Flat, 2D appearance
- No 3D depth or vanishing points

### Minimal Background
- White or light gray background
- No scenery or environment
- Focus entirely on subject

## Typography (for UI)

### Card Text
- Font: Bold sans-serif
- Size: 14-18pt for descriptions
- Color: Dark gray (#2C3E50)
- Shadow: Optional light drop shadow

### Title Text
- Font: Bold display font
- Size: 24-36pt for titles
- Color: Matches card type (red/blue/purple)

## Animation Style

### Recommended Effects
- **Pulse**: Gentle scale animation for important elements
- **Glow**: Soft glow for magical items
- **Shake**: Quick shake for damage
- **Float**: Gentle bobbing for idle states

### Avoid
- Complex 3D rotations
- Particle systems with many particles
- Realistic physics simulations

## Asset Specifications

### Card Art
- Resolution: 512x682 pixels (3:4 ratio)
- Format: PNG with transparency
- Style: Flat cartoon, centered subject

### Relic Icons
- Resolution: 512x512 pixels (1:1 ratio)
- Format: PNG with transparency
- Style: Flat cartoon, simple icon

### UI Elements
- Resolution: Variable (power of 2)
- Format: PNG with transparency
- Style: Consistent with overall theme

## Examples of Good vs Bad

### ✅ Good
- Simple sword with clean lines
- Clear silhouette
- 2-3 colors max
- Centered on white background

### ❌ Bad
- Detailed realistic sword
- Complex shading and reflections
- Too many colors
- Background with perspective

## Quality Checklist

Before finalizing any asset:
- [ ] Simple, recognizable silhouette
- [ ] 2-3 colors maximum
- [ ] Centered composition
- [ ] White/light background
- [ ] No complex details
- [ ] Works at small size (64x64)
- [ ] Consistent with other assets