#!/usr/bin/env python3
"""ikunimage - 双模型图生图 / 图片编辑器（ikun 专用渠道）。

支持的模型：
  - gemini-3.1-flash-image-preview (NanoBanana2) - 稳定，¥0.125/次
  - gpt-image-2 - OpenAI 图像模型，¥0.06/次，可能不稳定

上传本地图片 + 文字描述，AI 理解图片和文字后生成新图片。

用法:
    # 首次配置
    python generate_ikun_edit.py --setup

    # 单张编辑（默认 NanoBanana2）
    python generate_ikun_edit.py --input photo.jpg --prompt "将背景改为雪景" \
                                 [--aspect-ratio 1:1] [--output edited.png] [--retry 3]

    # 使用 gpt-image-2
    python generate_ikun_edit.py --model gpt-image-2 --input photo.jpg --prompt "..." --retry 10

    # 使用 gpt-image-2 透明背景（直出可用 PNG）
    python generate_ikun_edit.py --model gpt-image-2 --transparent --input ui.png --prompt "修改颜色"

    # 并发批量编辑
    python generate_ikun_edit.py --batch tasks.json [--workers 2] [--retry 3]
"""

import argparse
import base64
import json
import mimetypes
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

try:
    import httpx
except ImportError:
    print("错误: 需要 httpx 库，请执行: pip install httpx", file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------------------
# 渠道配置（单渠道：ikun）
# ---------------------------------------------------------------------------

BASE_URL = "https://api.ikuncode.cc"
CONFIG_DIR = Path.home() / ".ikunimage"
CONFIG_FILE = CONFIG_DIR / "config.json"

# 模型配置（与 generate_ikun.py 共用）
MODELS = {
    "gemini-3.1-flash-image-preview": {
        "name": "NanoBanana2",
        "api_type": "gemini",
        "path": "/v1beta/models/gemini-3.1-flash-image-preview:generateContent",
        "price": 0.125,  # ¥/次
        "timeout_default": 600,
        "timeout_map": {"1K": 360, "2K": 600, "4K": 1200},
        "stable": True,
        "transparent_supported": False,  # 不支持透明背景
        "description": "Gemini Flash 图像模型，稳定可靠，白底输出",
    },
    "gpt-image-2": {
        "name": "GPT-Image-2",
        "api_type": "openai",
        # OpenAI 图生图用 /v1/images/edits 接口
        "path": "/v1/images/edits",
        "price": 0.06,  # ¥/次
        "timeout_default": 900,
        "timeout_map": {"1K": 540, "2K": 900, "4K": 1800},
        "stable": False,
        "transparent_supported": True,  # 支持透明背景直出
        "description": "OpenAI 图像模型，价格便宜，支持透明背景直出",
    },
}

DEFAULT_MODEL = "gemini-3.1-flash-image-preview"

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------

VALID_ASPECT_RATIOS = [
    "1:1", "16:9", "9:16", "4:3", "3:4",
    "3:2", "2:3", "21:9", "5:4", "4:5",
]

SUPPORTED_IMAGE_FORMATS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

MAX_IMAGE_SIZE_MB = 4

# OpenAI images/edits 支持的尺寸
OPENAI_SIZE_MAP = {
    "1:1": "1024x1024",
    "16:9": "1536x1024",
    "9:16": "1024x1536",
}

RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504, 524}

_print_lock = threading.Lock()


def _safe_print(msg, *, file=None):
    """线程安全的打印。"""
    with _print_lock:
        print(msg, file=file or sys.stdout, flush=True)


# ---------------------------------------------------------------------------
# API Key 管理（与 generate_ikun.py 共用配置文件）
# ---------------------------------------------------------------------------

