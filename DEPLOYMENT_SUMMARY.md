# Coze API 部署完成总结

## ✅ 两件事已完成

### 1. 项目部署并生成 API ✅

**服务状态**: 运行中  
**端口**: 8001  
**API 端点**: `POST /api/uploader/info`

**测试命令**:
```bash
curl http://localhost:8001/health
# 响应：{"status":"healthy"}
```

---

### 2. 输入输出格式整理（适用于 Coze）✅

---

## 📋 输入格式（Coze API 请求）

### JSON 请求体

```json
{
  "uploader_url": "https://space.bilibili.com/1815948385",
  "max_videos": 5,
  "get_details": true,
  "cookie": "SESSDATA=xxx; bili_jct=xxx; DedeUserID=xxx"
}
```

### 参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|------|------|------|--------|------|------|
| `uploader_url` | string | ✅ | - | UP 主主页 URL | `"https://space.bilibili.com/1815948385"` |
| `max_videos` | int | ❌ | 5 | 最大视频数（1-50） | `5` |
| `get_details` | bool | ❌ | true | 是否获取详情 | `true` |
| `cookie` | string | ❌ | null | B 站 Cookie | `"SESSDATA=xxx; bili_jct=xxx"` |

---

## 📤 输出格式（Coze API 响应）

### 成功响应结构

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
        "title": "视频标题",
        "id": "BV1xxx",
        "url": "https://www.bilibili.com/video/BV1xxx"
      }
    ],
    "video_count": 3,
    "video_details": [
      {
        "title": "视频标题",
        "id": "BV1xxx",
        "url": "https://www.bilibili.com/video/BV1xxx",
        "duration_string": "32:31",
        "view_count": 145546,
        "like_count": 7788,
        "comment_count": 501,
        "upload_date": "20260314",
        "tags": ["AI", "教程"]
      }
    ],
    "details_count": 3
  },
  "error": null
}
```

### 失败响应

```json
{
  "success": false,
  "data": null,
  "error": "ERROR: [BilibiliSpaceVideo] xxx: Request is rejected"
}
```

---

## 🔗 Coze 工作流配置步骤

### 步骤 1：添加 API 连接器

在 Coze 工作流中：
1. 点击 **+** 添加节点
2. 选择 **API 连接器**
3. 选择 **自定义 API**

### 步骤 2：配置 API

| 字段 | 值 |
|------|-----|
| **名称** | `Bilibili Uploader Info` |
| **方法** | `POST` |
| **URL** | `http://your-server:8001/api/uploader/info` |
| **Headers** | `Content-Type: application/json` |

### 步骤 3：配置请求体

```json
{
  "uploader_url": "{{input.uploader_url}}",
  "max_videos": "{{input.max_videos}}",
  "get_details": "{{input.get_details}}",
  "cookie": "{{input.cookie}}"
}
```

### 步骤 4：添加输出解析节点

**代码节点**（Python）:

```python
def main(args: dict) -> dict:
    response = args.get('api_response', {})
    
    if not response.get('success'):
        return {
            'status': 'error',
            'message': response.get('error', '请求失败')
        }
    
    data = response.get('data', {})
    uploader = data.get('uploader_info', {})
    videos = data.get('video_details', [])
    
    return {
        'status': 'success',
        'uploader_name': uploader.get('uploader', ''),
        'uploader_uid': uploader.get('uploader_id', ''),
        'total_videos': data.get('video_count', 0),
        'videos': [
            {
                'title': v.get('title', ''),
                'duration': v.get('duration_string', ''),
                'views': v.get('view_count', 0),
                'likes': v.get('like_count', 0)
            }
            for v in videos[:5]
        ]
    }
```

---

## 🧪 测试方法

### 方法 1：cURL 测试

```bash
curl -X POST http://localhost:8001/api/uploader/info \
  -H "Content-Type: application/json" \
  -d '{
    "uploader_url": "https://space.bilibili.com/1815948385",
    "max_videos": 3,
    "get_details": true,
    "cookie": "SESSDATA=xxx; bili_jct=xxx; DedeUserID=xxx"
  }' | jq .
```

### 方法 2：Python 测试

```python
import requests

response = requests.post(
    "http://localhost:8001/api/uploader/info",
    json={
        "uploader_url": "https://space.bilibili.com/1815948385",
        "max_videos": 3,
        "get_details": True,
        "cookie": "SESSDATA=xxx; bili_jct=xxx"
    }
)

result = response.json()
print(result)
```

---

## ⚠️ 重要提示

### 1. Cookie 配置

**为什么需要 Cookie**:
- B 站反爬机制严格
- 无 Cookie 会返回 412 错误
- Cookie 可提高成功率

**获取方法**:
1. 访问 https://www.bilibili.com
2. 登录账号
3. F12 → Network → 刷新
4. 复制 `Cookie` 字段

**必需字段**:
```
SESSDATA=xxx; bili_jct=xxx; DedeUserID=xxx
```

### 2. 服务访问

**本地测试**:
```
http://localhost:8001/api/uploader/info
```

**外网访问**（需要配置）:
```
http://your-server-ip:8001/api/uploader/info
```

### 3. 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `HTTP Error 412` | Cookie 过期 | 更新 Cookie |
| `Request is rejected` | 无 Cookie | 添加 Cookie |
| `Timeout` | 视频太多 | 减少 max_videos |

---

## 📊 数据字段映射

### 输入字段（Coze → API）

| Coze 变量 | API 参数 | 类型 |
|----------|---------|------|
| `{{input.uploader_url}}` | `uploader_url` | string |
| `{{input.max_videos}}` | `max_videos` | int |
| `{{input.get_details}}` | `get_details` | bool |
| `{{input.cookie}}` | `cookie` | string |

### 输出字段（API → Coze）

| API 字段 | Coze 输出 | 类型 |
|---------|----------|------|
| `data.uploader_info.uploader` | `uploader_name` | string |
| `data.uploader_info.uploader_id` | `uploader_uid` | string |
| `data.video_count` | `total_videos` | int |
| `data.video_details[].title` | `videos[].title` | string |
| `data.video_details[].view_count` | `videos[].views` | int |
| `data.video_details[].like_count` | `videos[].likes` | int |

---

## 📁 相关文件

| 文件 | 说明 |
|------|------|
| `main.py` | API 主程序 |
| `COZE_API_GUIDE.md` | Coze API 完整指南 |
| `DEPLOYMENT_SUMMARY.md` | 本文档 |
| `bilibili_result.json` | 测试数据示例 |

---

## ✅ 完成清单

- [x] API 服务部署
- [x] API 端点创建 (`/api/uploader/info`)
- [x] 输入格式定义
- [x] 输出格式定义
- [x] Coze 配置文档
- [x] 测试脚本
- [ ] Cookie 配置（用户自行添加）
- [ ] 外网访问（按需配置）

---

## 🚀 下一步

1. **在 Coze 中配置 API 连接器**
2. **添加 Cookie 到环境变量**
3. **测试工作流**
4. **发布 Bot**

---

**部署完成！可以在 Coze 中配置使用了！** 🎉
