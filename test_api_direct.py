#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/ubuntu/.openclaw/workspace/projects/coze-bilibili-api')

from main import run_yt_dlp_api
import json

COOKIE = "enable_web_push=DISABLE; buvid4=71FEB3FD-87FC-F887-AC65-58C71B35E8D445617-024071412-6YSoObwaWXbSTqdeOvjWHg%3D%3D; DedeUserID=1983776166; DedeUserID__ckMd5=84988b4708a82a0a; SESSDATA=96abedd0%2C1789137924%2Ca7e8f%2A32CjBMeUI0wURiHL1YwmdHG9xOg_5QTon5nMAru602bVtKPUhftbHoGGrL19Y5J4Tm_OASVnR4aXRReXp5YUJLS1gxM1VLeDNlYU42YmJhV0FIMFlnZUhKVkFjczZheGRDSFpmOFMwSnlaNHNHTWRpaThYdkhoaTE0cDd3TzhjalhWbG0yWTl4Y253IIEC; bili_jct=9c2cc71b9117c844cab32f59c251cacc"

URL = "https://space.bilibili.com/20713882"

print("Testing run_yt_dlp_api...")
output = run_yt_dlp_api(URL, COOKIE, ["--playlist-end", "2"])

if not output:
    print("ERROR: No output")
    sys.exit(1)

if isinstance(output, dict) and "error" in output:
    print(f"ERROR: {output['error']}")
    sys.exit(1)

print(f"Output lines: {len(output.strip().split(chr(10)))}")
for i, line in enumerate(output.strip().split('\n')):
    if line.strip():
        try:
            d = json.loads(line)
            print(f"\n--- Entry {i+1} ---")
            print(f"ID: {d.get('id', 'N/A')}")
            print(f"Title: {d.get('title', 'N/A')[:50] if d.get('title') else 'EMPTY'}")
            print(f"Thumbnail: {d.get('thumbnail', 'N/A')[:60] if d.get('thumbnail') else 'EMPTY'}")
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Line: {line[:100]}...")
