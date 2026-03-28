---
name: taptap-sdk-integration
description: >
  Integrate TapTap base SDK for Unity WebGL mini-games. ALWAYS use this skill when: setting up TapTap initialization, implementing user login, or adding platform features. Trigger on phrases: "TapTap SDK", "SDK初始化", "TapTap登录", "平台集成", "初始化SDK", "用户登录", "TapTap平台", "TapTapManager". Called by taptap-publisher. Provides TapTapManager.cs, TapTapUserManager.cs implementation guidance.
model: inherit
---
# TapTap SDK Integration

Integrate the base TapTap SDK for Unity WebGL mini-game platform.

## SDK Overview

TapTap SDK provides:
- Platform initialization
- User authentication
- Share functionality
- Analytics hooks
- Platform-specific APIs

## Integration Steps

### Step 1: Get SDK Package

1. Download from TapTap developer portal
2. Import Unity package into project
3. Configure SDK settings

### Step 2: Initialize SDK

```csharp
// TapTapManager.cs
public class TapTapManager : MonoBehaviour
{
    private static TapTapManager instance;

    [SerializeField] private string appId;
    [SerializeField] private string appKey;

    public static bool IsInitialized { get; private set; }

    void Awake()
    {
        if (instance == null)
        {
            instance = this;
            InitializeSDK();
        }
    }

    void InitializeSDK()
    {
        // TapTap SDK initialization
        TapTapSDK.Init(appId, appKey, true);

        // Wait for initialization callback
        TapTapSDK.OnInitSuccess += OnInitSuccess;
        TapTapSDK.OnInitFail += OnInitFail;
    }

    void OnInitSuccess()
    {
        IsInitialized = true;
        Debug.Log("TapTap SDK initialized successfully");
    }

    void OnInitFail(string error)
    {
        IsInitialized = false;
        Debug.LogError($"TapTap SDK init failed: {error}");
    }
}
```

### Step 3: User Login (Optional)

```csharp
public void Login()
{
    if (!IsInitialized) return;

    TapTapUser.Login(OnLoginSuccess, OnLoginFail);
}

void OnLoginSuccess(TapTapUserInfo user)
{
    Debug.Log($"User logged in: {user.Name}");
    // Store user info for game
}

void OnLoginFail(string error)
{
    Debug.LogError($"Login failed: {error}");
}
```

### Step 4: Share Functionality

```csharp
public void ShareGame()
{
    if (!IsInitialized) return;

    TapTapShare.Share(
        title: "卡牌冒险",
        description: "Roguelike卡牌战斗游戏",
        imageUrl: "share_image_url"
    );
}
```

## Configuration

### App Settings

```
App ID: [From TapTap Developer Portal]
App Key: [From TapTap Developer Portal]
Server URL: [For backend features, if needed]
```

### Unity Settings

- WebGL template: TapTap-compatible
- Scripting backend: IL2CPP
- Target platform: WebGL

## Directory Structure

```
Assets/Scripts/Platform/TapTap/
├── TapTapManager.cs      // Main SDK handler
├── TapTapUserManager.cs  // User authentication
├── TapTapShareHandler.cs // Share functionality
└── TapTapConfig.cs       // Configuration constants
```

## Error Handling

| Error Code | Meaning | Solution |
|------------|---------|----------|
| InitFailed | SDK init failed | Check app ID/key |
| NetworkError | Connection issue | Retry with delay |
| AuthFailed | Login failed | Show retry option |
| InvalidConfig | Wrong settings | Verify portal config |

## Testing Checklist

- [ ] SDK initializes on game start
- [ ] Init success callback received
- [ ] Login works (if implemented)
- [ ] Share works (if implemented)
- [ ] No crashes from SDK calls
- [ ] WebGL build includes SDK

## References

Read `references/sdk-usage.md` for complete API reference.