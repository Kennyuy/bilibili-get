# Coze Video API - 快速开始指南 v1.1

## ✅ 更新内容

- ✨ **支持抖音平台**
- ✨ **直接传入 Cookie 字符串**（不需要文件）
- ✨ **自动平台检测**

---

## 🚀 服务状态

```bash
# 检查服务
docker compose ps

# 查看日志
docker compose logs -f
```

**访问地址**: `http://localhost:8001`

---

## 📋 快速测试

### 1. 哔哩哔哩 - 获取视频信息

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

### 2. 抖音 - 获取视频信息

```bash
curl -X POST http://localhost:8001/api/coze/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.douyin.com/video/7xxx",
    "platform": "douyin",
    "action": "info",
    "cookie": "ttwid=xxx; sessionid=xxx"
  }'
```

### 3. 下载视频

```bash
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

---

## 🔑 Cookie 获取

### 哔哩哔哩

1. 访问 https://www.bilibili.com 并登录
2. F12 打开开发者工具 → Network 标签
3. 刷新页面，点击任意请求
4. 复制 `Cookie` 字段

**必需字段**:
```
SESSDATA=xxx; bili_jct=xxx; DedeUserID=xxx
```

### 抖音

1. 访问 https://www.douyin.com 并登录
2. F12 打开开发者工具 → Network 标签
3. 刷新页面，点击任意请求
4. 复制 `Cookie` 字段

**必需字段**:
```
ttwid=xxx; sessionid=xxx
```

---

## 🌐 支持的 URL 格式

### 哔哩哔哩
- `https://www.bilibili.com/video/BV1xx411c7mD`
- `https://b23.tv/xxx`

### 抖音
- `https://www.douyin.com/video/7xxx`
- `https://v.douyin.com/xxx`
- `https://iesdouyin.com/share/video/xxx`

---

## 📊 API 参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `url` | string | ✅ | 视频 URL |
| `platform` | string | ❌ | 平台：`auto`, `bilibili`, `douyin` |
| `action` | string | ✅ | 操作：`info`, `download` |
| `quality` | string | ❌ | 画质：`best`, `1080p`, `720p`, `480p` |
| `cookie` | string | ❌ | Cookie 字符串 |

---

## 🔗 Coze 工作流配置

### HTTP 请求节点配置

| 配置项 | 值 |
|--------|-----|
| **URL** | `http://your-server:8001/api/coze/webhook` |
| **方法** | `POST` |
| **Content-Type** | `application/json` |

### 请求体

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
        return {'status': 'error', 'message': response.get('error')}
    
    data = response.get('data', {})
    
    if args.get('action') == 'info':
        return {
            'status': 'success',
            'platform': data.get('platform'),
            'title': data.get('title'),
            'author': data.get('author'),
            'duration': data.get('duration'),
            'view_count': data.get('view_count'),
            'like_count': data.get('like_count')
        }
    else:
        return {
            'status': 'success',
            'filename': data.get('filename'),
            'message': data.get('message')
        }
```

---

## ⚠️ 注意事项

1. **Cookie 安全**: 不要将 Cookie 提交到 Git
2. **Cookie 有效期**: Cookie 会过期，需定期更新
3. **平台检测**: 建议明确指定 `platform` 参数
4. **并发限制**: 避免高频请求

---

## 📁 项目文件

```
coze-bilibili-api/
├── main.py              # FastAPI 主程序 ✅
├── config.py            # 配置管理 ✅
├── requirements.txt     # Python 依赖 ✅
├── Dockerfile           # Docker 配置 ✅
├── docker-compose.yml   # Docker Compose ✅
├── API_SPEC.md         # API 文档 ✅
├── QUICKSTART.md       # 快速开始 ✅
└── README.md           # 完整文档 ✅
```

---

## 🔧 常用命令

```bash
cd /home/ubuntu/.openclaw/workspace/projects/coze-bilibili-api

# 查看状态
docker compose ps

# 查看日志
docker compose logs -f

# 重启服务
docker compose restart

# 更新代码
docker compose down && docker compose up -d --build
```

---

**服务已就绪！支持哔哩哔哩和抖音！** 🚀
