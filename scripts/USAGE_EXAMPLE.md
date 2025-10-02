# OSS 视频同步脚本 - 使用示例

## 📝 完整使用流程示例

### 步骤 1: 配置阿里云 OSS

假设您的 OSS 配置如下：
- Bucket 名称: `my-video-bucket`
- 区域: 杭州 (oss-cn-hangzhou)
- 视频存储路径: `videos/`

### 步骤 2: 配置 .env 文件

```bash
cd scripts
cp .env.example .env
```

编辑 `.env` 文件：

```env
# 阿里云 OSS 配置
OSS_ACCESS_KEY_ID=LTAI5tGh4xxx
OSS_ACCESS_KEY_SECRET=aBcDeFg123xxx
OSS_ENDPOINT=oss-cn-hangzhou.aliyuncs.com
OSS_BUCKET_NAME=my-video-bucket

# 只扫描 videos/ 目录
OSS_PREFIX=videos/

# 使用 Cloudflare CDN（可选，推荐）
OSS_CUSTOM_DOMAIN=https://cdn.example.com

# 支持的视频格式
VIDEO_EXTENSIONS=.mp4,.avi,.mov,.mkv,.flv,.wmv,.webm,.m4v

# 输出文件
JSON_OUTPUT_FILE=videos.json
```

### 步骤 3: 安装依赖

**方法 1: 一键安装（推荐）**
```bash
python setup.py
```

此脚本会自动安装依赖并创建配置文件。

**方法 2: 手动安装**
```bash
pip install -r requirements.txt
```

### 步骤 4: 首次运行（空 JSON 文件）

```bash
python sync_oss_videos.py
```

**输出示例：**

```
============================================================
🚀 阿里云 OSS 视频同步工具
============================================================

✅ 成功连接到 OSS Bucket: my-video-bucket
🔍 开始扫描 OSS bucket...
   扫描路径: videos/
   ✓ 发现视频: videos/cat_funny.mp4
   ✓ 发现视频: videos/dog_playing.mp4
   ✓ 发现视频: videos/cute_baby.mp4

📊 扫描完成:
   总文件数: 5
   视频文件数: 3

ℹ️  JSON 文件不存在，将创建新文件: videos.json
📋 现有视频数量: 0

🆕 发现 3 个新视频:
   1. https://cdn.example.com/videos/cat_funny.mp4
   2. https://cdn.example.com/videos/cute_baby.mp4
   3. https://cdn.example.com/videos/dog_playing.mp4

✅ 成功保存到: videos.json

============================================================
✅ 同步完成！总共 3 个视频
============================================================
```

生成的 `videos.json` 文件：

```json
[
  "https://cdn.example.com/videos/cat_funny.mp4",
  "https://cdn.example.com/videos/cute_baby.mp4",
  "https://cdn.example.com/videos/dog_playing.mp4"
]
```

### 步骤 5: 上传新视频到 OSS

假设您上传了 2 个新视频到 OSS：
- `videos/bird_singing.mp4`
- `videos/fish_swimming.mp4`

### 步骤 6: 再次运行同步

```bash
python sync_oss_videos.py
```

**输出示例：**

```
============================================================
🚀 阿里云 OSS 视频同步工具
============================================================

✅ 成功连接到 OSS Bucket: my-video-bucket
🔍 开始扫描 OSS bucket...
   扫描路径: videos/
   ✓ 发现视频: videos/bird_singing.mp4
   ✓ 发现视频: videos/cat_funny.mp4
   ✓ 发现视频: videos/cute_baby.mp4
   ✓ 发现视频: videos/dog_playing.mp4
   ✓ 发现视频: videos/fish_swimming.mp4

📊 扫描完成:
   总文件数: 7
   视频文件数: 5

📋 现有视频数量: 3

🆕 发现 2 个新视频:
   1. https://cdn.example.com/videos/bird_singing.mp4
   2. https://cdn.example.com/videos/fish_swimming.mp4

✅ 成功保存到: videos.json

============================================================
✅ 同步完成！总共 5 个视频
============================================================
```

更新后的 `videos.json`：

```json
[
  "https://cdn.example.com/videos/bird_singing.mp4",
  "https://cdn.example.com/videos/cat_funny.mp4",
  "https://cdn.example.com/videos/cute_baby.mp4",
  "https://cdn.example.com/videos/dog_playing.mp4",
  "https://cdn.example.com/videos/fish_swimming.mp4"
]
```

## 🌐 部署 JSON 文件

### 方案 1: 上传到 OSS（推荐）

```bash
# 使用 ossutil 或 Web 控制台上传
ossutil cp videos.json oss://my-video-bucket/videos.json

# 设置公共读权限
ossutil set-acl oss://my-video-bucket/videos.json public-read
```

JSON URL: `https://cdn.example.com/videos.json`

### 方案 2: 使用 GitHub Gist

1. 访问 https://gist.github.com/
2. 创建新 Gist，粘贴 `videos.json` 内容
3. 点击 "Raw" 获取链接

JSON URL: `https://gist.githubusercontent.com/username/xxx/raw/videos.json`

### 方案 3: 自己的 Web 服务器

```bash
# 上传到服务器
scp videos.json user@server:/var/www/html/videos.json
```

JSON URL: `https://your-domain.com/videos.json`

