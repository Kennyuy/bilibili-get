#!/usr/bin/env python3
"""
API 测试脚本
"""

import requests
import json

BASE_URL = "http://localhost:8000"

# 测试视频 URL
TEST_VIDEO_URL = "https://www.bilibili.com/video/BV1E7wtzaEdq"


def test_health():
    """测试健康检查"""
    print("=" * 60)
    print("测试 1: 健康检查")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"状态码：{response.status_code}")
    print(f"响应：{json.dumps(response.json(), indent=2)}")
    print()


def test_video_info():
    """测试获取视频信息"""
    print("=" * 60)
    print("测试 2: 获取视频信息")
    print("=" * 60)
    
    payload = {
        "url": TEST_VIDEO_URL
    }
    
    response = requests.post(
        f"{BASE_URL}/api/video/info",
        json=payload
    )
    
    print(f"状态码：{response.status_code}")
    result = response.json()
    
    if result.get("success"):
        data = result.get("data", {})
        print(f"标题：{data.get('title', '')}")
        print(f"UP 主：{data.get('uploader', '')}")
        print(f"时长：{data.get('duration_string', '')}")
        print(f"播放量：{data.get('view_count', 0):,}")
        print(f"点赞数：{data.get('like_count', 0):,}")
    else:
        print(f"错误：{result.get('error', '')}")
    
    print()


def test_coze_webhook_info():
    """测试 Coze Webhook - 获取信息"""
    print("=" * 60)
    print("测试 3: Coze Webhook - 获取信息")
    print("=" * 60)
    
    payload = {
        "video_url": TEST_VIDEO_URL,
        "action": "info"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/coze/webhook",
        json=payload
    )
    
    print(f"状态码：{response.status_code}")
    result = response.json()
    
    if result.get("success"):
        data = result.get("data", {})
        print(f"标题：{data.get('title', '')}")
        print(f"UP 主：{data.get('uploader', '')}")
        print(f"时长：{data.get('duration', '')}")
        print(f"播放量：{data.get('view_count', 0):,}")
    else:
        print(f"错误：{result.get('error', '')}")
    
    print()


def test_list_formats():
    """测试列出可用格式"""
    print("=" * 60)
    print("测试 4: 列出可用格式")
    print("=" * 60)
    
    from urllib.parse import quote
    encoded_url = quote(TEST_VIDEO_URL, safe='')
    
    response = requests.get(f"{BASE_URL}/api/formats/{encoded_url}")
    
    print(f"状态码：{response.status_code}")
    result = response.json()
    
    if result.get("success"):
        data = result.get("data", {})
        print(f"视频：{data.get('title', '')}")
        print(f"可用格式数量：{len(data.get('formats', []))}")
        
        formats = data.get("formats", [])[:5]
        print("\n前 5 个格式:")
        for fmt in formats:
            print(f"  - {fmt.get('format_id')}: {fmt.get('format')} ({fmt.get('resolution')})")
    else:
        print(f"错误：{result.get('error', '')}")
    
    print()


def main():
    """运行所有测试"""
    print("\n🚀 Coze Bilibili API 测试\n")
    
    try:
        test_health()
        test_video_info()
        test_coze_webhook_info()
        test_list_formats()
        
        print("=" * 60)
        print("✅ 所有测试完成！")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到 API 服务")
        print("请确保服务已启动：docker-compose up -d")
    except Exception as e:
        print(f"❌ 测试失败：{e}")


if __name__ == "__main__":
    main()
