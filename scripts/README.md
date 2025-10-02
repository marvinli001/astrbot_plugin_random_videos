# OSS 视频同步脚本

自动扫描阿里云 OSS 中的视频文件，并同步到 `videos.json` 文件。

## 📋 功能特性

- ✅ 自动扫描 OSS bucket 中的所有视频文件
- ✅ 支持多种视频格式（mp4, avi, mov, mkv, flv, wmv, webm, m4v）
- ✅ 智能对比，只添加新视频链接
- ✅ 支持自定义 CDN 域名（如 Cloudflare CDN）
- ✅ 自动处理空文件和格式错误
- ✅ 支持指定 OSS 目录前缀
- ✅ 自动 URL 编码处理
- ✅ JSON 格式化输出（带换行和缩进）

## 🚀 快速开始

### 方法 1: 一键安装（推荐）

```bash
cd scripts
python setup.py
```

此脚本会自动：
- ✅ 安装 Python 依赖（oss2, python-dotenv）
- ✅ 创建 `.env` 配置文件（从 .env.example）
- ✅ 提示编辑配置信息

### 方法 2: 手动安装

**步骤 1：安装依赖**
```bash
cd scripts
pip install -r requirements.txt
```

**步骤 2：配置环境变量**
```bash
# 复制配置模板
cp .env.example .env

# 编辑配置文件
# Windows: notepad .env
# Linux/macOS: nano .env
```

**配置示例：**
```env
# 阿里云 OSS 配置（必填）
OSS_ACCESS_KEY_ID=your_access_key_id
OSS_ACCESS_KEY_SECRET=your_access_key_secret
OSS_ENDPOINT=oss-cn-hangzhou.aliyuncs.com
OSS_BUCKET_NAME=your_bucket_name

# OSS 路径配置（可选）
OSS_PREFIX=videos/

# 自定义访问域名（可选，推荐使用 CDN）
OSS_CUSTOM_DOMAIN=https://cdn.example.com

# 视频格式（可选，使用默认即可）
VIDEO_EXTENSIONS=.mp4,.avi,.mov,.mkv,.flv,.wmv,.webm,.m4v

# 输出文件（可选）
JSON_OUTPUT_FILE=videos.json
```

### 运行同步

```bash
python sync_oss_videos.py
```

## 📖 配置说明

### 必填配置

| 配置项 | 说明 | 示例 |
|--------|------|------|
| `OSS_ACCESS_KEY_ID` | 阿里云 AccessKey ID | `LTAI5t...` |
| `OSS_ACCESS_KEY_SECRET` | 阿里云 AccessKey Secret | `aBcD...` |
| `OSS_ENDPOINT` | OSS 区域节点 | `oss-cn-hangzhou.aliyuncs.com` |
| `OSS_BUCKET_NAME` | OSS Bucket 名称 | `my-videos` |

### 可选配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `OSS_PREFIX` | 只扫描特定目录 | 空（扫描整个 bucket） |
| `OSS_CUSTOM_DOMAIN` | 自定义 CDN 域名 | 空（使用 OSS 默认域名） |
| `VIDEO_EXTENSIONS` | 支持的视频格式 | `.mp4,.avi,.mov,...` |
| `JSON_OUTPUT_FILE` | 输出 JSON 文件名 | `videos.json` |

## 🌐 CDN 配置示例

### 使用 Cloudflare CDN

如果您通过 Cloudflare CDN 加速 OSS：

```env
OSS_CUSTOM_DOMAIN=https://cdn.example.com
```

脚本会生成如下格式的链接：
```
https://cdn.example.com/videos/sample.mp4
```

### 使用 OSS 默认域名

如果不配置 `OSS_CUSTOM_DOMAIN`，脚本会使用 OSS 默认域名：

```
https://my-bucket.oss-cn-hangzhou.aliyuncs.com/videos/sample.mp4
```

## 📁 输出格式

脚本会生成格式化的 JSON 文件：

