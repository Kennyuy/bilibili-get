# Coze Bilibili API - 快速开始

## ✅ 项目状态

- **GitHub**: https://github.com/Kennyuy/coze-bilibili-api
- **API 状态**: 运行中 (端口 8001)
- **测试通过**: ✅ (单依纯 UID: 20713882)

---

## 🚀 5 分钟在 Coze 中配置

### 步骤 1：添加 API 连接器

1. 打开 Coze Bot 编辑页面
2. 点击 **工作流** → **+** → **API 连接器**
3. 点击 **添加 API**

### 步骤 2：填写 API 信息

```
名称：Bilibili Uploader Info
方法：POST
URL: http://your-server-ip:8001/api/uploader/info
```

### 步骤 3：配置请求体

```json
{
  "uploader_url": "{{input.uploader_url}}",
  "max_videos": "{{input.max_videos}}",
  "get_details": "{{input.get_details}}",
  "cookie": "{{input.cookie}}"
}
```

### 步骤 4：添加输入参数

| 参数 | 类型 | 必填 |
|------|------|------|
| `uploader_url` | string | ✅ |
| `max_videos` | number | ❌ |
| `get_details` | boolean | ❌ |
| `cookie` | string | ❌ |

### 步骤 5：测试

输入测试数据：
```json
{
  "uploader_url": "https://space.bilibili.com/20713882",
  "max_videos": 3,
  "get_details": true
}
```

---

## 📋 API 输入输出

### 输入

```json
{
  "uploader_url": "https://space.bilibili.com/20713882",
  "max_videos": 5,
  "get_details": true,
  "cookie": "SESSDATA=xxx; bili_jct=xxx"
}
```

### 输出

```json
{
  "success": true,
  "data": {
    "uploader_info": {
      "uploader": "单依纯",
      "uploader_id": "20713882"
    },
    "video_details": [
      {
        "title": "视频标题",
        "view_count": 425066,
        "like_count": 30640,
        "duration_string": "3:46"
      }
    ]
  }
}
```

---

## 📁 文档

| 文档 | 说明 |
|------|------|
| [COZE_SETUP_GUIDE.md](COZE_SETUP_GUIDE.md) | **完整配置指南** |
| [DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md) | 部署总结 |
| [COZE_API_GUIDE.md](COZE_API_GUIDE.md) | API 文档 |

---

## ⚠️ 注意事项

1. **Cookie**: 建议配置 B 站 Cookie（提高成功率）
2. **外网访问**: 确保 Coze 能访问你的 API 服务
3. **请求限制**: 建议 max_videos ≤ 10

---

## 🎯 完整教程

查看详细配置指南：
https://github.com/Kennyuy/coze-bilibili-api/blob/main/COZE_SETUP_GUIDE.md
