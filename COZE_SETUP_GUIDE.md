# Coze 插件配置完整指南

## ✅ 项目已上传

**GitHub 仓库**: https://github.com/Kennyuy/coze-bilibili-api

---

## 📋 在 Coze 中配置 API 插件

### 方式一：使用 API 连接器（推荐）

#### 步骤 1：创建 Bot

1. 访问 https://www.coze.cn
2. 点击 **创建 Bot**
3. 填写 Bot 名称和描述
4. 点击 **创建**

#### 步骤 2：添加 API 连接器

1. 在 Bot 编辑页面，点击 **工作流** 标签
2. 点击 **+** 添加节点
3. 选择 **API 连接器**
4. 点击 **添加 API**

#### 步骤 3：配置 API 信息

| 字段 | 值 |
|------|-----|
| **名称** | `Bilibili Uploader Info` |
| **描述** | `获取 B 站 UP 主信息及视频详情` |
| **方法** | `POST` |
| **URL** | `http://your-server-ip:8001/api/uploader/info` |

> ⚠️ **注意**: 将 `your-server-ip` 替换为你的服务器 IP 地址

#### 步骤 4：配置 Headers

点击 **Headers**，添加：

| Key | Value |
|-----|-------|
| `Content-Type` | `application/json` |

#### 步骤 5：配置请求体

点击 **Body**，选择 **JSON**，输入：

```json
{
  "uploader_url": "{{input.uploader_url}}",
  "max_videos": "{{input.max_videos}}",
  "get_details": "{{input.get_details}}",
  "cookie": "{{input.cookie}}"
}
```

#### 步骤 6：定义输入参数

点击 **输入**，添加以下参数：

| 参数名 | 类型 | 必填 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `uploader_url` | string | ✅ | - | UP 主主页 URL |
| `max_videos` | number | ❌ | 5 | 最大视频数 |
| `get_details` | boolean | ❌ | true | 是否获取详情 |
| `cookie` | string | ❌ | - | B 站 Cookie |

#### 步骤 7：测试 API

1. 点击 **测试** 按钮
2. 输入测试数据：
   ```json
   {
     "uploader_url": "https://space.bilibili.com/20713882",
     "max_videos": 3,
     "get_details": true,
     "cookie": "SESSDATA=xxx; bili_jct=xxx"
   }
   ```
3. 点击 **运行测试**
4. 查看返回结果

#### 步骤 8：添加输出解析节点

1. 在 API 连接器后添加 **代码** 节点
2. 选择 **Python**
3. 输入以下代码：

```python
def main(args: dict) -> dict:
    """解析 B 站 UP 主信息 API 响应"""
    response = args.get('api_response', {})
    
    # 错误处理
    if not response.get('success'):
        return {
            'status': 'error',
            'message': response.get('error', '请求失败')
        }
    
    data = response.get('data', {})
    uploader = data.get('uploader_info', {})
    videos = data.get('video_details', [])
    
    # 构建输出
    result = {
        'status': 'success',
        'uploader_name': uploader.get('uploader', ''),
        'uploader_uid': uploader.get('uploader_id', ''),
        'total_videos': data.get('video_count', 0),
        'videos': []
    }
    
    # 处理视频列表
    for v in videos[:5]:  # 最多返回 5 个
        result['videos'].append({
            'title': v.get('title', ''),
            'duration': v.get('duration_string', ''),
            'views': f"{v.get('view_count', 0):,}",
            'likes': f"{v.get('like_count', 0):,}",
            'comments': f"{v.get('comment_count', 0):,}",
            'upload_date': v.get('upload_date', ''),
            'tags': ', '.join(v.get('tags', []))
        })
    
    return result
```

4. 点击 **保存**

#### 步骤 9：配置 Bot 人设

在 **人设与回复逻辑** 中添加：

```markdown
# 角色
你是一个 B 站视频数据助手，可以帮助用户获取 UP 主信息和视频详情。

# 技能
- 获取 UP 主基本信息
- 获取 UP 主视频列表
- 获取视频详细数据（播放量、点赞数等）

# 工作流程
1. 用户提供 UP 主主页 URL
2. 调用 API 获取数据
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
   评论：{comments}
   上传：{upload_date}
   标签：{tags}
```

#### 步骤 10：发布 Bot

1. 点击右上角 **发布**
2. 选择发布平台
3. 点击 **确认发布**

---

### 方式二：使用插件市场（未来）

