#!/usr/bin/env python3
"""
测试 B 站 UP 主信息爬取
"""

import json
import subprocess
import tempfile
import os
from typing import Dict, List, Any, Optional

COOKIE = """enable_web_push=DISABLE; buvid4=71FEB3FD-87FC-F887-AC65-58C71B35E8D445617-024071412-6YSoObwaWXbSTqdeOvjWHg%3D%3D; DedeUserID=1983776166; DedeUserID__ckMd5=84988b4708a82a0a; enable_feed_channel=ENABLE; fingerprint=46ab6655ff3d6b75daba84eb51dae5ee; buvid_fp_plain=undefined; buvid_fp=46ab6655ff3d6b75daba84eb51dae5ee; header_theme_version=OPEN; theme-tip-show=SHOWED; theme-avatar-tip-show=SHOWED; buvid3=447D77B5-4D8F-E0B3-04FC-048D89AFC3B522684infoc; b_nut=1752497422; _uuid=6A299E1010-A7510-10F51-EAED-1ADE4E1BE4A208796infoc; rpdid=0zbfAHNU5C|fN5EjplC|2vx|3w1UUv6r; hit-dyn-v2=1; CURRENT_BLACKGAP=0; LIVE_BUVID=AUTO6317682855142671; bmg_af_switch=1; bmg_src_def_domain=i0.hdslb.com; b-user-id=cca7134c-16b3-46a6-da50-4bdfabb25d30; home_feed_column=4; SESSDATA=96abedd0%2C1789137924%2Ca7e8f%2A32CjBMeUI0wURiHL1YwmdHG9xOg_5QTon5nMAru602bVtKPUhftbHoGGrL19Y5J4Tm_OASVnR4aXRReXp5YUJLS1gxM1VLeDNlYU42YmJhV0FIMFlnZUhKVkFjczZheGRDSFpmOFMwSnlaNHNHTWRpaThYdkhoaTE0cDd3TzhjalhWbG0yWTl4Y253IIEC; bili_jct=9c2cc71b9117c844cab32f59c251cacc; sid=7l3uoaq0; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzM5MDk4NzEsImlhdCI6MTc3MzY1MDYxMSwicGx0IjotMX0.rqZBAYZv4e6BvSuKEKoppOUEtrbBM8zBnuejpquQ3JY; bili_ticket_expires=1773909811; PVID=4; browser_resolution=1080-632; CURRENT_QUALITY=120; CURRENT_FNVAL=4048; bp_t_offset_1983776166=1180990735088877568; b_lsid=3C4CC9FF_19CFFE8BDCE"""

UPLOADER_URL = "https://space.bilibili.com/20713882?spm_id_from=333.337.0.0"

YT_DLP_PATH = "/home/ubuntu/.openclaw/workspace/projects/xhs-crawler/venv/bin/yt-dlp"


def convert_cookie_to_netscape(cookie_str: str) -> str:
    """将浏览器 Cookie 字符串转换为 Netscape 格式"""
    lines = ["# Netscape HTTP Cookie File"]
    domain = ".bilibili.com"
    
    cookies = cookie_str.split(';')
    for cookie in cookies:
        cookie = cookie.strip()
        if '=' in cookie:
            key, value = cookie.split('=', 1)
            key = key.strip()
            value = value.strip()
            # Netscape 格式：domain flag path secure expiry name value
            lines.append(f"{domain}\tTRUE\t/\tFALSE\t0\t{key}\t{value}")
    
    return '\n'.join(lines)


