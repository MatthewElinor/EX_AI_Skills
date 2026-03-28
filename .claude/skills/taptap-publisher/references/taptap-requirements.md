# TapTap Mini-Game Platform Requirements

This document summarizes TapTap's technical requirements for mini-game publishing.

## Package Requirements

### WebGL Build
- **Recommended max size**: 20-30 MB (compressed)
- **Maximum allowed**: 50 MB (may affect discoverability)
- **Format**: WebGL build (Unity WebGL template)

### Performance
- **Target FPS**: 30+ on mid-range devices
- **Memory**: Keep under 200 MB RAM usage
- **Loading time**: Under 10 seconds initial load

## SDK Requirements

### TapTap SDK
- Minimum version: Check developer portal for current version
- Required features:
  - Initialization on game start
  - User login (optional but recommended)
  - Share functionality

### TapTap Ad SDK
- Required for monetization
- Rewarded video ads supported
- Interstitial ads (optional)
- Banner ads (not recommended for game UX)

## Ad Placement Guidelines

### Rewarded Video Ads

**Allowed placements**:
- After game failure (revive option)
- For bonus rewards (double gold, free item)
- At player request (optional rewards)

**NOT allowed**:
- Forced ads during gameplay
- Ads blocking critical UI
- Ads before player can interact

**Frequency recommendations**:
- Limit to 3-5 ads per session
- Minimum 30 seconds between ads
- Never interrupt active gameplay

### Rewarded Content Guidelines

Reward types allowed:
- Extra gold/currency
- Free items (cards, relics)
- Revive/continue option
- Bonus content

Reward types NOT allowed:
- Gameplay advantages that make game too easy
- Pay-to-win mechanics
- Exclusive content only via ads

## Content Guidelines

### Allowed Content
- Fantasy/sci-fi themes
- Card games, puzzle games
- Roguelike mechanics
- Anime/cartoon art styles

### Prohibited Content
- Gambling simulation (real money gambling)
- Explicit violence
- Sexual content
- Political content
- Real-money transactions (use TapTap's payment system)

### Age Rating
- Most card games: 12+ or 16+
- Check TapTap's rating guidelines

## Submission Requirements

### Required Materials

1. **Game Description** (200-500 Chinese characters)
   - Game genre and features
   - How to play briefly
   - Unique selling points

2. **Screenshots** (5-10 images)
   - Main gameplay screens
   - Key features shown
   - 1280x720 or similar resolution

3. **App Icon**
   - 512x512 PNG
   - Simple, recognizable
   - No text-heavy designs

4. **Category Selection**
   - Card game → "策略" or "卡牌"
   - Roguelike → "Roguelike" subcategory

### Optional Materials
- Trailer video (30-60 seconds)
- Update log
- Developer contact info

## Review Process

### Timeline
- Initial review: 1-3 business days
- Additional review if changes needed: 1-2 days
- Total: 3-7 days typically

### Common Rejection Reasons
1. Technical issues (crashes, performance)
2. Content violations
3. Missing required materials
4. Ad placement violations
5. Copyright concerns

### After Approval
- Game goes live within 24 hours
- Monitor analytics for issues
- Respond to user feedback
- Plan updates based on feedback

## Developer Portal Access

### Registration
1. Register at developer.taptap.cn
2. Complete developer profile
3. Create new application
4. Get App ID and SDK keys

### SDK Documentation
Available at: developer.taptap.cn/document

### Support
- Developer forums: forums.taptap.cn
- Email support: Check portal for contact

## Testing Before Submission

### Pre-Submission Checklist

1. **Functionality**
   - [ ] Full game loop playable
   - [ ] No crashes in 30+ minutes of play
   - [ ] Save/load works correctly
   - [ ] All UI screens accessible

2. **SDK Integration**
   - [ ] SDK initializes without errors
   - [ ] Ads load successfully
   - [ ] Ad rewards granted correctly
   - [ ] No ad-related crashes

3. **Performance**
   - [ ] FPS stays above 30
   - [ ] Memory under 200 MB
   - [ ] Load time under 10 seconds

4. **Content**
   - [ ] All text in Chinese
   - [ ] No prohibited content
   - [ ] Age-appropriate