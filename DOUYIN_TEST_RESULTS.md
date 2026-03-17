# 抖音 API 测试结果

## 测试状态

| 项目 | 状态 | 说明 |
|------|------|------|
| **API 代码** | ✅ 完成 | 支持抖音平台 |
| **Cookie 格式** | ✅ 支持 | 可直接传入 Cookie 字符串 |
| **实际测试** | ⚠️ 需要新鲜 Cookie | 抖音反爬严格 |

---

## 测试结果

### ❌ 当前 Cookie 问题

```json
{
  "success": false,
  "error": "WARNING: [Douyin] 7598365104291302675: Failed to parse JSON\nERROR: [Douyin] 7598365104291302675: Fresh cookies (not necessarily logged in) are needed"
}
```

**原因**:
1. Cookie 已过期
2. 抖音需要登录状态的 Cookie
3. 抖音反爬机制严格

---

## 解决方案

### 1. 获取新鲜 Cookie

**步骤**:
1. 打开浏览器无痕模式
2. 访问 https://www.douyin.com
3. **登录账号**
4. 打开要访问的视频
5. F12 → Network → 刷新
6. 复制最新的 `Cookie` 字段

### 2. 使用正确的 URL 格式

**推荐格式**:
```
https://www.douyin.com/video/7598365104291302675
```

**不支持的格式**:
```
https://www.douyin.com/jingxuan?modal_id=7598365104291302675
```

### 3. 必需的 Cookie 字段

```
ttwid=xxx; sessionid=xxx; sid_tt=xxx; uid_tt=xxx
```

---

## API 使用示例

### 请求格式

```json
{
  "url": "https://www.douyin.com/video/7598365104291302675",
  "platform": "douyin",
  "action": "info",
  "cookie": "ttwid=xxx; sessionid=xxx; sid_tt=xxx"
}
```

### 预期响应（成功时）

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

## 对比：哔哩哔哩

| 平台 | Cookie 有效期 | 反爬强度 | 测试状态 |
|------|------------|---------|---------|
| **哔哩哔哩** | 较长（数周） | 中等 | ✅ 通过 |
| **抖音** | 较短（数天） | 严格 | ⚠️ 需新鲜 Cookie |

---

## 建议

1. **使用 B 站测试**: 哔哩哔哩 API 已验证可用
2. **抖音 Cookie 更新**: 每次使用前重新获取 Cookie
3. **错误处理**: 在 Coze 工作流中添加错误处理逻辑

---

## 测试脚本

```bash
# 运行测试
./test_douyin2.sh

# 查看日志
docker logs coze-bilibili-api --tail=50
```

---

## 更新 Cookie 后测试

```bash
# 1. 更新 douyin_cookies.txt 文件
# 2. 重新运行测试
./test_douyin2.sh
```