```json
[
  "https://cdn.example.com/videos/video1.mp4",
  "https://cdn.example.com/videos/video2.mp4",
  "https://cdn.example.com/videos/video3.mp4"
]
```

## 🔧 工作流程

1. **连接 OSS**：使用配置的凭证连接到阿里云 OSS
2. **扫描视频**：遍历指定路径下的所有文件，筛选出视频文件
3. **生成链接**：
   - 如果配置了 `OSS_CUSTOM_DOMAIN`，使用自定义域名
   - 否则使用 OSS 默认域名
   - 自动处理 URL 编码
4. **加载现有数据**：读取 `videos.json`（如果存在）
5. **对比去重**：找出新增的视频链接
6. **保存更新**：将合并后的链接保存到 JSON 文件

## 🛡️ 错误处理

脚本具有完善的错误处理机制：

- ✅ 自动检测并提示缺少的依赖
- ✅ 验证必填配置项
- ✅ 处理空 JSON 文件
- ✅ 处理格式错误的 JSON（自动备份为 `.json.bak`）
- ✅ 捕获网络和 API 错误

## 📊 输出示例

```
============================================================
🚀 阿里云 OSS 视频同步工具
============================================================

✅ 成功连接到 OSS Bucket: my-videos
🔍 开始扫描 OSS bucket...
   扫描路径: videos/
   ✓ 发现视频: videos/demo1.mp4
   ✓ 发现视频: videos/demo2.mp4
   ✓ 发现视频: videos/demo3.mp4

📊 扫描完成:
   总文件数: 15
   视频文件数: 3

📋 现有视频数量: 1

🆕 发现 2 个新视频:
   1. https://cdn.example.com/videos/demo2.mp4
   2. https://cdn.example.com/videos/demo3.mp4

✅ 成功保存到: videos.json

============================================================
✅ 同步完成！总共 3 个视频
============================================================
```

## 🔄 定时任务

### Linux/macOS (crontab)

每天凌晨 2 点自动同步：

```bash
0 2 * * * cd /path/to/scripts && /usr/bin/python3 sync_oss_videos.py >> sync.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（如每天凌晨 2 点）
4. 操作：启动程序
   - 程序：`python`
   - 参数：`sync_oss_videos.py`
   - 起始于：`D:\path\to\scripts`

## 🔗 集成到插件

同步完成后，在 AstrBot 插件配置中设置 JSON 文件的访问 URL：

### 方案 1: 本地文件

将 `videos.json` 放到 Web 服务器，配置 URL：
```
https://your-domain.com/videos.json
```

### 方案 2: GitHub Gist

将 `videos.json` 上传到 GitHub Gist，使用 Raw URL：
```
https://gist.githubusercontent.com/username/xxx/raw/videos.json
```

### 方案 3: OSS 直链

将 `videos.json` 上传到 OSS，设置公共读权限：
```
https://your-bucket.oss-cn-hangzhou.aliyuncs.com/videos.json
```

## ⚙️ 高级用法

### 只扫描特定目录

```env
OSS_PREFIX=videos/2024/
```

### 添加自定义视频格式

```env
VIDEO_EXTENSIONS=.mp4,.avi,.mov,.ts,.m3u8
```

### 修改输出文件名

```env
JSON_OUTPUT_FILE=my_videos.json
```

## ❓ 常见问题

**Q: 第一次运行时 videos.json 不存在怎么办？**
A: 脚本会自动创建新文件，无需手动创建。

**Q: JSON 文件格式错误怎么办？**
A: 脚本会自动备份为 `.json.bak` 并重新生成。

**Q: 如何节省 OSS 流量费用？**
A: 配置 `OSS_CUSTOM_DOMAIN` 使用 Cloudflare 等免费 CDN。

**Q: 视频链接中有中文或特殊字符？**
A: 脚本会自动进行 URL 编码处理，无需担心。

## 📝 许可证

MIT License