def _load_config() -> dict:
    """从配置文件加载配置，文件不存在或解析失败返回空 dict。"""
    if not CONFIG_FILE.exists():
        return {}
    try:
        return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _save_config(config: dict) -> None:
    """将配置写入配置文件。"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(
        json.dumps(config, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def resolve_api_key(cli_key: str | None = None) -> str:
    """按优先级解析 API Key。"""
    if cli_key:
        return cli_key

    env_key = os.environ.get("IKUN_API_KEY", "").strip()
    if env_key:
        return env_key

    config = _load_config()
    file_key = config.get("api_key", "").strip()
    if file_key:
        return file_key

    print(
        "错误: 未找到 API Key。请通过以下方式之一配置：\n"
        "  1. 运行 python generate_ikun.py --setup 进行交互式配置\n"
        f"  2. 手动创建 {CONFIG_FILE}，内容: {{\"api_key\": \"sk-xxx\"}}\n"
        "  3. 设置环境变量 IKUN_API_KEY=***\n"
        "  4. 使用 --api-key sk-xxx 命令行参数",
        file=sys.stderr,
    )
    sys.exit(1)


def run_setup() -> None:
    """交互式引导创建配置文件。"""
    print("=" * 50)
    print("  ikunimage 配置向导")
    print("=" * 50)
    print(f"\n配置文件位置: {CONFIG_FILE}\n")

    existing = _load_config()
    if existing.get("api_key"):
        masked = existing["api_key"][:6] + "..." + existing["api_key"][-4:]
        print(f"当前已有 API Key: {masked}")
        confirm = input("是否覆盖？(y/N): ").strip().lower()
        if confirm not in ("y", "yes"):
            print("已取消。")
            return

    api_key = input("请输入 ikun API Key (sk-xxx): ").strip()
    if not api_key:
        print("错误: API Key 不能为空。", file=sys.stderr)
        sys.exit(1)

    # 询问默认模型
    print("\n选择默认模型：")
    for model_id, info in MODELS.items():
        stable_mark = "✓ 稳定" if info["stable"] else "⚠ 可能不稳定"
        print(f"  1. {model_id} ({info['name']}) - ¥{info['price']}/次 {stable_mark}")
    
    model_choice = input("默认模型 (1/2, 默认 1): ").strip()
    if model_choice == "2":
        default_model = "gpt-image-2"
    else:
        default_model = "gemini-3.1-flash-image-preview"

    config = existing.copy()
    config["api_key"] = api_key
    config["default_model"] = default_model
    _save_config(config)

    print(f"\n配置已保存到 {CONFIG_FILE}")
    print(f"默认模型: {default_model}")
    print("现在可以使用 ikunimage 编辑图片了。")


# ---------------------------------------------------------------------------
# 图片读取
# ---------------------------------------------------------------------------

def read_image_as_base64(image_path: str) -> tuple[str, str, bytes]:
    """读取本地图片并返回 (base64_data, mime_type, raw_bytes)。

    Raises:
        FileNotFoundError: 图片不存在
        ValueError: 格式不支持或文件过大
    """
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"图片文件不存在: {image_path}")

    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_IMAGE_FORMATS:
        raise ValueError(
            f"不支持的图片格式 '{suffix}'，支持: {', '.join(sorted(SUPPORTED_IMAGE_FORMATS))}"
        )

    size_mb = path.stat().st_size / (1024 * 1024)
    if size_mb > MAX_IMAGE_SIZE_MB:
        raise ValueError(f"图片过大 ({size_mb:.1f}MB)，建议 < {MAX_IMAGE_SIZE_MB}MB")

    mime_type, _ = mimetypes.guess_type(str(path))
    if not mime_type or not mime_type.startswith("image/"):
        mime_type = "image/jpeg"

    raw = path.read_bytes()
    b64 = base64.b64encode(raw).decode("utf-8")
    return b64, mime_type, raw


# ---------------------------------------------------------------------------
# Gemini API（JSON 格式，内嵌 base64 图片）
# ---------------------------------------------------------------------------

# 透明背景提示词模板（与 generate_ikun.py 共用）
TRANSPARENT_BG_PROMPT_SUFFIX = (
    "transparent background PNG, alpha channel, clean edges, "
    "ready-to-use UI asset, no background color"
)

WHITE_BG_PROMPT_SUFFIX = (
    "white background, suitable for background removal processing"
)


def build_edit_payload_gemini(
    prompt: str,
    image_b64: str,
    mime_type: str,
    aspect_ratio: str,
) -> dict:
    """构建 Gemini 图生图请求 payload。"""
    return {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": image_b64,
                        }
                    },
                ]
            }
        ],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {
                "aspectRatio": aspect_ratio,
            },
        },
    }


def request_gemini(payload: dict, timeout: int, api_key: str, model_path: str) -> httpx.Response:
    """发送 Gemini API 请求。"""
    url = BASE_URL + model_path
    with httpx.Client(timeout=timeout) as client:
        return client.post(
            url,
            json=payload,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
        )


def parse_response_gemini(resp: httpx.Response) -> tuple[bytes, str]:
    """解析 Gemini API 响应。"""
    data = resp.json()
    try:
        parts = data["candidates"][0]["content"]["parts"]
        image_part = next(p for p in parts if "inlineData" in p)
        b64_data = image_part["inlineData"]["data"]
        mime_type = image_part["inlineData"].get("mimeType", "image/png")
    except (KeyError, IndexError, StopIteration):
        snippet = json.dumps(data, indent=2, ensure_ascii=False)[:500]
        raise ValueError(f"API 响应中未找到图片数据: {snippet}")
    
    return base64.b64decode(b64_data), mime_type


# ---------------------------------------------------------------------------
# OpenAI API（multipart/form-data 格式）
# ---------------------------------------------------------------------------

def request_openai_edit(
    prompt: str,
    image_bytes: bytes,
    timeout: int,
    api_key: str,
    model: str,
    size: str = "1024x1024",
    transparent: bool = False,
) -> httpx.Response:
    """发送 OpenAI images/edits API 请求（multipart/form-data）。
    
    Args:
        transparent: 是否生成透明背景。True: 自动添加透明提示词。
    """
    url = BASE_URL + "/v1/images/edits"
    
    # 根据背景模式调整提示词
    if transparent:
        final_prompt = f"{prompt}, {TRANSPARENT_BG_PROMPT_SUFFIX}"
    else:
        final_prompt = f"{prompt}, {WHITE_BG_PROMPT_SUFFIX}"
    
    # multipart/form-data 格式
    files = {
        "image": ("image.png", image_bytes, "image/png"),
    }
    data = {
        "model": model,
        "prompt": final_prompt,
        "n": 1,
        "size": size,
        "response_format": "b64_json",
    }
    
    with httpx.Client(timeout=timeout) as client:
        return client.post(
            url,
            files=files,
            data=data,
            headers={
                "Authorization": f"Bearer {api_key}",
            },
        )


def parse_response_openai(resp: httpx.Response) -> tuple[bytes, str]:
    """解析 OpenAI images/edits API 响应。"""
    data = resp.json()
    try:
        image_data = data["data"][0]
        b64_data = image_data["b64_json"]
        mime_type = "image/png"
    except (KeyError, IndexError):
        snippet = json.dumps(data, indent=2, ensure_ascii=False)[:500]
        raise ValueError(f"API 响应中未找到图片数据: {snippet}")
    
    return base64.b64decode(b64_data), mime_type


# ---------------------------------------------------------------------------
# 核心编辑逻辑（线程安全）
# ---------------------------------------------------------------------------

def _edit_core(
    input_image: str,
    prompt: str,
    api_key: str,
    model: str = DEFAULT_MODEL,
    aspect_ratio: str = "1:1",
    output_path: str = "output.png",
    max_retries: int = 3,
    task_label: str = "",
    transparent: bool = False,
) -> dict:
    """编辑单张图片，返回结果字典。线程安全，不会调用 sys.exit。

    Args:
        transparent: 是否生成透明背景。仅 gpt-image-2 支持。
    
    返回:
        成功: {"success": True, "path": str, "size_kb": float, "elapsed": float, "model": str, "transparent": bool}
        失败: {"success": False, "error": str}
    """
    model_info = MODELS.get(model)
    if not model_info:
        return {"success": False, "error": f"未知模型: {model}"}
    
    # 检查透明背景支持
    if transparent and not model_info.get("transparent_supported", False):
        _safe_print(f"[ikunimage] 警告: 模型 {model_info['name']} 不支持透明背景，将输出白色背景")
        transparent = False
    
    tag = f"[ikunimage 编辑{' ' + task_label if task_label else ''}]"

    # 读取输入图片
    try:
        image_b64, mime_type, image_bytes = read_image_as_base64(input_image)
        _safe_print(f"{tag} 输入图片: {input_image} ({mime_type})")
    except (FileNotFoundError, ValueError) as e:
        return {"success": False, "error": str(e)}

    timeout = model_info["timeout_default"]
    stable_mark = "✓" if model_info["stable"] else "⚠"
    bg_mode = "透明背景" if transparent else "白色背景"
    
    _safe_print(f"{tag} 正在编辑图片...")
    _safe_print(f"{tag}   模型: {model_info['name']} ({stable_mark}) | ¥{model_info['price']}/次 | {bg_mode}")
    _safe_print(f"{tag}   编辑描述: {prompt[:80]}{'...' if len(prompt) > 80 else ''}")
    _safe_print(f"{tag}   宽高比: {aspect_ratio} | 超时: {timeout}s")

    resp = None
    last_error = None

    for attempt in range(max_retries + 1):
        if attempt > 0:
            delay = min(2 ** attempt, 60)
            _safe_print(f"{tag} 第 {attempt}/{max_retries} 次重试，等待 {delay}s ...")
            time.sleep(delay)

        _safe_print(f"{tag} 发送请求 (attempt {attempt + 1})")

        t0 = time.time()
        try:
            if model_info["api_type"] == "gemini":
                payload = build_edit_payload_gemini(prompt, image_b64, mime_type, aspect_ratio)
                resp = request_gemini(payload, timeout, api_key, model_info["path"])
            else:  # openai
                size = OPENAI_SIZE_MAP.get(aspect_ratio, "1024x1024")
                resp = request_openai_edit(prompt, image_bytes, timeout, api_key, model, size, transparent)
        except httpx.TimeoutException:
            last_error = "请求超时"
            _safe_print(f"{tag} 请求超时 ({timeout}s)", file=sys.stderr)
            continue
        except httpx.ConnectError as e:
            last_error = f"连接失败: {e}"
            _safe_print(f"{tag} 连接失败: {e}", file=sys.stderr)
            continue

        elapsed = time.time() - t0

        if resp.status_code == 200:
            _safe_print(f"{tag} API 响应成功，耗时 {elapsed:.1f}s")
            break

        if resp.status_code in RETRYABLE_STATUS_CODES and attempt < max_retries:
            try:
                err_body = resp.json()
                err_msg = err_body.get("error", {}).get("message", resp.text[:200])
            except Exception:
                err_msg = resp.text[:200]
            last_error = f"HTTP {resp.status_code}: {err_msg}"
            _safe_print(f"{tag} 收到 {resp.status_code}，将重试", file=sys.stderr)
            continue

        # 不可重试
        try:
            err_detail = json.dumps(resp.json(), indent=2, ensure_ascii=False)[:500]
        except Exception:
            err_detail = resp.text[:500]
        return {"success": False, "error": f"HTTP {resp.status_code}: {err_detail}"}
    else:
        return {"success": False, "error": f"重试 {max_retries} 次仍然失败。最后错误: {last_error}"}

    # 解析响应
    try:
        if model_info["api_type"] == "gemini":
            image_out_bytes, out_mime = parse_response_gemini(resp)
        else:
            image_out_bytes, out_mime = parse_response_openai(resp)
    except ValueError as e:
        return {"success": False, "error": str(e)}

    out = Path(output_path)
    if not out.suffix:
        ext = out_mime.split("/")[-1].replace("jpeg", "jpg")
        out = out.with_suffix(f".{ext}")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(image_out_bytes)

    size_kb = len(image_out_bytes) / 1024
    _safe_print(f"{tag} 编辑完成，大小 {size_kb:.0f}KB -> {out}")

    return {
        "success": True,
        "path": str(out),
        "size_kb": round(size_kb, 1),
        "elapsed": round(elapsed, 1),
        "model": model,
        "model_name": model_info["name"],
        "price": model_info["price"],
        "transparent": transparent,
    }


# ---------------------------------------------------------------------------
# 单张编辑（CLI 单图模式）
# ---------------------------------------------------------------------------

def edit(
    input_image: str,
    prompt: str,
    api_key: str,
    model: str = DEFAULT_MODEL,
    aspect_ratio: str = "1:1",
    output_path: str = "output.png",
    max_retries: int = 3,
    transparent: bool = False,
) -> str:
    """单张编辑入口，失败时 sys.exit(1)。
    
    Args:
        transparent: 是否生成透明背景。仅 gpt-image-2 支持。
    """
    result = _edit_core(
        input_image=input_image,
        prompt=prompt,
        api_key=api_key,
        model=model,
        aspect_ratio=aspect_ratio,
        output_path=output_path,
        max_retries=max_retries,
        transparent=transparent,
    )
    if not result["success"]:
        print(f"错误: {result['error']}", file=sys.stderr)
        sys.exit(1)
    return result["path"]


# ---------------------------------------------------------------------------
# 并发批量编辑
# ---------------------------------------------------------------------------

def edit_batch(
    tasks: list,
    api_key: str,
    model: str = DEFAULT_MODEL,
    workers: int = 0,
    max_retries: int = 3,
    transparent: bool = False,
) -> list:
    """并发批量编辑多张图片。

    参数:
        tasks: 任务列表，每个元素为 dict:
            {
                "input": str,            # 必填，输入图片路径
                "prompt": str,           # 必填，编辑描述
                "aspect_ratio": str,     # 可选，默认 "1:1"
                "output": str,           # 必填，输出路径
                "model": str,            # 可选，默认使用全局 model
                "transparent": bool,     # 可选，默认使用全局 transparent
            }
        api_key: ikun API Key
        model: 默认模型
        workers: 并发数。0 = 自动（默认 2）
        max_retries: 每个任务的最大重试次数
        transparent: 默认透明背景设置。仅 gpt-image-2 支持

    返回:
        结果列表，每个元素含 "index" 字段。
    """
    num_tasks = len(tasks)

    if workers <= 0:
        workers = min(num_tasks, 2)
    workers = max(1, min(workers, num_tasks))

    model_info = MODELS.get(model, MODELS[DEFAULT_MODEL])
    bg_mode = "透明背景" if transparent else "白色背景"
    print(f"[ikunimage 批量编辑] 共 {num_tasks} 个任务，并发数: {workers}")
    print(f"[ikunimage 批量编辑] 模型: {model_info['name']} (¥{model_info['price']}/次) | {bg_mode}")

    t_start = time.time()
    results = [None] * num_tasks

    def _run_task(index: int, task: dict) -> tuple:
        task_model = task.get("model", model)
        task_transparent = task.get("transparent", transparent)
        result = _edit_core(
            input_image=task["input"],
            prompt=task["prompt"],
            api_key=api_key,
            model=task_model,
            aspect_ratio=task.get("aspect_ratio", "1:1"),
            output_path=task["output"],
            max_retries=max_retries,
            task_label=f"#{index + 1}",
            transparent=task_transparent,
        )
        result["index"] = index
        return index, result

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(_run_task, i, t): i
            for i, t in enumerate(tasks)
        }
        for future in as_completed(futures):
            idx, result = future.result()
            results[idx] = result
            status = "OK" if result["success"] else "FAIL"
            _safe_print(f"[ikunimage 批量编辑] 任务 #{idx + 1} {status}")

    t_total = time.time() - t_start
    ok = sum(1 for r in results if r and r["success"])
    print(f"\n[ikunimage 批量编辑] 全部完成: {ok}/{num_tasks} 成功，总耗时 {t_total:.1f}s")

    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="ikunimage - 双模型图生图 / 图片编辑器（ikun 渠道）",
        epilog="上传本地图片 + 文字描述，AI 生成编辑后的新图片。",
    )

    # 配置子命令
    parser.add_argument(
        "--setup", action="store_true",
        help="交互式引导创建配置文件",
    )

    # API Key
    parser.add_argument(
        "--api-key", default=None,
        help="API Key（优先级高于环境变量和配置文件）",
    )

    # 模型选择
    parser.add_argument(
        "--model", "-m", default=None,
        choices=list(MODELS.keys()),
        help=f"图像编辑模型（默认: {DEFAULT_MODEL}）\n"
             "  gemini-3.1-flash-image-preview: NanoBanana2, 稳定 ¥0.125/次\n"
             "  gpt-image-2: OpenAI, ¥0.06/次, 可能不稳定需要更多重试",
    )

    # 单图模式参数
    parser.add_argument(
        "--input", "-i", default=None,
        help="输入图片路径（单图模式，必填）",
    )
    parser.add_argument(
        "--prompt", "-p", default=None,
        help="编辑描述提示词（单图模式，必填）",
    )
    parser.add_argument(
        "--aspect-ratio", "-ar", default="1:1",
        choices=VALID_ASPECT_RATIOS, help="输出图片宽高比（默认: 1:1）",
    )
    parser.add_argument(
        "--output", "-o", default="output.png",
        help="输出文件路径",
    )

    # 批量模式参数
    parser.add_argument(
        "--batch", "-b", default=None, metavar="JSON_FILE",
        help="批量任务 JSON 文件路径（与 --input/--prompt 互斥）",
    )
    parser.add_argument(
        "--workers", "-w", type=int, default=0,
        help="并发 worker 数（默认: 自动）",
    )

    # 通用参数
    parser.add_argument(
        "--retry", "-r", type=int, default=None,
        choices=range(0, 21), metavar="0-20",
        help="每个任务的最大重试次数（默认: Gemini 3次, gpt-image-2 10次）",
    )
    
    # 背景模式（仅 gpt-image-2 支持）
    parser.add_argument(
        "--transparent", "-t", action="store_true",
        help="生成透明背景 PNG（仅 gpt-image-2 支持，NanoBanana2 会输出白底）",
    )
    parser.add_argument(
        "--bg", choices=["transparent", "white"], default=None,
        help="背景模式选择: transparent（透明）或 white（白色，后续可去背景）",
    )

    args = parser.parse_args()

    # --setup 模式
    if args.setup:
        run_setup()
        return

    # 互斥检查
    if args.batch and (args.input or args.prompt):
        parser.error("--batch 和 --input/--prompt 不能同时使用")
    if not args.batch and not (args.input and args.prompt):
        parser.error("必须指定 --input 和 --prompt（单图模式）或 --batch（批量模式），或使用 --setup 配置")

    # 解析 API Key
    api_key = resolve_api_key(args.api_key)

    # 解析模型
    model = args.model
    if not model:
        config = _load_config()
        model = config.get("default_model", DEFAULT_MODEL)
    
    model_info = MODELS.get(model, MODELS[DEFAULT_MODEL])
    
    # 解析重试次数
    max_retries = args.retry
    if max_retries is None:
        max_retries = 3 if model_info["stable"] else 10

    # 解析透明背景参数
    transparent = False
    if args.transparent:
        transparent = True
    if args.bg == "transparent":
        transparent = True
    elif args.bg == "white":
        transparent = False
    
    bg_mode = "透明背景" if transparent else "白色背景"
    bg_support = "✓支持" if model_info.get("transparent_supported") else "不支持"
    print(f"[ikunimage 编辑] 模型: {model_info['name']} ({model})")
    print(f"[ikunimage 编辑] 价格: ¥{model_info['price']}/次 | 重试: {max_retries}次 | 背景: {bg_mode} ({bg_support})")

    if args.batch:
        # 批量模式
        batch_path = Path(args.batch)
        if not batch_path.exists():
            print(f"错误: 批量任务文件不存在: {batch_path}", file=sys.stderr)
            sys.exit(1)

        try:
            tasks = json.loads(batch_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"错误: 解析批量任务文件失败: {e}", file=sys.stderr)
            sys.exit(1)

        if not isinstance(tasks, list) or not tasks:
            print("错误: 批量任务文件必须是非空 JSON 数组", file=sys.stderr)
            sys.exit(1)

        for i, t in enumerate(tasks):
            if "input" not in t or "prompt" not in t or "output" not in t:
                print(f"错误: 任务 #{i + 1} 缺少必填字段 input/prompt/output", file=sys.stderr)
                sys.exit(1)

        results = edit_batch(
            tasks=tasks,
            api_key=api_key,
            model=model,
            workers=args.workers,
            max_retries=max_retries,
            transparent=transparent,
        )

        # 输出汇总 JSON
        print("\n" + json.dumps(results, indent=2, ensure_ascii=False))

        if any(not r["success"] for r in results if r):
            sys.exit(1)
    else:
        # 单图模式
        edit(
            input_image=args.input,
            prompt=args.prompt,
            api_key=api_key,
            model=model,
            aspect_ratio=args.aspect_ratio,
            output_path=args.output,
            max_retries=max_retries,
            transparent=transparent,
        )


if __name__ == "__main__":
    main()