如果你的 API 需要公开给其他用户使用，可以：

1. 将 API 部署到公网
2. 在 Coze 插件市场提交插件
3. 等待审核通过
4. 用户可以直接添加插件

---

## 🔧 服务器配置

### 1. 确保 API 可访问

**检查服务状态**:
```bash
docker ps | grep coze-bilibili-api
```

**查看日志**:
```bash
docker logs coze-bilibili-api -f
```

### 2. 配置外网访问（如果需要）

**方案 A：使用服务器公网 IP**

1. 确保服务器防火墙开放 8001 端口
   ```bash
   sudo ufw allow 8001
   ```

2. 在 Coze 中使用公网 IP：
   ```
   http://your-server-public-ip:8001/api/uploader/info
   ```

**方案 B：使用内网穿透**

如果使用本地开发环境，可以使用 ngrok：

```bash
# 安装 ngrok
npm install -g ngrok

# 启动内网穿透
ngrok http 8001
```

然后使用 ngrok 提供的 URL。

---

## 📊 完整示例

### 用户输入
```
帮我获取这个 UP 主的信息：https://space.bilibili.com/20713882
```

### Bot 处理流程
1. 提取 URL
2. 调用 API 连接器
3. 解析返回数据
4. 格式化输出

### Bot 输出
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
   评论：1,869
   上传：20260302
   标签：单依纯，MV，还有什么更好的

2. 变个魔术，我们二巡见
   时长：0:15
   播放：505,263
   点赞：34,462
   评论：1,413
   上传：20260225
   标签：单依纯，纯妹妹巡回演唱会

3. 【单依纯《我表示理解》】2026 我表示理解万岁！
   时长：3:20
   播放：255,513
   点赞：17,372
   评论：946
   上传：20260217
   标签：单依纯，我表示理解
```

---

## ⚠️ 注意事项

### 1. Cookie 配置

**为什么需要 Cookie**:
- B 站反爬机制严格
- 无 Cookie 可能返回 412 错误

**如何获取 Cookie**:
1. 访问 https://www.bilibili.com
2. 登录账号
3. F12 → Network → 刷新
4. 复制 `Cookie` 字段

**在 Coze 中使用**:
- 可以将 Cookie 设置为 Bot 的变量
- 或者每次调用时传入

### 2. 错误处理

常见错误及解决方案：

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `HTTP Error 412` | Cookie 过期 | 更新 Cookie |
| `Request is rejected` | 无 Cookie | 添加 Cookie 参数 |
| `Timeout` | 视频太多 | 减少 max_videos |
| `Connection refused` | 服务未启动 | 检查 Docker 容器 |

### 3. 性能优化

**建议配置**:
- `max_videos`: 5-10（避免过多）
- `get_details`: 根据需要选择
- 添加结果缓存机制

---

## 📁 项目文件

上传到 GitHub 的文件：

```
coze-bilibili-api/
├── main.py                      # API 主程序 ✅
├── config.py                    # 配置文件 ✅
├── requirements.txt             # Python 依赖 ✅
├── Dockerfile                   # Docker 配置 ✅
├── docker-compose.yml           # Docker Compose ✅
├── bilibili_uploader_crawler.py # UP 主爬取脚本 ✅
├── README.md                    # 项目说明 ✅
├── COZE_API_GUIDE.md           # API 文档 ✅
├── COZE_SETUP_GUIDE.md         # 本指南 ✅
├── DEPLOYMENT_SUMMARY.md       # 部署总结 ✅
├── .gitignore                  # Git 忽略文件 ✅
├── .env.example                # 环境变量示例 ✅
├── start.sh                    # 启动脚本 ✅
└── test_api.py                 # 测试脚本 ✅
```

---

## 🚀 快速开始

### 1. 部署 API 服务

```bash
cd /home/ubuntu/.openclaw/workspace/projects/coze-bilibili-api
docker compose up -d
```

### 2. 在 Coze 中配置

按照上面的步骤配置 API 连接器

### 3. 测试

在 Coze Bot 中输入：
```
获取 UP 主信息：https://space.bilibili.com/20713882
```

---

## 📞 获取帮助

- **GitHub Issues**: https://github.com/Kennyuy/coze-bilibili-api/issues
- **API 文档**: http://your-server:8001/docs

---

**配置完成！现在可以在 Coze 中使用 B 站 UP 主信息 API 了！** 🎉
