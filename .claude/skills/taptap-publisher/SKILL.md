---
name: taptap-publisher
description: >
  Master skill for TapTap platform integration and publishing workflow. ALWAYS use this skill when the user mentions: publishing to TapTap ("上架TapTap", "TapTap发布"), SDK integration ("接入SDK", "TapTap SDK"), ad setup ("广告接入", "激励视频"), submission ("提交审核", "上架"), or Chinese mobile game market. Also trigger when discussing WebGL build optimization for TapTap, mini-game monetization, or TapTap developer portal. This skill coordinates taptap-sdk-integration, taptap-ad-integration, and taptap-submit sub-skills. Do NOT trigger for other platforms like Steam, App Store, or Google Play.
model: inherit
---
# TapTap Publisher

Master skill that orchestrates all TapTap platform integration tasks for Unity WebGL mini-game publishing.

## Platform Overview

**TapTap Mini-Game Requirements**:
- Target platform: Web-based (WebGL)
- Primary monetization: Rewarded video ads
- Distribution: TapTap app store
- Audience: Chinese market

## Workflow

### Step 1: Platform Research

Before integration, understand TapTap's requirements:
- Package size limits
- SDK versions required
- Ad placement policies
- Submission checklist

Read `references/taptap-requirements.md` for details.

### Step 2: SDK Integration (Sequential)

1. **Basic SDK Integration**
   - Initialize TapTap SDK
   - User login/authentication
   - Share functionality
   - Call `/taptap-sdk-integration`

2. **Ad SDK Integration**
   - Initialize ad SDK
   - Set up rewarded video ads
   - Configure ad placements
   - Call `/taptap-ad-integration`

### Step 3: Build Optimization

Before submission, optimize WebGL build:
- Asset compression
- Code stripping
- Texture compression
- Streaming assets

### Step 4: Submission Preparation

Prepare all submission materials:
- Game description (Chinese)
- Screenshots (5-10)
- App icon
- Category selection
- Age rating

Call `/taptap-submit`

### Step 5: Submit and Track

1. Submit game through TapTap developer portal
2. Track review status
3. Address any feedback
4. Publish upon approval

## Key Integration Points

### Rewarded Video Ad Placements

**Recommended placements for roguelike card game**:

| Placement | Trigger | Reward |
|-----------|---------|--------|
| Revive | After defeat | Continue with restored HP |
| Bonus Gold | After victory | Double gold reward |
| Free Relic | In shop | Get random relic |
| Heal | At rest node | Extra heal option |

### Unity WebGL Optimization Checklist

- [ ] Enable IL2CPP code stripping
- [ ] Use Addressables for streaming
- [ ] Compress textures (WebP format)
- [ ] Reduce audio quality if acceptable
- [ ] Remove unused assets
- [ ] Optimize shaders

## Sub-Skills

Call these skills for specific tasks:

- `/taptap-sdk-integration` - Basic TapTap SDK setup
- `/taptap-ad-integration` - Ad SDK and rewarded video
- `/taptap-submit` - Submission preparation and process

## Integration Code Structure

```
Assets/Scripts/Platform/TapTap/
├── TapTapManager.cs      // SDK initialization
├── TapTapAdManager.cs    // Ad loading and display
├── TapTapUserManager.cs  // User authentication
├── AdPlacementConfig.cs  // Ad placement definitions
└── AdRewardHandler.cs    // Reward processing
```

## Ad SDK Key Methods

```csharp
// Initialize
TapTapAdManager.Init();

// Load rewarded video
TapTapAdManager.LoadRewardedAd(placementId);

// Show rewarded video with callback
TapTapAdManager.ShowRewardedAd(placementId, (success, reward) => {
    if (success) {
        // Grant reward
        Player.GainGold(reward.amount);
    }
});

// Check ad availability
bool isReady = TapTapAdManager.IsRewardedAdReady(placementId);
```

## Submission Checklist

Before submitting, verify:

1. **Technical**:
   - [ ] WebGL build runs without errors
   - [ ] SDK properly initialized
   - [ ] Ads load and display correctly
   - [ ] Save/load works
   - [ ] No crashes on common scenarios

2. **Content**:
   - [ ] Game description (200-500 chars)
   - [ ] Screenshots showing gameplay
   - [ ] App icon (512x512)
   - [ ] No prohibited content

3. **Legal**:
   - [ ] Age rating appropriate
   - [ ] No copyrighted content without license
   - [ ] Privacy policy if collecting data

## Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| WebGL build too large | Enable compression, use Addressables |
| SDK init fails | Check app ID, ensure correct package |
| Ads not loading | Check placement IDs, test mode settings |
| Submission rejected | Review feedback, fix issues, resubmit |

## Developer Portal

Access TapTap developer portal at: https://developer.taptap.cn/

Key sections:
- Application management
- SDK documentation
- Ad configuration
- Review status
- Analytics dashboard