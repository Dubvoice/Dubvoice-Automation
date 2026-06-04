#!/usr/bin/env python3
"""DubVoice Local API — end-to-end test / example client.

Starts from the running DubVoice "Webhook" server, submits a generation job,
polls until it finishes and downloads the result.

Usage:
    python test_webhook.py --key YOUR_KEY
    python test_webhook.py --key YOUR_KEY --type video --prompt "ocean waves"
    python test_webhook.py --key YOUR_KEY --type tts --text "Hello world" --voice <voice_id>

Requirements:
    pip install requests
"""
from __future__ import annotations

import argparse
import sys
import time

try:
    import requests
except ImportError:
    sys.exit("This script needs 'requests'.  Install it with:  pip install requests")


def main() -> int:
    ap = argparse.ArgumentParser(description="Test the DubVoice local REST API.")
    ap.add_argument("--key", required=True, help="X-API-Key from the Webhook tab")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--type", choices=["image", "video", "tts"], default="image")
    ap.add_argument("--prompt", default="a red sports car at sunset")
    ap.add_argument("--text", default="Hello from DubVoice!", help="text for --type tts")
    ap.add_argument("--voice", default="", help="voice_id for --type tts")
    ap.add_argument("--model", default="", help="override the default model")
    ap.add_argument("--ratio", default="16:9")
    ap.add_argument("--out", default="", help="output file (default: result.<ext>)")
    ap.add_argument("--timeout", type=int, default=900)
    args = ap.parse_args()

    base = f"http://{args.host}:{args.port}"
    headers = {"X-API-Key": args.key, "Content-Type": "application/json"}

    # ---- health check ----
    try:
        h = requests.get(f"{base}/api/health", timeout=5).json()
    except Exception as e:  # noqa: BLE001
        return _fail(f"Cannot reach {base} — is the Webhook server running?  ({e})")
    print(f"✓ Server is up: {h}")

    # ---- build the request ----
    if args.type == "image":
        endpoint = "/api/image/generate"
        body = {"prompt": args.prompt, "aspect_ratio": args.ratio}
        if args.model:
            body["model"] = args.model
        default_ext = ".png"
    elif args.type == "video":
        endpoint = "/api/video/generate"
        body = {"prompt": args.prompt, "aspect_ratio": args.ratio}
        if args.model:
            body["model"] = args.model
        default_ext = ".mp4"
    else:  # tts
        endpoint = "/api/tts/generate"
        body = {"text": args.text}
        if args.voice:
            body["voice_id"] = args.voice
        if args.model:
            body["model"] = args.model
        default_ext = ".mp3"

    print(f"→ POST {endpoint}  {body}")
    r = requests.post(base + endpoint, headers=headers, json=body, timeout=30)
    if r.status_code >= 400:
        return _fail(f"Request rejected ({r.status_code}): {r.text}")
    task_id = r.json().get("task_id")
    if not task_id:
        return _fail(f"No task_id in response: {r.text}")
    print(f"✓ Job submitted. task_id = {task_id}")

    # ---- poll ----
    start = time.time()
    last = None
    while True:
        if time.time() - start > args.timeout:
            return _fail("Timed out waiting for the job to finish.")
        s = requests.get(f"{base}/api/status/{task_id}", headers=headers, timeout=15).json()
        status, prog = s.get("status"), s.get("progress")
        line = f"  status={status} progress={prog}%"
        if line != last:
            print(line)
            last = line
        if status == "completed":
            break
        if status == "failed":
            return _fail(f"Job failed: {s.get('error')}")
        time.sleep(4)

    # ---- download ----
    out = args.out or f"result{default_ext}"
    data = requests.get(f"{base}/api/file/{task_id}", headers=headers, timeout=120).content
    with open(out, "wb") as f:
        f.write(data)
    print(f"✓ Done. Saved {len(data):,} bytes to {out}")
    return 0


def _fail(msg: str) -> int:
    print(f"✗ {msg}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
