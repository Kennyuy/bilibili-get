# Coze Video API - 接口规范 v1.1

## 基础信息

- **基础 URL**: `http://localhost:8001`
- **Content-Type**: `application/json`
- **支持平台**: 哔哩哔哩、抖音
- **认证**: Cookie 字符串（可选，推荐）

---

## 📋 输入参数说明

### 通用参数

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `url` | string | ✅ | 视频 URL | `"https://www.bilibili.com/video/BV1xx"` |
| `platform` | string | ❌ | 平台类型 | `"auto"`, `"bilibili"`, `"douyin"` |
| `cookie` | string | ❌ | Cookie 字符串 | `"SESSDATA=xxx; bili_jct=xxx"` |
| `action` | string | ✅ | 操作类型 | `"info"`, `"download"` |
| `quality` | string | ❌ | 画质 | `"best"`, `"1080p"`, `"720p"` |

---

## 🎯 平台 URL 格式

### 哔哩哔哩

```
https://www.bilibili.com/video/BV1xx411c7mD
https://b23.tv/xxx
```

### 抖音

```
https://www.douyin.com/video/7xxx
https://v.douyin.com/xxx
https://iesdouyin.com/share/video/xxx
```

---

## 📤 请求示例

### 1. 获取视频信息（哔哩哔哩）

**请求**:
```json
{
  "url": "https://www.bilibili.com/video/BV1E7wtzaEdq",
  "platform": "bilibili",
  "action": "info",
  "cookie": "SESSDATA=xxx; bili_jct=xxx; DedeUserID=xxx"
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "platform": "bilibili",
    "title": "从 LLM 到 Agent Skill，一期视频带你打通底层逻辑！",
    "author": "马克的技术工作坊",
    "duration": "32:31",
    "view_count": 141644,
    "like_count": 7650,
    "url": "https://www.bilibili.com/video/BV1E7wtzaEdq",
    "thumbnail": "http://i0.hdslb.com/bfs/archive/xxx.jpg"
  }
}
```

---

### 2. 获取视频信息（抖音）

**请求**:
```json
{
  "url": "https://www.douyin.com/video/7348790315519806771",
  "platform": "douyin",
  "action": "info",
  "cookie": "ttwid=xxx; sessionid=xxx; csrf_session_id=xxx"
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "platform": "douyin",
    "title": "视频标题",
    "author": "抖音博主",
    "duration": "0:59",
    "view_count": 1234567,
    "like_count": 123456,
    "url": "https://www.douyin.com/video/7xxx",
    "thumbnail": "http://..."
  }
}
```

---

### 3. 下载视频

**请求**:
```json
{
  "url": "https://www.bilibili.com/video/BV1E7wtzaEdq",
  "platform": "bilibili",
  "action": "download",
  "quality": "1080p",
  "cookie": "SESSDATA=xxx; bili_jct=xxx"
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "filename": "视频标题.mp4",
    "file_path": "/tmp/video_download_xxx/视频标题.mp4",
    "message": "Video downloaded successfully"
  }
}
```

---

### 4. 自动检测平台

**请求**:
```json
{
  "url": "https://www.bilibili.com/video/BV1E7wtzaEdq",
  "platform": "auto",
  "action": "info"
}
```

**说明**: `platform="auto"` 时会自动根据 URL 检测平台

**响应**:
```json
{
  "success": true,
  "data": {
    "platform": "bilibili",
    "title": "...",
    ...
  }
}
```

---

## 🔑 Cookie 获取方法

### 哔哩哔哩 Cookie

1. 打开浏览器，访问 https://www.bilibili.com
2. 登录账号
3. 按 F12 打开开发者工具
4. 切换到 **Network** 标签
5. 刷新页面，点击任意请求
6. 复制 **Request Headers** 中的 `Cookie` 字段

**必需字段**:
- `SESSDATA` - 登录会话
- `bili_jct` - CSRF 令牌
- `DedeUserID` - 用户 ID

**示例**:
```
SESSDATA=96abedd0%2C1789137924%2Cxxx; bili_jct=9c2cc71b9117c844cab32f59c251cacc; DedeUserID=1983776166
```

---

### 抖音 Cookie

1. 打开浏览器，访问 https://www.douyin.com
2. 登录账号
3. 按 F12 打开开发者工具
4. 切换到 **Network** 标签
5. 刷新页面，点击任意请求
6. 复制 **Request Headers** 中的 `Cookie` 字段

**必需字段**:
- `ttwid` - 会话 ID
- `sessionid` - 登录会话
- `csrf_session_id` - CSRF 令牌

**示例**:
```
ttwid=1%7Cxxx; sessionid=xxx; csrf_session_id=xxx
```

---

## 📊 完整 API 接口

### 1. Coze Webhook（推荐）

**接口**: `POST /api/coze/webhook`

