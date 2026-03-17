# Coze API 部署指南

## ✅ API 已部署

**服务地址**: `http://localhost:8001`

**API 端点**: `POST /api/uploader/info`

---

## 📋 输入格式（Coze API 请求）

### 请求体（JSON）

```json
{
  "uploader_url": "https://space.bilibili.com/1815948385",
  "max_videos": 5,
  "get_details": true,
  "cookie": "SESSDATA=xxx; bili_jct=xxx; DedeUserID=xxx"
}
```

### 参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `uploader_url` | string | ✅ | - | B 站 UP 主主页 URL |
| `max_videos` | int | ❌ | 5 | 最大获取视频数量（1-50） |
| `get_details` | bool | ❌ | true | 是否获取视频详情 |
| `cookie` | string | ❌ | null | B 站 Cookie（推荐提供） |

### URL 格式

**正确格式**:
```
https://space.bilibili.com/1815948385
```

**如何获取**:
1. 访问 UP 主主页
2. 复制浏览器地址栏 URL
3. 格式：`https://space.bilibili.com/{UID}`

---

## 📤 输出格式（Coze API 响应）

### 成功响应

```json
{
  "success": true,
  "data": {
    "uploader_info": {
      "uploader": "马克的技术工作坊",
      "uploader_id": "1815948385",
      "url": "https://space.bilibili.com/1815948385"
    },
    "videos": [
      {
        "index": 1,
        "title": "从 LLM 到 Agent Skill，一期视频带你打通底层逻辑！",
        "id": "BV1E7wtzaEdq",
        "url": "https://www.bilibili.com/video/BV1E7wtzaEdq"
      },
      {
        "index": 2,
        "title": "Claude Code 从 0 到 1 全攻略",
        "id": "BV14rzQB9EJj",
        "url": "https://www.bilibili.com/video/BV14rzQB9EJj"
      }
    ],
    "video_count": 2,
    "video_details": [
      {
        "title": "从 LLM 到 Agent Skill，一期视频带你打通底层逻辑！",
        "id": "BV1E7wtzaEdq",
        "url": "https://www.bilibili.com/video/BV1E7wtzaEdq",
        "duration_string": "32:31",
        "view_count": 145546,
        "like_count": 7788,
        "comment_count": 501,
        "upload_date": "20260314",
        "tags": ["AI", "教程", "Context", "Agent Skills"]
      }
    ],
    "details_count": 1
  },
  "error": null
}
```

### 失败响应

```json
{
  "success": false,
  "data": null,
  "error": "ERROR: [BilibiliSpaceVideo] xxx: Request is rejected by server"
}
```

---

## 🔗 Coze 工作流配置

### 步骤 1：添加 API 连接器

1. 在 Coze 工作流中添加 **API 连接器**
2. 选择 **自定义 API**
3. 配置如下：

### 步骤 2：配置 API

| 配置项 | 值 |
|--------|-----|
| **名称** | `Bilibili Uploader Info` |
| **方法** | `POST` |
| **URL** | `http://your-server:8001/api/uploader/info` |
| **Content-Type** | `application/json` |

### 步骤 3：配置请求体

```json
{
  "uploader_url": "{{input.uploader_url}}",
  "max_videos": "{{input.max_videos}}",
  "get_details": "{{input.get_details}}",
  "cookie": "{{input.cookie}}"
}
```

### 步骤 4：输出解析

**代码节点**:

```python
def main(args: dict) -> dict:
    """解析 B 站 UP 主信息 API 响应"""
    response = args.get('api_response', {})
    
    if not response.get('success'):
        return {
            'status': 'error',
            'message': response.get('error', '请求失败')
        }
    
    data = response.get('data', {})
    
    # UP 主信息
    uploader = data.get('uploader_info', {})
    
    # 视频列表
    videos = data.get('videos', [])
    video_details = data.get('video_details', [])
    
    # 格式化输出
    result = {
        'status': 'success',
        'uploader_name': uploader.get('uploader', ''),
        'uploader_id': uploader.get('uploader_id', ''),
        'video_count': data.get('video_count', 0),
        'videos': []
    }
    
    # 合并视频信息和详情
    for video in videos:
        video_info = {
            'title': video.get('title', ''),
            'url': video.get('url', ''),
            'id': video.get('id', '')
        }
        
        # 查找对应的详情
        for detail in video_details:
            if detail.get('id') == video.get('id'):
                video_info['duration'] = detail.get('duration_string', '')
                video_info['view_count'] = detail.get('view_count', 0)
                video_info['like_count'] = detail.get('like_count', 0)
                video_info['tags'] = detail.get('tags', [])
                break
        
        result['videos'].append(video_info)
    
    return result
```