## 🔧 在 AstrBot 中使用

1. 登录 AstrBot 管理面板
2. 找到 "随机视频插件" 配置
3. 设置 `video_json_url` 为您的 JSON 文件 URL：
   ```
   https://cdn.example.com/videos.json
   ```
4. 保存配置
5. 在聊天中发送 `/rv` 测试

## 🔄 设置定时同步

### Linux/macOS (crontab)

```bash
# 编辑 crontab
crontab -e

# 添加定时任务（每天凌晨 2 点同步）
0 2 * * * cd /path/to/scripts && /usr/bin/python3 sync_oss_videos.py >> sync.log 2>&1

# 每 6 小时同步一次
0 */6 * * * cd /path/to/scripts && /usr/bin/python3 sync_oss_videos.py >> sync.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 名称: "OSS 视频同步"
4. 触发器: 每天凌晨 2:00
5. 操作: 启动程序
   - 程序: `python`
   - 参数: `sync_oss_videos.py`
   - 起始于: `D:\path\to\scripts`
6. 完成

### 使用 GitHub Actions 自动同步并部署

创建 `.github/workflows/sync-videos.yml`：

```yaml
name: Sync OSS Videos

on:
  schedule:
    - cron: '0 2 * * *'  # 每天凌晨 2 点
  workflow_dispatch:  # 允许手动触发

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          cd scripts
          pip install -r requirements.txt

      - name: Create .env file
        run: |
          cd scripts
          cat > .env << EOF
          OSS_ACCESS_KEY_ID=${{ secrets.OSS_ACCESS_KEY_ID }}
          OSS_ACCESS_KEY_SECRET=${{ secrets.OSS_ACCESS_KEY_SECRET }}
          OSS_ENDPOINT=${{ secrets.OSS_ENDPOINT }}
          OSS_BUCKET_NAME=${{ secrets.OSS_BUCKET_NAME }}
          OSS_PREFIX=${{ secrets.OSS_PREFIX }}
          OSS_CUSTOM_DOMAIN=${{ secrets.OSS_CUSTOM_DOMAIN }}
          EOF

      - name: Sync videos
        run: |
          cd scripts
          python sync_oss_videos.py

      - name: Commit and push
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add scripts/videos.json
          git commit -m "Auto sync videos from OSS" || exit 0
          git push
```

在 GitHub 仓库设置中添加 Secrets：
- `OSS_ACCESS_KEY_ID`
- `OSS_ACCESS_KEY_SECRET`
- `OSS_ENDPOINT`
- `OSS_BUCKET_NAME`
- `OSS_PREFIX`
- `OSS_CUSTOM_DOMAIN`

## 📊 实际使用数据示例

### 场景：视频网站

**OSS 结构：**
```
my-video-bucket/
├── videos/
│   ├── 2024/
│   │   ├── 01/
│   │   │   ├── funny_cat_01.mp4
│   │   │   └── cute_dog_01.mp4
│   │   └── 02/
│   │       ├── baby_laugh.mp4
│   │       └── bird_singing.mp4
│   └── 2025/
│       └── 01/
│           └── new_year.mp4
```

**配置：**
```env
OSS_PREFIX=videos/
OSS_CUSTOM_DOMAIN=https://cdn.mysite.com
```

**生成的 JSON：**
```json
[
  "https://cdn.mysite.com/videos/2024/01/cute_dog_01.mp4",
  "https://cdn.mysite.com/videos/2024/01/funny_cat_01.mp4",
  "https://cdn.mysite.com/videos/2024/02/baby_laugh.mp4",
  "https://cdn.mysite.com/videos/2024/02/bird_singing.mp4",
  "https://cdn.mysite.com/videos/2025/01/new_year.mp4"
]
```

## ❓ 常见问题排查

### 问题 1: 连接 OSS 失败

**错误信息：**
```
❌ 连接 OSS 失败: The Access Key ID you provided does not exist
```

**解决方法：**
- 检查 `OSS_ACCESS_KEY_ID` 和 `OSS_ACCESS_KEY_SECRET` 是否正确
- 确认 AccessKey 是否已激活

### 问题 2: 权限不足

**错误信息：**
```
❌ 扫描 OSS 时出错: You have no right to access this object
```

**解决方法：**
- 确认 AccessKey 具有读取 Bucket 的权限
- 在 OSS 控制台检查 RAM 用户权限

### 问题 3: JSON 文件为空

**原因：**
- OSS 中没有视频文件
- `OSS_PREFIX` 配置错误
- 视频格式不在 `VIDEO_EXTENSIONS` 列表中

**解决方法：**
```bash
# 检查 OSS 中的文件
ossutil ls oss://my-video-bucket/videos/

# 调整配置
OSS_PREFIX=  # 清空，扫描整个 bucket
VIDEO_EXTENSIONS=.mp4,.avi,.mov,.mkv  # 添加更多格式
```

## 🎯 最佳实践

1. **使用 CDN 域名**：通过 Cloudflare 等免费 CDN 减少流量费用
2. **定期同步**：设置 cron job 每天自动同步
3. **备份 JSON**：在 Git 仓库中保留 `videos.json` 的历史版本
4. **监控日志**：将同步日志重定向到文件，方便排查问题
5. **测试环境**：先在测试环境验证，再部署到生产环境
