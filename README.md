# Coze Bilibili API Service

📺 哔哩哔哩视频信息获取和下载 API 服务，可与 Coze 工作流集成

## 功能特性

- ✅ **视频信息获取** - 获取标题、UP 主、播放量、点赞数等
- ✅ **视频下载** - 支持多种画质（4K/1080p/720p/480p）
- ✅ **Coze Webhook** - 可直接被 Coze 工作流调用
- ✅ **Docker 部署** - 一键启动，开箱即用
- ✅ **API Key 认证** - 可选的安全认证

## 快速开始

### 方法 1：Docker 部署（推荐）

**服务已部署！** 运行在 `http://localhost:8001`

```bash
# 进入项目目录
cd /home/ubuntu/.openclaw/workspace/projects/coze-bilibili-api

# 检查服务状态
docker compose ps

# 查看日志
docker compose logs -f

# 重启服务
docker compose restart

# 停止服务
docker compose down
```

### 方法 2：直接运行（开发环境）

```bash
# 1. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 安装 yt-dlp
pip install yt-dlp

# 4. 安装 ffmpeg（系统级）
sudo apt install ffmpeg

# 5. 启动服务
python main.py
```

## API 接口

### 1. 健康检查

```bash
curl http://localhost:8000/health
```

**响应**:
```json
{"status": "healthy"}
```

### 2. 获取视频信息

```bash
curl -X POST http://localhost:8000/api/video/info \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.bilibili.com/video/BV1xx411c7mD"
  }'
```

**响应**:
```json
{
  "success": true,
  "data": {
    "id": "BV1xx411c7mD",
    "title": "视频标题",
    "uploader": "UP 主名称",
    "duration": 1951,
    "duration_string": "32:31",
    "view_count": 138022,
    "like_count": 7486,
    "comment_count": 490,
    "upload_date": "20260314",
    "thumbnail": "http://...",
    "url": "https://www.bilibili.com/video/BV1xx411c7mD"
  }
}
```

### 3. 下载视频

```bash
curl -X POST http://localhost:8000/api/video/download \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.bilibili.com/video/BV1xx411c7mD",
    "quality": "1080p"
  }'
```

**quality 参数**:
- `best` - 最佳画质（默认）
- `4k` - 4K 超高清
- `1080p` - 1080P 高清
- `720p` - 720P 准高清
- `480p` - 480P 标清

**响应**:
```json
{
  "success": true,
  "file_path": "/tmp/bilibili_download_xxx/视频标题.mp4",
  "download_url": "/api/files/视频标题.mp4"
}
```

### 4. Coze Webhook 接口

```bash
curl -X POST http://localhost:8000/api/coze/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "video_url": "https://www.bilibili.com/video/BV1xx411c7mD",
    "action": "info"
  }'
```

**action 参数**:
- `info` - 获取视频信息
- `download` - 下载视频

**响应（info）**:
```json
{
  "success": true,
  "data": {
    "title": "视频标题",
    "uploader": "UP 主名称",
    "duration": "32:31",
    "view_count": 138022,
    "like_count": 7486,
    "url": "https://www.bilibili.com/video/BV1xx411c7mD",
    "thumbnail": "http://..."
  }
}
```

### 5. 列出可用格式

```bash
curl http://localhost:8000/api/formats/https://www.bilibili.com/video/BV1xx411c7mD
```

## Coze 工作流集成

### 步骤 1：添加 HTTP 请求节点

在 Coze 工作流中添加 **HTTP 请求** 节点

### 步骤 2：配置请求

- **URL**: `http://your-server:8000/api/coze/webhook`
- **方法**: `POST`
- **Headers**: 
  - `Content-Type: application/json`
- **Body** (JSON):
```json
{
  "video_url": "{{input.video_url}}",
  "action": "{{input.action}}",
  "quality": "{{input.quality}}"
}
```

### 步骤 3：解析响应

添加 **代码** 节点处理响应：

```python
def main(args: dict) -> dict:
    response = args.get('http_response', {})
    
    if response.get('success'):
        data = response.get('data', {})
        return {
            'title': data.get('title', ''),
            'uploader': data.get('uploader', ''),
            'duration': data.get('duration', ''),
            'view_count': data.get('view_count', 0),
            'like_count': data.get('like_count', 0),
        }
    else:
        return {
            'error': response.get('error', 'Unknown error')
        }
```

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `API_PORT` | API 服务端口 | `8000` |
| `API_KEY` | API 密钥（可选） | 无 |
| `COOKIES_FILE` | B 站 Cookie 文件路径 | 无 |
| `DOWNLOAD_DIR` | 视频下载目录 | `/tmp/bilibili_downloads` |
| `DOWNLOAD_TIMEOUT` | 下载超时（秒） | `600` |
| `LOG_LEVEL` | 日志级别 | `INFO` |
| `DEBUG` | 调试模式 | `false` |

## 获取 B 站 Cookie

1. 安装浏览器扩展：**"Get cookies.txt LOCALLY"**
2. 访问 B 站并登录
3. 点击扩展图标，导出 `cookies.txt`
4. 将文件放在安全位置，并在 `.env` 中配置路径

## 项目结构

```
coze-bilibili-api/
├── main.py              # FastAPI 主程序
├── config.py            # 配置管理
├── requirements.txt     # Python 依赖
├── Dockerfile           # Docker 配置
├── docker-compose.yml   # Docker Compose
├── .env.example         # 环境变量示例
├── .env                 # 实际环境变量（需创建）
├── bilibili_cookies.txt # B 站 Cookie（需自行准备）
└── downloads/           # 视频下载目录
```

## 安全注意事项

1. **API Key**: 生产环境建议启用 API Key 认证
2. **Cookie 文件**: 妥善保管，不要提交到 Git
3. **访问控制**: 建议通过 Nginx 反向代理并配置 HTTPS
4. **速率限制**: 避免频繁请求触发 B 站反爬

## 常见问题

### Q: 下载失败，提示 412 错误？
A: Cookie 可能过期，请重新导出 Cookie 文件

### Q: 视频和音频分离？
A: 确保已安装 ffmpeg，Docker 镜像已预装

### Q: 如何在 Coze 中使用？
A: 使用 HTTP 请求节点调用 `/api/coze/webhook` 接口

### Q: 如何查看日志？
A: `docker-compose logs -f` 或查看应用日志

## License

MIT