---

## 🧪 测试命令

### cURL 测试

```bash
# 基本测试
curl -X POST http://localhost:8001/api/uploader/info \
  -H "Content-Type: application/json" \
  -d '{
    "uploader_url": "https://space.bilibili.com/1815948385",
    "max_videos": 3,
    "get_details": true
  }'

# 带 Cookie 测试
curl -X POST http://localhost:8001/api/uploader/info \
  -H "Content-Type: application/json" \
  -d '{
    "uploader_url": "https://space.bilibili.com/1815948385",
    "max_videos": 3,
    "get_details": true,
    "cookie": "SESSDATA=xxx; bili_jct=xxx; DedeUserID=xxx"
  }'
```

### Python 测试

```python
import requests

API_URL = "http://localhost:8001/api/uploader/info"

response = requests.post(API_URL, json={
    "uploader_url": "https://space.bilibili.com/1815948385",
    "max_videos": 3,
    "get_details": True
})

result = response.json()

if result["success"]:
    data = result["data"]
    print(f"UP 主：{data['uploader_info']['uploader']}")
    print(f"视频数：{data['video_count']}")
    
    for video in data.get('video_details', []):
        print(f"\n标题：{video['title']}")
        print(f"播放：{video['view_count']:,}")
        print(f"点赞：{video['like_count']:,}")
```

---

## ⚠️ 注意事项

### 1. Cookie 配置

**为什么需要 Cookie**:
- B 站反爬机制严格
- 没有 Cookie 可能返回 412 错误
- Cookie 可提高请求成功率

**如何获取 Cookie**:
1. 访问 https://www.bilibili.com
2. 登录账号
3. F12 → Network → 刷新
4. 复制 `Cookie` 字段

**必需字段**:
```
SESSDATA=xxx; bili_jct=xxx; DedeUserID=xxx
```

### 2. 请求限制

| 限制项 | 值 |
|--------|-----|
| 最大视频数 | 50 |
| 推荐视频数 | 5-10 |
| 请求超时 | 120 秒 |

### 3. 错误处理

| 错误信息 | 原因 | 解决方案 |
|---------|------|----------|
| `Request is rejected` | 无 Cookie 或 Cookie 过期 | 更新 Cookie |
| `HTTP Error 412` | Cookie 无效 | 重新获取 Cookie |
| `Timeout` | 网络超时 | 减少视频数量 |

---

## 📊 数据字段说明

### uploader_info（UP 主信息）

| 字段 | 类型 | 说明 |
|------|------|------|
| `uploader` | string | UP 主名称 |
| `uploader_id` | string | UP 主 UID |
| `url` | string | 主页 URL |

### videos（视频列表）

| 字段 | 类型 | 说明 |
|------|------|------|
| `index` | int | 序号 |
| `title` | string | 视频标题 |
| `id` | string | 视频 ID（BV 号） |
| `url` | string | 视频链接 |

### video_details（视频详情）

| 字段 | 类型 | 说明 |
|------|------|------|
| `title` | string | 视频标题 |
| `id` | string | 视频 ID |
| `url` | string | 视频链接 |
| `duration_string` | string | 时长（MM:SS） |
| `view_count` | int | 播放量 |
| `like_count` | int | 点赞数 |
| `comment_count` | int | 评论数 |
| `upload_date` | string | 上传日期（YYYYMMDD） |
| `tags` | array | 标签列表 |

---

## 🚀 部署检查清单

- [x] API 服务运行中
- [x] API 端点可用
- [x] 输入输出格式定义
- [x] Coze 工作流配置文档
- [ ] Cookie 配置（用户自行添加）
- [ ] 外网访问配置（如需）

---

## 📁 相关文件

- `main.py` - API 主程序
- `COZE_API_GUIDE.md` - 本文档
- `API_UPLOADER_GUIDE.md` - UP 主爬取指南
- `bilibili_result.json` - 测试结果

---

**API 已就绪！可以在 Coze 中配置使用！** 🎉