def run_yt_dlp(url: str, cookie: Optional[str] = None, extra_args: List[str] = None) -> Optional[str]:
    """执行 yt-dlp 命令并返回 JSON 结果"""
    cmd = [
        YT_DLP_PATH,
        "--dump-json",
        "--no-download",
    ]
    
    # 处理 Cookie（转换为 Netscape 格式）
    if cookie:
        temp_cookie = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
        netscape_cookie = convert_cookie_to_netscape(cookie)
        temp_cookie.write(netscape_cookie)
        temp_cookie.close()
        cmd.extend(["--cookies", temp_cookie.name])
    
    if extra_args:
        cmd.extend(extra_args)
    
    cmd.append(url)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        # 清理临时 Cookie 文件
        if cookie:
            try:
                os.unlink(temp_cookie.name)
            except:
                pass
        
        if result.returncode != 0:
            print(f"❌ yt-dlp error: {result.stderr}")
            return None
        
        return result.stdout
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def get_uploader_info(uploader_url: str, cookie: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """获取 UP 主信息"""
    print(f"\n{'='*60}")
    print(f"📊 获取 UP 主信息：{uploader_url}")
    print(f"{'='*60}")
    
    # 获取主页信息（播放列表模式）
    output = run_yt_dlp(uploader_url, cookie, ["--playlist-end", "1"])
    
    if not output:
        return None
    
    try:
        data = json.loads(output.strip())
        uploader_info = {
            "uploader": data.get("uploader", ""),
            "uploader_id": data.get("uploader_id", ""),
            "channel": data.get("channel", ""),
            "channel_id": data.get("channel_id", ""),
            "url": uploader_url,
            "total_videos": data.get("playlist_count", 0),
        }
        
        print(f"✅ UP 主：{uploader_info['uploader']}")
        print(f"✅ UID: {uploader_info['uploader_id']}")
        print(f"✅ 视频总数：{uploader_info['total_videos']}")
        
        return uploader_info
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        return None


def get_uploader_videos(uploader_url: str, cookie: Optional[str] = None, max_videos: int = 10) -> List[Dict[str, Any]]:
    """获取 UP 主视频列表"""
    print(f"\n{'='*60}")
    print(f"📹 获取视频列表（最多 {max_videos} 个）")
    print(f"{'='*60}")
    
    # 不使用 flat-playlist，直接获取完整信息
    output = run_yt_dlp(uploader_url, cookie, ["--playlist-end", str(max_videos)])
    
    if not output:
        return []
    
    # 解析多行 JSON
    videos = []
    for line in output.strip().split('\n'):
        if line.strip():
            try:
                entry = json.loads(line)
                # 跳过播放列表信息行（没有 id 字段）
                if not entry.get("id"):
                    continue
                video = {
                    "index": len(videos) + 1,
                    "title": entry.get("title", ""),
                    "id": entry.get("id", ""),
                    "url": f"https://www.bilibili.com/video/{entry.get('id', '')}",
                    "duration": entry.get("duration", 0),
                    "thumbnail": entry.get("thumbnail", ""),
                }
                videos.append(video)
                print(f"  {video['index']}. {video['title'][:50]}...")
            except json.JSONDecodeError:
                continue
    
    print(f"\n✅ 共获取 {len(videos)} 个视频")
    return videos


def get_video_detail(video_url: str, cookie: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """获取视频详细信息"""
    output = run_yt_dlp(video_url, cookie)
    
    if not output:
        return None
    
    try:
        data = json.loads(output.strip())
        detail = {
            "title": data.get("title", ""),
            "id": data.get("id", ""),
            "url": data.get("webpage_url", ""),
            "duration": data.get("duration", 0),
            "duration_string": data.get("duration_string", ""),
            "upload_date": data.get("upload_date", ""),
            "description": data.get("description", ""),
            "view_count": data.get("view_count", 0),
            "like_count": data.get("like_count", 0),
            "comment_count": data.get("comment_count", 0),
            "thumbnail": data.get("thumbnail", ""),
            "uploader": data.get("uploader", ""),
            "uploader_id": data.get("uploader_id", ""),
            "tags": data.get("tags", []),
            "formats_count": len(data.get("formats", [])),
        }
        return detail
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        return None


def crawl_uploader(uploader_url: str, cookie: Optional[str] = None, max_videos: int = 5, get_details: bool = True) -> Dict[str, Any]:
    """完整爬取 UP 主信息和视频详情"""
    result = {
        "uploader_info": None,
        "videos": [],
        "video_details": [],
    }
    
    # 1. 获取 UP 主信息
    uploader_info = get_uploader_info(uploader_url, cookie)
    if not uploader_info:
        print("❌ 获取 UP 主信息失败")
        return result
    
    result["uploader_info"] = uploader_info
    
    # 2. 获取视频列表
    videos = get_uploader_videos(uploader_url, cookie, max_videos)
    if not videos:
        print("❌ 获取视频列表失败")
        return result
    
    result["videos"] = videos
    
    # 3. 获取视频详情
    if get_details:
        print(f"\n{'='*60}")
        print(f"📖 获取视频详情...")
        print(f"{'='*60}")
        
        for i, video in enumerate(videos, 1):
            print(f"\n[{i}/{len(videos)}] 获取视频详情：{video['title'][:30]}...")
            detail = get_video_detail(video["url"], cookie)
            
            if detail:
                result["video_details"].append(detail)
                print(f"  ✅ 播放量：{detail['view_count']:,}")
                print(f"  ✅ 点赞数：{detail['like_count']:,}")
                print(f"  ✅ 时长：{detail['duration_string']}")
            else:
                print(f"  ❌ 获取失败")
    
    return result


def main():
    """主函数"""
    print(f"🚀 开始爬取 B 站 UP 主数据")
    print(f"📍 URL: {UPLOADER_URL}")
    
    # 爬取数据
    result = crawl_uploader(
        uploader_url=UPLOADER_URL,
        cookie=COOKIE,
        max_videos=3,  # 获取 3 个视频
        get_details=True  # 获取详情
    )
    
    # 输出 JSON 结果
    print(f"\n{'='*60}")
    print(f"📊 JSON 输出")
    print(f"{'='*60}")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
