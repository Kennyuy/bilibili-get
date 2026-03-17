#!/usr/bin/env python3
"""
B 站 UP 主主页信息爬取脚本
获取博主信息 + 视频列表 + 视频详情
"""

import json
import subprocess
import tempfile
import os
from pathlib import Path
from typing import Dict, List, Any, Optional

# 配置
COOKIE_FILE = "/home/ubuntu/.openclaw/workspace/projects/coze-bilibili-api/bilibili_cookies.txt"
YT_DLP_PATH = "/home/ubuntu/.openclaw/workspace/projects/xhs-crawler/venv/bin/yt-dlp"


def run_yt_dlp(url: str, cookie_file: str = COOKIE_FILE, extra_args: List[str] = None) -> Optional[Dict]:
    """执行 yt-dlp 命令并返回 JSON 结果"""
    cmd = [
        YT_DLP_PATH,
        "--dump-json",
        "--no-download",
    ]
    
    if cookie_file and os.path.exists(cookie_file):
        cmd.extend(["--cookies", cookie_file])
    
    if extra_args:
        cmd.extend(extra_args)
    
    cmd.append(url)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            print(f"❌ yt-dlp error: {result.stderr}")
            return None
        
        return json.loads(result.stdout)
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def get_uploader_info(uploader_url: str) -> Optional[Dict[str, Any]]:
    """
    获取 UP 主主页信息
    
    Args:
        uploader_url: UP 主主页 URL，如 https://space.bilibili.com/1815948385
    
    Returns:
        UP 主信息字典
    """
    print(f"\n{'='*60}")
    print(f"📊 获取 UP 主信息：{uploader_url}")
    print(f"{'='*60}")
    
    # 获取主页信息（播放列表模式）
    data = run_yt_dlp(uploader_url, extra_args=["--playlist-end", "1"])
    
    if not data:
        return None
    
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


def get_uploader_videos(uploader_url: str, max_videos: int = 10) -> List[Dict[str, Any]]:
    """
    获取 UP 主视频列表
    
    Args:
        uploader_url: UP 主主页 URL
        max_videos: 最大获取视频数量
    
    Returns:
        视频列表
    """
    print(f"\n{'='*60}")
    print(f"📹 获取视频列表（最多 {max_videos} 个）")
    print(f"{'='*60}")
    
    # 使用播放列表模式获取多个视频（返回多行 JSON）
    cmd = [
        YT_DLP_PATH,
        "--dump-json",
        "--no-download",
        "--flat-playlist",
        "--playlist-end", str(max_videos),
    ]
    
    if os.path.exists(COOKIE_FILE):
        cmd.extend(["--cookies", COOKIE_FILE])
    
    cmd.append(uploader_url)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            print(f"❌ yt-dlp error: {result.stderr}")
            return []
        
        # 解析多行 JSON
        videos = []
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                try:
                    entry = json.loads(line)
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
    except Exception as e:
        print(f"❌ Error: {e}")
        return []
    
    for i, entry in enumerate(entries, 1):
        if not entry:
            continue
        
        video = {
            "index": i,
            "title": entry.get("title", ""),
            "id": entry.get("id", ""),
            "url": f"https://www.bilibili.com/video/{entry.get('id', '')}",
            "duration": entry.get("duration", 0),
            "thumbnail": entry.get("thumbnail", ""),
        }
        videos.append(video)
        print(f"  {i}. {video['title'][:50]}...")
    
    print(f"\n✅ 共获取 {len(videos)} 个视频")
    return videos


def get_video_detail(video_url: str) -> Optional[Dict[str, Any]]:
    """
    获取视频详细信息
    
    Args:
        video_url: 视频 URL
    
    Returns:
        视频详细信息
    """
    data = run_yt_dlp(video_url)
    
    if not data:
        return None
    
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


def crawl_uploader(uploader_url: str, max_videos: int = 5, get_details: bool = True) -> Dict[str, Any]:
    """
    完整爬取 UP 主信息和视频详情
    
    Args:
        uploader_url: UP 主主页 URL
        max_videos: 最大获取视频数量
        get_details: 是否获取视频详情
    
    Returns:
        完整数据
    """
    result = {
        "uploader_info": None,
        "videos": [],
        "video_details": [],
    }
    
    # 1. 获取 UP 主信息
    uploader_info = get_uploader_info(uploader_url)
    if not uploader_info:
        print("❌ 获取 UP 主信息失败")
        return result
    
    result["uploader_info"] = uploader_info
    
    # 2. 获取视频列表
    videos = get_uploader_videos(uploader_url, max_videos)
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
            detail = get_video_detail(video["url"])
            
            if detail:
                result["video_details"].append(detail)
                print(f"  ✅ 播放量：{detail['view_count']:,}")
                print(f"  ✅ 点赞数：{detail['like_count']:,}")
                print(f"  ✅ 时长：{detail['duration_string']}")
            else:
                print(f"  ❌ 获取失败")
    
    return result


def save_result(result: Dict, output_file: str = "bilibili_result.json"):
    """保存结果到 JSON 文件"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\n📁 结果已保存到：{output_file}")


def main():
    """主函数"""
    # 示例：马克的技术工作坊
    uploader_url = "https://space.bilibili.com/1815948385"
    
    # 爬取数据
    result = crawl_uploader(
        uploader_url=uploader_url,
        max_videos=3,  # 获取 3 个视频
        get_details=True  # 获取详情
    )
    
    # 保存结果
    save_result(result)
    
    # 输出摘要
    print(f"\n{'='*60}")
    print(f"📊 爬取完成摘要")
    print(f"{'='*60}")
    
    if result["uploader_info"]:
        info = result["uploader_info"]
        print(f"UP 主：{info['uploader']}")
        print(f"UID: {info['uploader_id']}")
        print(f"视频总数：{info['total_videos']}")
    
    print(f"\n获取视频数：{len(result['videos'])}")
    print(f"获取详情数：{len(result['video_details'])}")


if __name__ == "__main__":
    main()
