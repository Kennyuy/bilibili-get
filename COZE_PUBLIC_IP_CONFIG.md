# Coze 配置指南（公网 IP: 1.12.64.197）

## ✅ 服务状态

**公网访问**: ✅ 可用  
**API 地址**: `http://1.12.64.197:8001/api/uploader/info`  
**健康检查**: ✅ 通过

---

## 🎯 在 Coze 中配置（5 步完成）

### 步骤 1：打开 Coze

访问：https://www.coze.cn

### 步骤 2：创建或编辑 Bot

1. 点击 **创建 Bot** 或选择已有 Bot
2. 进入 Bot 编辑页面
3. 点击 **工作流** 标签

### 步骤 3：添加 API 连接器

1. 点击 **+** 添加节点
2. 选择 **API 连接器**
3. 点击 **添加 API**

### 步骤 4：填写 API 配置

#### 基本信息

| 字段 | 值 |
|------|-----|
| **名称** | `Bilibili Uploader Info` |
| **描述** | `获取 B 站 UP 主信息及视频详情` |
| **方法** | `POST` |
| **URL** | `http://1.12.64.197:8001/api/uploader/info` |

> ✅ **重要**: URL 已配置为你的公网 IP

#### Headers

点击 **Headers**，添加：

| Key | Value |
|-----|-------|
| `Content-Type` | `application/json` |

#### 请求体（Body）

点击 **Body**，选择 **JSON**，输入：

```json
{
  "uploader_url": "{{input.uploader_url}}",
  "max_videos": "{{input.max_videos}}",
  "get_details": "{{input.get_details}}",
  "cookie": "{{input.cookie}}"
}
```

### 步骤 5：配置输入参数

点击 **输入**，添加以下参数：

| 参数名 | 类型 | 必填 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `uploader_url` | string | ✅ | - | UP 主主页 URL |
| `max_videos` | number | ❌ | 5 | 最大视频数（1-50） |
| `get_details` | boolean | ❌ | true | 是否获取详情 |
| `cookie` | string | ❌ | - | B 站 Cookie（可选） |

---

## 🧪 测试配置

### 测试 1：基本测试

在 API 连接器中点击 **测试**，输入：

```json
{
  "uploader_url": "https://space.bilibili.com/20713882",
  "max_videos": 3,
  "get_details": true
}
```

点击 **运行测试**，应该返回：

```json
{
  "success": true,
  "data": {
    "uploader_info": {
      "uploader": "单依纯",
      "uploader_id": "20713882"
    },
    "video_count": 3,
    "video_details": [...]
  }
}
```

### 测试 2：在 Bot 中测试

在 Bot 对话框中输入：
```
帮我获取这个 UP 主的信息：https://space.bilibili.com/20713882
```

---

## 📊 添加输出解析（可选）

### 代码节点配置

在 API 连接器后添加 **代码** 节点：

**语言**: Python

**代码**:
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
    uploader = data.get('uploader_info', {})
    videos = data.get('video_details', [])
    
    result = {
        'status': 'success',
        'uploader_name': uploader.get('uploader', ''),
        'uploader_uid': uploader.get('uploader_id', ''),
        'total_videos': data.get('video_count', 0),
        'videos': []
    }
    
    for v in videos[:5]:
        result['videos'].append({
            'title': v.get('title', ''),
            'duration': v.get('duration_string', ''),
            'views': f"{v.get('view_count', 0):,}",
            'likes': f"{v.get('like_count', 0):,}",
            'upload_date': v.get('upload_date', '')
        })
    
    return result
```

---

## 🤖 配置 Bot 人设

在 **人设与回复逻辑** 中添加：

```markdown
# 角色
你是 B 站视频数据助手，帮助用户获取 UP 主信息和视频详情。

# 技能
- 获取 UP 主基本信息（名称、UID）
- 获取 UP 主视频列表
- 获取视频详细数据（播放量、点赞数、评论数等）

