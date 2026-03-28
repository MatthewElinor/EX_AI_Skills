---
name: taptap-ad-integration
description: >
  Integrate TapTap ad SDK for rewarded video ads in Unity WebGL mini-games. ALWAYS use this skill when: setting up ad placements, implementing rewarded video ads, or connecting ads to game rewards. Trigger on phrases: "TapTap广告", "激励视频", "广告SDK", "广告接入", "rewarded video", "广告变现", "视频广告", "广告位", "TapTapAdManager". Called by taptap-publisher. Provides TapTapAdManager.cs and AdRewardHandler.cs implementation guidance.
model: inherit
---
# TapTap Ad Integration

Integrate TapTap ad SDK for rewarded video ads monetization.

## Ad Types

| Type | Description | Recommendation |
|------|-------------|----------------|
| Rewarded Video | User chooses to watch, gets reward | ✅ Primary monetization |
| Interstitial | Full-screen ad between screens | ⚠️ Use sparingly |
| Banner | Small ad at screen edge | ❌ Not recommended |

## Ad Placements for Roguelike

### Recommended Placements

| Placement | Trigger | Reward | User Value |
|-----------|---------|--------|------------|
| Revive | After defeat | Continue with 50% HP | High |
| Bonus Gold | After victory | Double gold reward | Medium |
| Free Relic | In shop | Random relic (no cost) | High |
| Heal Option | At rest node | Extra heal option | Medium |

### Placement IDs

Configure in TapTap portal:
- `revive_ad` - Revive after death
- `bonus_gold_ad` - Double victory gold
- `shop_relic_ad` - Free shop relic
- `rest_heal_ad` - Extra rest heal

## Core Implementation

### TapTapAdManager

```csharp
public class TapTapAdManager : MonoBehaviour
{
    private static TapTapAdManager instance;

    // Placement IDs
    private const string REVIVE_PLACEMENT = "revive_ad";
    private const string BONUS_GOLD_PLACEMENT = "bonus_gold_ad";
    private const string SHOP_RELIC_PLACEMENT = "shop_relic_ad";

    // Ad state
    private Dictionary<string, bool> adReadyStatus;

    public static TapTapAdManager Instance => instance;

    void Awake()
    {
        instance = this;
        InitializeAdSDK();
    }

    void InitializeAdSDK()
    {
        TapTapAd.Init();

        // Register callbacks
        TapTapAd.OnAdLoaded += OnAdLoaded;
        TapTapAd.OnAdFailedToLoad += OnAdFailedToLoad;
        TapTapAd.OnAdShowed += OnAdShowed;
        TapTapAd.OnAdClosed += OnAdClosed;
        TapTapAd.OnAdRewarded += OnAdRewarded;

        // Pre-load ads
        PreloadAds();
    }

    void PreloadAds()
    {
        LoadRewardedAd(REVIVE_PLACEMENT);
        LoadRewardedAd(BONUS_GOLD_PLACEMENT);
        LoadRewardedAd(SHOP_RELIC_PLACEMENT);
    }

    public void LoadRewardedAd(string placementId)
    {
        TapTapAd.LoadRewardedVideo(placementId);
    }

    public bool IsAdReady(string placementId)
    {
        return adReadyStatus.ContainsKey(placementId) && adReadyStatus[placementId];
    }

    public void ShowRewardedAd(string placementId, Action<bool> onComplete)
    {
        if (!IsAdReady(placementId))
        {
            onComplete?.Invoke(false);
            return;
        }

        currentAdCallback = onComplete;
        TapTapAd.ShowRewardedVideo(placementId);
    }
}
```

### Ad Reward Handler

```csharp
public class AdRewardHandler
{
    public void HandleReviveReward()
    {
        // Player continues with 50% HP
        GameManager.Instance.Player.HP = GameManager.Instance.Player.MaxHP * 0.5f;
        // Return to battle or give extra turn
    }

    public void HandleBonusGoldReward(int baseGold)
    {
        // Double the gold reward
        GameManager.Instance.Player.Gold += baseGold;
    }

    public void HandleFreeRelicReward()
    {
        // Grant random relic from pool
        var relic = RelicManager.GetRandomRelic();
        GameManager.Instance.Player.AddRelic(relic);
    }

    public void HandleHealReward()
    {
        // Extra heal at rest node
        GameManager.Instance.Player.HP += 15;
    }
}
```

## UI Integration

### Show Ad Option

```csharp
// In defeat screen
public void ShowReviveOption()
{
    if (TapTapAdManager.Instance.IsAdReady(REVIVE_PLACEMENT))
    {
        reviveButton.SetActive(true);
        reviveButton.onClick.AddListener(() => {
            TapTapAdManager.Instance.ShowRewardedAd(REVIVE_PLACEMENT, (success) => {
                if (success) {
                    AdRewardHandler.HandleReviveReward();
                    // Continue game
                } else {
                    // Show game over
                }
            });
        });
    }
    else
    {
        reviveButton.SetActive(false);
    }
}
```

## Ad Frequency Limits

Prevent ad fatigue:
- Maximum 5 ads per session
- Minimum 30 seconds between ads
- No ads in first 2 minutes
- No consecutive same placements

```csharp
private int adsWatchedThisSession = 0;
private float lastAdTime = 0;

public bool CanShowAd()
{
    if (adsWatchedThisSession >= 5) return false;
    if (Time.time - lastAdTime < 30f) return false;
    if (Time.time < 120f) return false; // First 2 minutes
    return true;
}
```

## Callback Handling

```csharp
void OnAdLoaded(string placementId)
{
    adReadyStatus[placementId] = true;
    Debug.Log($"Ad loaded: {placementId}");
}

void OnAdFailedToLoad(string placementId, string error)
{
    adReadyStatus[placementId] = false;
    Debug.LogError($"Ad load failed: {placementId} - {error}");
}

void OnAdShowed(string placementId)
{
    // Pause game audio
    AudioManager.PauseAll();
    lastAdTime = Time.time;
}

void OnAdClosed(string placementId)
{
    // Resume game audio
    AudioManager.ResumeAll();
    // Preload next ad
    LoadRewardedAd(placementId);
}

void OnAdRewarded(string placementId, TapTapReward reward)
{
    adsWatchedThisSession++;
    // Process reward based on placement
    ProcessReward(placementId, reward);
}
```

## Testing Checklist

- [ ] Ads load successfully
- [ ] Ad ready status correct
- [ ] Ads display without crashes
- [ ] Rewards granted after ad
- [ ] Ad frequency limits work
- [ ] Audio pauses during ad
- [ ] Game resumes after ad
- [ ] Failed ads handled gracefully