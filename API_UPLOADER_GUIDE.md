# B 站 UP 主信息爬取指南

## ✅ 功能说明

本 API 可以获取 B 站 UP 主主页信息及其视频详情，分为两步：

1. **获取 UP 主信息** - 用户名、UID、简介、粉丝数等
2. **获取视频详情** - 视频标题、链接、时长、播放量、点赞数、投币数等

---

## 📋 数据字段

### UP 主信息

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `uploader` | string | UP 主名称 | `"马克的技术工作坊"` |
| `uploader_id` | string | UP 主 ID | `"1815948385"` |
| `url` | string | 主页 URL | `"https://space.bilibili.com/1815948385"` |
| `total_videos` | int | 视频总数 | `30` |

### 视频列表

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `index` | int | 序号 | `1` |
| `title` | string | 视频标题 | `"从 LLM 到 Agent Skill..."` |
| `id` | string | 视频 ID | `"BV1E7wtzaEdq"` |
| `url` | string | 视频链接 | `"https://www.bilibili.com/video/BV1E7wtzaEdq"` |
| `duration` | int | 时长（秒） | `1951` |
| `thumbnail` | string | 封面图 | `"http://..."` |

### 视频详情

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `title` | string | 视频标题 | `"从 LLM 到 Agent Skill..."` |
| `id` | string | 视频 ID | `"BV1E7wtzaEdq"` |
| `url` | string | 视频链接 | `"https://www.bilibili.com/video/BV1E7wtzaEdq"` |
| `duration` | int | 时长（秒） | `1951` |
| `duration_string` | string | 时长字符串 | `"32:31"` |
| `upload_date` | string | 上传日期 | `"20260314"` |
| `description` | string | 视频简介 | `"AI 核心概念大串联..."` |
| `view_count` | int | 播放量 | `145546` |
| `like_count` | int | 点赞数 | `7788` |
| `comment_count` | int | 评论数 | `501` |
| `thumbnail` | string | 封面图 | `"http://..."` |
| `tags` | array | 标签 | `["AI", "教程"]` |

---

## 🚀 使用方法

### 方法 1：Python 脚本

```python
cd /home/ubuntu/.openclaw/workspace/projects/coze-bilibili-api
python3 bilibili_uploader_crawler.py
```

**配置参数**:
```python
# 在脚本中修改
uploader_url = "https://space.bilibili.com/1815948385"  # UP 主主页
max_videos = 3  # 获取视频数量
get_details = True  # 是否获取详情
```

**输出**:
- 控制台输出摘要
- JSON 文件：`bilibili_result.json`

---

### 方法 2：API 接口

**接口**: `POST /api/uploader/info`

**请求**:
```json
{
  "uploader_url": "https://space.bilibili.com/1815948385",
  "max_videos": 3,
  "get_details": true,
  "cookie": "SESSDATA=xxx; bili_jct=xxx"
}
```

**响应**:
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
        "title": "从 LLM 到 Agent Skill...",
        "id": "BV1E7wtzaEdq",
        "url": "https://www.bilibili.com/video/BV1E7wtzaEdq"
      }
    ],
    "video_details": [
      {
        "title": "从 LLM 到 Agent Skill...",
        "view_count": 145546,
        "like_count": 7788,
        "duration_string": "32:31"
      }
    ]
  }
}
```

---

## 📊 测试结果

### 测试 UP 主：马克的技术工作坊

**URL**: `https://space.bilibili.com/1815948385`

**获取结果**:

```json
{
  "uploader_info": {
    "uploader": "马克的技术工作坊",
    "uploader_id": "1815948385"
  },
  "videos": [
    {
      "title": "从 LLM 到 Agent Skill，一期视频带你打通底层逻辑！",
      "id": "BV1E7wtzaEdq",
      "url": "https://www.bilibili.com/video/BV1E7wtzaEdq"
    },
    {
      "title": "Midjourney 2025 完全使用教程",
      "id": "BV1PMcoeZEzE",
      "url": "https://www.bilibili.com/video/BV1PMcoeZEzE"
    },
    {
      "title": "NotebookLM 快速上手（2025）",
      "id": "BV1njcoepEsp",
      "url": "https://www.bilibili.com/video/BV1njcoepEsp"
    }
  ],
  "video_details": [
    {
      "title": "从 LLM 到 Agent Skill，一期视频带你打通底层逻辑！",
      "duration_string": "32:31",
      "view_count": 145546,
      "like_count": 7788,
      "comment_count": 501,
      "tags": ["AI", "教程", "Context", "Agent Skills"]
    }
  ]
}
```

---

## 🔧 自定义 UP 主

### 获取 UP 主 ID

1. 访问 UP 主主页
2. 复制 URL 中的数字 ID
   - `https://space.bilibili.com/1815948385` → ID: `1815948385`

### 修改脚本

编辑 `bilibili_uploader_crawler.py`:

```python
# 修改这一行
uploader_url = "https://space.bilibili.com/YOUR_UP_ID"
```

---

## ⚠️ 注意事项

1. **Cookie 有效期**: Cookie 会过期，需定期更新
2. **请求频率**: 建议设置延迟，避免触发反爬
3. **视频数量**: 获取大量视频时，建议分批处理
4. **数据缓存**: 建议缓存结果，避免重复请求

---

## 📁 文件说明

```
coze-bilibili-api/
├── bilibili_uploader_crawler.py  # UP 主爬取脚本 ✅
├── bilibili_result.json          # 爬取结果 ✅
├── API_UPLOADER_GUIDE.md         # 本文档 ✅
└── bilibili_cookies.txt          # Cookie 文件
```

---

## 🎯 下一步

### 集成到 Coze 工作流

1. **HTTP 请求节点**: 调用 API 接口
2. **代码节点**: 解析返回的 JSON 数据
3. **输出**: 展示 UP 主信息和视频数据

### 扩展功能

- [ ] 获取粉丝数、关注数
- [ ] 获取视频弹幕
- [ ] 获取评论数据
- [ ] 批量爬取多个 UP 主

---

**测试完成！API 已就绪！** 🎉
