# 快速开始指南

## 🚀 5 分钟快速部署

### 方法 1: 使用现有 JSON URL（最简单）

如果您已有视频 JSON 文件的 URL：

1. **安装插件**
   ```bash
   # 将插件文件夹复制到 AstrBot 的 data/plugins 目录
   cp -r astrbot_plugin_random_videos /path/to/astrbot/data/plugins/
   ```

2. **配置插件**
   - 登录 AstrBot 管理面板
   - 找到"随机视频插件"配置
   - 设置 `video_json_url` 为您的 JSON URL
   - 保存配置

3. **重启 AstrBot**

4. **测试使用**
   ```
   发送: /rv
   Bot 会回复一个随机视频
   ```

### 方法 2: 使用 OSS 自动同步（推荐）

如果您的视频存储在阿里云 OSS：

#### Step 1: 配置 OSS 同步脚本

```bash
# 进入 scripts 目录
cd scripts

# 一键安装配置（推荐）
python setup.py

# 按提示编辑 .env 文件，填写您的 OSS 配置
```

或手动配置：
```bash
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env 文件
```

#### Step 2: 运行同步

```bash
python sync_oss_videos.py
```

这会在 `scripts/` 目录生成 `videos.json` 文件。

#### Step 3: 部署 JSON 文件

**选项 A: 上传到 OSS**
```bash
# 上传到 OSS
ossutil cp videos.json oss://your-bucket/videos.json
ossutil set-acl oss://your-bucket/videos.json public-read

# 使用 URL
# https://your-bucket.oss-cn-hangzhou.aliyuncs.com/videos.json
# 或 https://your-cdn-domain.com/videos.json
```

**选项 B: GitHub Gist**
1. 访问 https://gist.github.com/
2. 创建新 Gist，粘贴 `videos.json` 内容
3. 复制 Raw URL

**选项 C: 自己的服务器**
```bash
scp videos.json user@server:/var/www/html/videos.json
```

#### Step 4: 配置 AstrBot 插件

在 AstrBot 管理面板中设置 `video_json_url` 为您部署的 JSON URL。

## 📋 JSON 格式要求

插件支持 3 种 JSON 格式：

**格式 1: 简单数组（推荐）**
```json
[
  "https://example.com/video1.mp4",
  "https://example.com/video2.mp4",
  "https://example.com/video3.mp4"
]
```

**格式 2: 对象格式**
```json
{
  "videos": [
    "https://example.com/video1.mp4",
    "https://example.com/video2.mp4"
  ]
}
```

**格式 3: 键值对**
```json
{
  "video1": "https://example.com/video1.mp4",
  "video2": "https://example.com/video2.mp4"
}
```

## 🎮 使用命令

| 命令 | 别名 | 说明 |
|------|------|------|
| `/randomvideo` | `/rv`, `/随机视频` | 随机播放一个视频 |
| `/videoinfo` | `/视频信息` | 查看视频库信息 |
| `/reloadvideos` | `/重载视频` | 重新加载视频列表（管理员） |

## 🔧 OSS 配置示例

### 基础配置（使用 OSS 默认域名）

```env
OSS_ACCESS_KEY_ID=LTAI5txxxxxx
OSS_ACCESS_KEY_SECRET=aBcDeFxxxxxx
OSS_ENDPOINT=oss-cn-hangzhou.aliyuncs.com
OSS_BUCKET_NAME=my-videos
OSS_PREFIX=videos/
```

生成的链接示例：
```
https://my-videos.oss-cn-hangzhou.aliyuncs.com/videos/sample.mp4
```

### 进阶配置（使用 CDN，节省流量）

```env
OSS_ACCESS_KEY_ID=LTAI5txxxxxx
OSS_ACCESS_KEY_SECRET=aBcDeFxxxxxx
OSS_ENDPOINT=oss-cn-hangzhou.aliyuncs.com
OSS_BUCKET_NAME=my-videos
OSS_PREFIX=videos/

# 使用 Cloudflare CDN
OSS_CUSTOM_DOMAIN=https://cdn.example.com
```

