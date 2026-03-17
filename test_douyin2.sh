#!/bin/bash

# 简化 Cookie（只保留关键字段）
DOUYIN_COOKIE="ttwid=1%7CBXbqnspE4jbHfOSOJ-6bQ-qwxepl7rQbIi_Gs6rYGNE%7C1773470270%7Cb2bc10294bf951ba6efc6e013dc1e8cc9524a120b5d71d90509c5de5d9f8ed3f; sessionid=e09948a297652a001e7dc31124a42770; sid_tt=e09948a297652a001e7dc31124a42770; uid_tt=5e739d763440b811ba813e1803bd37fa"

# 抖音视频 URL（简化格式）
VIDEO_URL="https://www.douyin.com/video/7598365104291302675"

# 创建 JSON 文件
cat > /tmp/douyin_test2.json << EOF
{
  "url": "$VIDEO_URL",
  "platform": "douyin",
  "action": "info",
  "cookie": "$DOUYIN_COOKIE"
}
EOF

# 发送请求
echo "🧪 测试抖音视频（简化 URL + Cookie）..."
curl -s -X POST http://localhost:8001/api/coze/webhook \
  -H "Content-Type: application/json" \
  -d @/tmp/douyin_test2.json | jq .

# 清理
rm -f /tmp/douyin_test2.json