# 工作流程
1. 用户提供 UP 主主页 URL
2. 调用 Bilibili Uploader Info API
3. 格式化返回结果

# 输出格式
【UP 主信息】
名称：{uploader_name}
UID: {uploader_uid}
视频总数：{total_videos}

【视频列表】
1. {title}
   时长：{duration}
   播放：{views}
   点赞：{likes}
   上传：{upload_date}
```

---

## ⚠️ 防火墙配置

### 检查防火墙状态

```bash
# Ubuntu/Debian
sudo ufw status

# 如果未开放 8001 端口
sudo ufw allow 8001/tcp
sudo ufw reload
```

### 云服务器安全组

如果你使用的是云服务器（阿里云、腾讯云等）：

1. 登录云服务商控制台
2. 找到 **安全组** 或 **防火墙** 设置
3. 添加入站规则：
   - 端口：`8001`
   - 协议：`TCP`
   - 来源：`0.0.0.0/0`（允许所有 IP）

---

## 🔒 安全建议

### 1. 使用 HTTPS（推荐）

目前使用 HTTP，建议配置 HTTPS：

```bash
# 安装 Nginx
sudo apt install nginx

# 配置反向代理
sudo nano /etc/nginx/sites-available/coze-api
```

Nginx 配置：
```nginx
server {
    listen 80;
    server_name 1.12.64.197;
    
    location /api/ {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 2. 添加 API Key 认证

在 API 请求中添加认证：

**Coze Headers 配置**:
```
X-API-Key: your-secret-key
```

**API 验证**:
在 `main.py` 中添加验证逻辑。

### 3. Cookie 管理

**建议**:
- 将 Cookie 存储为 Bot 变量
- 定期更新 Cookie
- 不要公开分享 Cookie

---

## 📱 在 Coze 中使用

### 示例对话

**用户**:
```
获取单依纯的 UP 主信息
```

**Bot**:
```
【UP 主信息】
名称：单依纯
UID: 20713882
视频总数：3

【视频列表】

1. 【单依纯《还有什么更好的》】MV
   时长：3:46
   播放：425,066
   点赞：30,640
   上传：20260302

2. 变个魔术，我们二巡见
   时长：0:15
   播放：505,263
   点赞：34,462
   上传：20260225

3. 【单依纯《我表示理解》】2026 我表示理解万岁！
   时长：3:20
   播放：255,513
   点赞：17,372
   上传：20260217
```

---

## 🔧 故障排查

### 问题 1：连接超时

**症状**: `Connection timeout`

**解决**:
1. 检查服务是否运行：
   ```bash
   docker ps | grep coze-bilibili-api
   ```

2. 检查防火墙：
   ```bash
   sudo ufw status
   ```

3. 测试公网访问：
   ```bash
   curl http://1.12.64.197:8001/health
   ```

### 问题 2：412 错误

**症状**: `HTTP Error 412`

**解决**: 添加 Cookie 参数

### 问题 3：Coze 无法连接

**症状**: API 测试失败

**解决**:
1. 确认 URL 正确：`http://1.12.64.197:8001/api/uploader/info`
2. 检查 Coze 是否能访问外网
3. 尝试在本地浏览器访问 API

---

## 📚 相关文档

| 文档 | 链接 |
|------|------|
| GitHub 仓库 | https://github.com/Kennyuy/coze-bilibili-api |
| 完整配置指南 | COZE_SETUP_GUIDE.md |
| API 文档 | COZE_API_GUIDE.md |
| 快速开始 | README_COZE.md |

---

## ✅ 配置检查清单

- [x] API 服务运行中
- [x] 公网 IP 可访问 (1.12.64.197)
- [x] 端口 8001 已开放
- [ ] 在 Coze 中配置 API 连接器
- [ ] 测试 API 连接
- [ ] 添加输出解析（可选）
- [ ] 配置 Bot 人设
- [ ] 发布 Bot

---

**现在可以在 Coze 中配置使用了！** 🎉