生成的链接示例：
```
https://cdn.example.com/videos/sample.mp4
```

**优势：**
- ✅ 通过 Cloudflare 免费 CDN 节省 OSS 流量费用
- ✅ 全球加速，用户访问更快
- ✅ 支持 HTTPS

## 🔄 自动同步设置

### Linux/macOS (定时任务)

```bash
# 编辑 crontab
crontab -e

# 每天凌晨 2 点自动同步
0 2 * * * cd /path/to/scripts && python3 sync_oss_videos.py >> sync.log 2>&1
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务 → 名称: "OSS 视频同步"
3. 触发器: 每天 2:00 AM
4. 操作: 启动程序
   - 程序: `python`
   - 参数: `sync_oss_videos.py`
   - 起始于: `D:\path\to\scripts`

## 📊 工作流程图

```
┌─────────────────┐
│  阿里云 OSS     │
│  (存储视频)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ sync_oss_videos │  ← 运行同步脚本
│    (Python)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  videos.json    │  ← 生成 JSON 文件
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  上传到服务器   │  ← GitHub/OSS/自己的服务器
│  (提供 URL)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  AstrBot 插件   │  ← 配置 video_json_url
│  (加载并播放)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Discord/QQ 等  │  ← 用户使用 /rv 命令
│  (随机视频)     │
└─────────────────┘
```

## ❓ 常见问题速查

**Q: 视频不播放？**
```bash
# 1. 检查配置
在 AstrBot 面板查看 video_json_url 是否正确

# 2. 测试 JSON URL 是否可访问
curl https://your-json-url.com/videos.json

# 3. 重新加载插件
发送: /reloadvideos
```

**Q: OSS 同步失败？**
```bash
# 检查凭证
确认 .env 文件中的 OSS_ACCESS_KEY_ID 和 OSS_ACCESS_KEY_SECRET

# 检查权限
确认 AccessKey 具有读取 Bucket 的权限

# 查看详细错误
python sync_oss_videos.py
```

**Q: 如何添加新视频？**
```bash
# 方法 1: OSS 自动同步
1. 上传视频到 OSS
2. 运行: python sync_oss_videos.py
3. 重新部署 videos.json
4. 在 AstrBot 中发送: /reloadvideos

# 方法 2: 手动编辑
1. 编辑 videos.json，添加新链接
2. 重新部署 JSON 文件
3. 在 AstrBot 中发送: /reloadvideos
```

**Q: Discord 视频播放和音频？**

✅ **完整支持**！插件在 Discord 上使用视频组件：
- 触发 Discord 原生媒体播放器
- 点击即可播放视频和音频
- 支持暂停、音量控制、全屏等功能
- 自动降级机制：如失败会使用链接（Discord 仍会嵌入预览）

**Q: Discord 按钮切换视频？**

目前 AstrBot 框架暂不支持 Discord 交互式按钮。使用斜杠命令：
- 发送 `/rv` 或 `/randomvideo` 获取新的随机视频
- 每次发送都会返回不同的视频（本轮不重复）

## 📚 详细文档

- **插件使用**: [README.md](README.md)
- **OSS 同步脚本**: [scripts/README.md](scripts/README.md)
- **完整使用示例**: [scripts/USAGE_EXAMPLE.md](scripts/USAGE_EXAMPLE.md)

## 🆘 获取帮助

如遇到问题：

1. **查看日志**: 检查 AstrBot 和同步脚本的日志
2. **查阅文档**: 阅读 README.md 和 USAGE_EXAMPLE.md
3. **提交 Issue**: 在 GitHub 仓库提交问题
4. **检查配置**: 确认所有配置项正确填写

## 🎉 开始使用

现在您已经了解了基本用法，选择适合您的方式开始使用吧！

**推荐流程：**
1. ✅ 配置 OSS 同步脚本
2. ✅ 运行同步生成 videos.json
3. ✅ 部署 JSON 到可访问的 URL
4. ✅ 配置 AstrBot 插件
5. ✅ 在聊天中测试 `/rv` 命令
6. ✅ 设置定时任务自动同步

祝您使用愉快！🚀
