# Coze Video API - 最终使用指南

## ✅ API 已完成

| 功能 | 状态 | 平台 |
|------|------|------|
| **API 服务** | ✅ 运行中 | 哔哩哔哩 + 抖音 |
| **Cookie 字符串输入** | ✅ 支持 | 两个平台 |
| **自动平台检测** | ✅ 支持 | 自动识别 |
| **哔哩哔哩** | ✅ 完全可用 | 推荐 |
| **抖音** | ⚠️ 需新鲜 Cookie | 反爬严格 |

---

## 🌐 服务地址

```
http://localhost:8001
```

---

## 📋 API 输入格式（JSON）

### 通用请求结构

```json
{
  "url": "视频 URL",
  "platform": "auto",
  "action": "info",
  "quality": "best",
  "cookie": "Cookie 字符串"
}
```

### 参数说明

| 参数 | 类型 | 必填 | 说明 | 可选值 |
|------|------|------|------|--------|
| `url` | string | ✅ | 视频 URL | - |
| `platform` | string | ❌ | 平台类型 | `"auto"`, `"bilibili"`, `"douyin"` |
| `action` | string | ✅ | 操作类型 | `"info"`, `"download"` |
| `quality` | string | ❌ | 画质（仅 download 需要） | `"best"`, `"1080p"`, `"720p"`, `"480p"` |
| `cookie` | string | ❌ | Cookie 字符串 | - |

---

## 🎯 平台 URL 格式

### 哔哩哔哩 ✅ 推荐

```
https://www.bilibili.com/video/BV1xx411c7mD
https://b23.tv/xxx
```

### 抖音 ⚠️ 需新鲜 Cookie

```
https://www.douyin.com/video/7xxxxxxxxxx
```

---

## 📤 请求示例

### 1. 哔哩哔哩 - 获取视频信息 ✅

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
    "view_count": 142172,
    "like_count": 7667,
    "url": "https://www.bilibili.com/video/BV1E7wtzaEdq",
    "thumbnail": "http://i0.hdslb.com/bfs/archive/xxx.jpg"
  }
}
```

---

### 2. 哔哩哔哩 - 下载视频 ✅

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

### 3. 抖音 - 获取视频信息 ⚠️

**请求**:
```json
{
  "url": "https://www.douyin.com/video/7598365104291302675",
  "platform": "douyin",
  "action": "info",
  "cookie": "ttwid=xxx; sessionid=xxx; sid_tt=xxx; odin_tt=xxx"
}
```

**可能的响应**:
```json
{
  "success": false,
  "error": "ERROR: [Douyin] xxx: Fresh cookies (not necessarily logged in) are needed"
}
```

> ⚠️ **注意**: 抖音反爬严格，需要非常新鲜的 Cookie（最好是刚登录获取的）

---

## 🔑 Cookie 获取方法

### 哔哩哔哩（推荐）

1. 访问 https://www.bilibili.com
2. 登录账号
3. F12 → Network → 刷新页面
4. 点击任意请求，复制 `Cookie` 字段

**必需字段**:
```
SESSDATA=xxx; bili_jct=xxx; DedeUserID=xxx
```

**示例**:
```
SESSDATA=96abedd0%2C1789137924%2Cxxx; bili_jct=9c2cc71b9117c844cab32f59c251cacc; DedeUserID=1983776166
```

---

### 抖音（需新鲜）

1. 浏览器**无痕模式**访问 https://www.douyin.com
2. **登录账号**
3. 打开**具体视频**（不是首页）
4. F12 → Network → 刷新
5. 复制最新的 `Cookie` 字段

**必需字段**:
```
ttwid=xxx; sessionid=xxx; sid_tt=xxx; odin_tt=xxx
```

---

## 🔗 Coze 工作流配置

### HTTP 请求节点

| 配置项 | 值 |
|--------|-----|
| **URL** | `http://your-server:8001/api/coze/webhook` |
| **方法** | `POST` |
| **Content-Type** | `application/json` |

### 请求体模板

```json
{
  "url": "{{input.video_url}}",
  "platform": "{{input.platform}}",
  "action": "{{input.action}}",
  "quality": "{{input.quality}}",
  "cookie": "{{input.cookie}}"
}
```

### 输出解析代码

```python
def main(args: dict) -> dict:
    response = args.get('http_response', {})
    
    if not response.get('success'):
        return {
            'status': 'error',
            'message': response.get('error', '请求失败')
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
    else:  # download
        return {
            'status': 'success',
            'filename': data.get('filename', ''),
            'file_path': data.get('file_path', ''),
            'message': data.get('message', '')
        }
```

---

## 🧪 测试命令

### 哔哩哔哩测试

```bash
curl -X POST http://localhost:8001/api/coze/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.bilibili.com/video/BV1E7wtzaEdq",
    "platform": "bilibili",
    "action": "info",
    "cookie": "SESSDATA=xxx; bili_jct=xxx; DedeUserID=xxx"
  }'
```

### 抖音测试

```bash
curl -X POST http://localhost:8001/api/coze/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.douyin.com/video/7xxx",
    "platform": "douyin",
    "action": "info",
    "cookie": "ttwid=xxx; sessionid=xxx; sid_tt=xxx"
  }'
```

---

## ⚠️ 常见问题

### 1. 抖音返回 "Fresh cookies needed"

**原因**: Cookie 过期或无效

**解决**:
- 使用无痕模式重新登录
- 获取最新的 Cookie
- 确保打开的是具体视频页面（不是首页）

### 2. 哔哩哔哩返回 412 错误

**原因**: Cookie 失效

**解决**: 重新获取 Cookie

### 3. 下载超时

**原因**: 视频太大或网络问题

**解决**:
- 降低画质（`quality: "480p"`）
- 检查网络连接
- 增加超时时间

---

## 📊 平台对比

| 特性 | 哔哩哔哩 | 抖音 |
|------|---------|------|
| **API 支持** | ✅ 完善 | ✅ 支持 |
| **Cookie 有效期** | 数周 | 数天 |
| **反爬强度** | 中等 | 严格 |
| **推荐程度** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **测试状态** | ✅ 通过 | ⚠️ 需新鲜 Cookie |

---

## 📁 项目文件

```
/home/ubuntu/.openclaw/workspace/projects/coze-bilibili-api/
├── main.py              # API 主程序 ✅
├── config.py            # 配置文件 ✅
├── requirements.txt     # Python 依赖 ✅
├── Dockerfile           # Docker 配置 ✅
├── docker-compose.yml   # Docker Compose ✅
├── API_SPEC.md         # API 规范 ✅
├── QUICKSTART.md       # 快速开始 ✅
├── FINAL_API_GUIDE.md  # 本文档 ✅
└── README.md           # 完整文档 ✅
```

---

## 🚀 服务管理

```bash
cd /home/ubuntu/.openclaw/workspace/projects/coze-bilibili-api

# 查看状态
docker compose ps

# 查看日志
docker compose logs -f

# 重启服务
docker compose restart

# 停止服务
docker compose down
```

---

## ✅ 总结

1. **API 已完成** - 支持哔哩哔哩和抖音
2. **Cookie 字符串输入** - 直接传入，不需要文件
3. **哔哩哔哩** - ✅ 完全可用，推荐使用
4. **抖音** - ⚠️ 需要非常新鲜的 Cookie
5. **自动平台检测** - `platform="auto"` 自动识别

**建议优先使用哔哩哔哩进行测试和开发！**