**请求**:
```json
{
  "url": "https://...",
  "platform": "auto",
  "action": "info",
  "quality": "best",
  "cookie": "..."
}
```

---

### 2. 获取视频信息

**接口**: `POST /api/video/info`

**请求**:
```json
{
  "url": "https://...",
  "platform": "bilibili",
  "cookie": "..."
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "id": "BV1xx411c7mD",
    "title": "视频标题",
    "description": "简介",
    "uploader": "UP 主",
    "url": "https://...",
    "duration": 1951,
    "duration_string": "32:31",
    "upload_date": "20260314",
    "view_count": 141644,
    "like_count": 7650,
    "comment_count": 490,
    "tags": ["AI", "教程"],
    "thumbnail": "http://...",
    "platform": "bilibili",
    "formats_count": 21
  }
}
```

---

### 3. 下载视频

**接口**: `POST /api/video/download`

**请求**:
```json
{
  "url": "https://...",
  "platform": "bilibili",
  "quality": "1080p",
  "cookie": "..."
}
```

**响应**:
```json
{
  "success": true,
  "file_path": "/tmp/video_download_xxx/视频标题.mp4",
  "download_url": "/api/files/视频标题.mp4",
  "error": null
}
```

---

### 4. 列出可用格式

**接口**: `GET /api/formats?url={url}&platform={platform}`

**请求**:
```
GET /api/formats?url=https://www.bilibili.com/video/BV1xx&platform=bilibili
```

**响应**:
```json
{
  "success": true,
  "data": {
    "platform": "bilibili",
    "title": "视频标题",
    "formats": [
      {
        "format_id": "30121",
        "format": "4K 超高清",
        "ext": "mp4",
        "resolution": "3840x2160",
        "filesize_approx": 1310151128,
        "tbr": 5372.224
      }
    ]
  }
}
```

---

## ⚠️ 错误处理

### 常见错误

| 错误信息 | 原因 | 解决方案 |
|---------|------|----------|
| `HTTP Error 412` | Cookie 过期或无效 | 重新获取 Cookie |
| `Command timeout` | 网络超时 | 检查网络，重试 |
| `Download timeout` | 下载超时 | 降低画质重试 |
| `Unknown platform` | URL 无法识别 | 检查 URL 格式 |

### 错误响应格式

```json
{
  "success": false,
  "data": null,
  "error": "ERROR: [BiliBili] xxx: Unable to download webpage..."
}
```

---

## 🔧 Coze 工作流配置

### 输入变量

```json
{
  "url": "string (required)",
  "platform": "string (enum: auto, bilibili, douyin)",
  "action": "string (enum: info, download)",
  "quality": "string (optional)",
  "cookie": "string (optional)"
}
```

### 输出解析

```python
def main(args: dict) -> dict:
    response = args.get('http_response', {})
    
    if not response.get('success'):
        return {
            'status': 'error',
            'message': response.get('error', 'Unknown error')
        }
    
    data = response.get('data', {})
    
    if args.get('action') == 'info':
        return {
            'status': 'success',
            'platform': data.get('platform', ''),
            'title': data.get('title', ''),
            'author': data.get('author', ''),
            'duration': data.get('duration', ''),
            'view_count': data.get('view_count', 0),
            'like_count': data.get('like_count', 0),
            'url': data.get('url', ''),
            'thumbnail': data.get('thumbnail', '')
        }
    else:
        return {
            'status': 'success',
            'filename': data.get('filename', ''),
            'file_path': data.get('file_path', ''),
            'message': data.get('message', '')
        }
```

---

## 📝 注意事项

1. **Cookie 有效期**: Cookie 会过期，建议定期更新
2. **平台检测**: `platform="auto"` 会自动检测，但建议明确指定
3. **并发限制**: 避免同时发起大量请求
4. **存储空间**: 下载的视频会占用磁盘空间
5. **法律合规**: 仅用于个人学习研究

---

## 🧪 测试命令

```bash
# 哔哩哔哩 - 获取信息
curl -X POST http://localhost:8001/api/coze/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.bilibili.com/video/BV1E7wtzaEdq",
    "platform": "bilibili",
    "action": "info",
    "cookie": "SESSDATA=xxx; bili_jct=xxx"
  }'

# 抖音 - 获取信息
curl -X POST http://localhost:8001/api/coze/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.douyin.com/video/7xxx",
    "platform": "douyin",
    "action": "info",
    "cookie": "ttwid=xxx; sessionid=xxx"
  }'

# 下载视频
curl -X POST http://localhost:8001/api/coze/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.bilibili.com/video/BV1E7wtzaEdq",
    "platform": "bilibili",
    "action": "download",
    "quality": "720p",
    "cookie": "SESSDATA=xxx; bili_jct=xxx"
  }'
```
