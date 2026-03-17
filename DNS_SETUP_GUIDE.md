# DNS 配置指南 - bilibili.kenny.help

## ✅ Nginx 配置完成

**本地测试**: ✅ 通过  
**Nginx 状态**: 运行中

---

## 🌐 第一步：配置 DNS 解析

### 方案 A：使用域名管理面板（推荐）

登录你的域名服务商（如阿里云、腾讯云、GoDaddy 等），添加以下 DNS 记录：

| 记录类型 | 主机记录 | 记录值 | TTL |
|---------|---------|--------|-----|
| `A` | `bilibili` | `1.12.64.197` | 10 分钟 |

### 具体步骤

#### 阿里云域名

1. 登录阿里云控制台
2. 进入 **域名与网站** → **域名**
3. 找到 `kenny.help`，点击 **解析**
4. 点击 **添加记录**
5. 填写：
   - 记录类型：`A`
   - 主机记录：`bilibili`
   - 记录值：`1.12.64.197`
   - TTL：`10 分钟`
6. 点击 **确认**

#### 腾讯云域名

1. 登录腾讯云控制台
2. 进入 **域名服务** → **域名解析**
3. 找到 `kenny.help`，点击 **解析**
4. 点击 **添加记录**
5. 填写：
   - 记录类型：`A`
   - 主机记录：`bilibili`
   - 记录值：`1.12.64.197`
   - TTL：`10 分钟`
6. 点击 **确认**

#### Cloudflare

1. 登录 Cloudflare
2. 选择 `kenny.help` 域名
3. 点击 **DNS** → **Add record**
4. 填写：
   - Type: `A`
   - Name: `bilibili`
   - IPv4 address: `1.12.64.197`
   - Proxy: `DNS only` (灰色云朵)
5. 点击 **Save**

---

## ⏱️ DNS 生效时间

- **国内 DNS**: 通常 5-30 分钟
- **国际 DNS**: 通常 10-60 分钟
- **最长**: 48 小时（很少见）

---

## 🧪 第二步：验证 DNS 解析

### 方法 1：使用 ping 命令

```bash
ping bilibili.kenny.help
```

应该显示：
```
PING bilibili.kenny.help (1.12.64.197) ...
```

### 方法 2：使用 nslookup

```bash
nslookup bilibili.kenny.help
```

应该显示：
```
Name:   bilibili.kenny.help
Address: 1.12.64.197
```

### 方法 3：在线工具

访问以下网站查询 DNS  propagation：
- https://www.whatsmydns.net/
- https://dnschecker.org/

---

## 🔧 第三步：测试 API 访问

### 本地测试

```bash
# 测试健康检查
curl http://bilibili.kenny.help/health

# 测试 API
curl -X POST http://bilibili.kenny.help/api/uploader/info \
  -H "Content-Type: application/json" \
  -d '{
    "uploader_url": "https://space.bilibili.com/20713882",
    "max_videos": 3,
    "get_details": true
  }'
```

### 浏览器测试

访问：
- http://bilibili.kenny.help/health
- http://bilibili.kenny.help/docs (API 文档)

---

## 🔒 第四步：配置 HTTPS（推荐）

### 使用 Let's Encrypt 免费证书

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx -y

# 获取证书
sudo certbot --nginx -d bilibili.kenny.help --email admin@kenny.help --agree-tos --redirect
```

按照提示完成验证后，会自动配置 HTTPS。

### 配置后访问

- **HTTP**: http://bilibili.kenny.help (自动跳转到 HTTPS)
- **HTTPS**: https://bilibili.kenny.help

---

## 🎯 第五步：更新 Coze 配置

### 新的 API 地址

将 Coze 中的 API URL 更新为：

```
https://bilibili.kenny.help/api/uploader/info
```

### 完整配置

| 字段 | 值 |
|------|-----|
| **名称** | `Bilibili Uploader Info` |
| **方法** | `POST` |
| **URL** | `https://bilibili.kenny.help/api/uploader/info` |
| **Headers** | `Content-Type: application/json` |

---

## 📊 Nginx 配置详情

### 配置文件位置

```
/etc/nginx/sites-available/bilibili.kenny.help
```

### 配置内容

```nginx
server {
    listen 80;
    server_name bilibili.kenny.help;
    
    # 日志文件
    access_log /var/log/nginx/bilibili.kenny.help-access.log;
    error_log /var/log/nginx/bilibili.kenny.help-error.log;
    
    # 代理到 API 服务
    location / {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 超时设置
        proxy_connect_timeout 120s;
        proxy_send_timeout 120s;
        proxy_read_timeout 120s;
        
        # 缓冲区设置
        proxy_buffer_size 128k;
        proxy_buffers 4 256k;
        proxy_busy_buffers_size 256k;
    }
    
    # 健康检查端点
    location /health {
        proxy_pass http://localhost:8001/health;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🔧 Nginx 管理命令

```bash
# 查看状态
sudo systemctl status nginx

# 重启
sudo systemctl restart nginx

# 重新加载配置
sudo systemctl reload nginx

# 停止
sudo systemctl stop nginx

# 查看日志
sudo tail -f /var/log/nginx/bilibili.kenny.help-access.log
sudo tail -f /var/log/nginx/bilibili.kenny.help-error.log
```

---

## ⚠️ 故障排查

### 问题 1：DNS 不生效

**检查**:
```bash
ping bilibili.kenny.help
```

**解决**:
- 等待 DNS 生效（最多 48 小时）
- 检查 DNS 配置是否正确
- 清除本地 DNS 缓存

### 问题 2：Nginx 无法访问

**检查**:
```bash
sudo systemctl status nginx
sudo nginx -t
```

**解决**:
```bash
sudo systemctl restart nginx
```

### 问题 3：502 Bad Gateway

**原因**: API 服务未运行

**检查**:
```bash
docker ps | grep coze-bilibili-api
```

**解决**:
```bash
cd /home/ubuntu/.openclaw/workspace/projects/coze-bilibili-api
docker compose up -d
```

---

## ✅ 检查清单

- [x] Nginx 安装并配置
- [ ] DNS 解析配置完成
- [ ] DNS 解析生效（ping 测试通过）
- [ ] API 访问测试通过
- [ ] (可选) HTTPS 证书配置
- [ ] Coze API URL 更新

---

## 📞 获取帮助

**查看日志**:
```bash
sudo tail -f /var/log/nginx/bilibili.kenny.help-error.log
```

**测试配置**:
```bash
sudo nginx -t
```

---

**配置完成后，记得在 Coze 中更新 API URL！** 🎉
