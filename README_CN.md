# AstrBot 随机视频插件 v1.1.0

<div align="center">

![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)
![AstrBot](https://img.shields.io/badge/AstrBot-v4.x-green.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**一个功能强大的 AstrBot 随机视频播放插件**

支持 Discord 原生播放器 · 防重复播放 · OSS 自动同步

[快速开始](#-快速开始) · [功能特性](#-功能特性) · [Discord 指南](DISCORD_GUIDE.md) · [更新日志](CHANGELOG.md)

</div>

---

## 📋 目录

- [功能特性](#-功能特性)
- [快速开始](#-快速开始)
- [平台支持](#-平台支持)
- [命令列表](#-命令列表)
- [配置说明](#️-配置说明)
- [OSS 同步工具](#-oss-同步工具)
- [文档导航](#-文档导航)
- [常见问题](#-常见问题)
- [更新日志](#-更新日志)

---

## ✨ 功能特性

### 🎥 视频播放
- ✅ **Discord 原生播放器**：完整支持音视频播放、媒体控制
- ✅ **智能随机**：确保当前轮次不重复播放
- ✅ **自动轮次管理**：播放完所有视频后自动开始新一轮
- ✅ **会话隔离**：每个聊天独立的播放历史

### 🌐 多平台支持
- Discord（原生播放器 + 媒体控制）
- QQ / QQ 频道
- Telegram
- 微信平台
- 其他 AstrBot 支持的平台

### 🔧 OSS 自动同步
- 自动扫描阿里云 OSS bucket 中的视频
- 智能对比，只添加新视频
- 支持 Cloudflare CDN（节省流量）
- 支持多种视频格式
- 一键安装脚本

### 📊 数据管理
- 远程 JSON 加载
- 实时播放进度显示
- 管理员重载功能
- 支持多种 JSON 格式

---

## 🚀 快速开始

### 方法 1: 使用现有 JSON URL

```bash
# 1. 安装插件
将插件文件夹复制到 AstrBot 的 data/plugins 目录

# 2. 配置插件
在 AstrBot 管理面板设置 video_json_url

# 3. 重启 AstrBot

# 4. 使用
发送: /rv
```

### 方法 2: 使用 OSS 自动同步

```bash
# 1. 配置 OSS 同步
cd scripts
cp .env.example .env
# 编辑 .env 填写 OSS 配置

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行同步
python sync_oss_videos.py

# 4. 部署 JSON 文件
上传到 OSS/GitHub/服务器

# 5. 配置 AstrBot
设置 video_json_url 为 JSON URL
```

📚 **详细教程**：[QUICK_START.md](QUICK_START.md)

---

## 🎮 平台支持

### Discord 平台（推荐）

```
✅ 使用视频组件发送
✅ 触发原生媒体播放器
✅ 支持音视频播放
✅ 媒体控制（播放/暂停/音量/全屏）
✅ 自动降级机制
```

**效果演示**：
```
用户: /rv

Bot: [Discord 原生视频播放器]
     📊 本轮已播放: 3/10
     💡 发送 '/rv' 获取下一个视频
```

📖 **完整指南**：[DISCORD_GUIDE.md](DISCORD_GUIDE.md)

### 其他平台

- QQ：尝试使用平台视频组件
- Telegram：视频组件或链接
- 其他：降级为链接方式

---

## 📝 命令列表

| 命令 | 别名 | 说明 | 权限 |
|------|------|------|------|
| `/randomvideo` | `/rv`, `/随机视频` | 随机播放一个视频 | 所有用户 |
| `/videoinfo` | `/视频信息` | 查看视频库信息和播放进度 | 所有用户 |
| `/reloadvideos` | `/重载视频` | 重新加载视频列表 | 仅管理员 |

### 使用示例

```bash
# 播放随机视频
/rv

# 查看信息
/videoinfo

# 重新加载（管理员）
/reloadvideos
```

---

## ⚙️ 配置说明

### 插件配置（AstrBot 面板）

#### video_json_url（必填）
视频链接 JSON 文件的 URL

**支持的 JSON 格式**：

```json
// 格式 1: 简单数组（推荐）
[
  "https://cdn.example.com/video1.mp4",
  "https://cdn.example.com/video2.mp4"
]

// 格式 2: 对象格式
{
  "videos": ["url1", "url2"]
}

// 格式 3: 键值对
{
  "video1": "url1",
  "video2": "url2"
}
```

#### command_name（可选）
自定义命令名称，默认 `randomvideo`

---

## 🔧 OSS 同步工具

### 功能特性

- ✅ 自动扫描阿里云 OSS bucket
- ✅ 智能对比，只添加新视频
- ✅ 支持自定义 CDN 域名
- ✅ 支持多种视频格式
- ✅ 自动处理空文件和错误

### 快速使用

```bash
# 进入脚本目录
cd scripts

# 一键安装（Windows）
setup.bat

# 一键安装（Linux/macOS）
./setup.sh

# 配置 .env 文件
填写阿里云 OSS 配置

# 运行同步
python sync_oss_videos.py
```

### 配置示例

```env
# 阿里云 OSS 配置
OSS_ACCESS_KEY_ID=LTAI5txxxxxx
OSS_ACCESS_KEY_SECRET=aBcDeFxxxxxx
OSS_ENDPOINT=oss-cn-hangzhou.aliyuncs.com
OSS_BUCKET_NAME=my-videos
OSS_PREFIX=videos/

# 使用 Cloudflare CDN（推荐）
OSS_CUSTOM_DOMAIN=https://cdn.example.com
```

📖 **详细文档**：
- [scripts/README.md](scripts/README.md) - 脚本详细说明
- [scripts/USAGE_EXAMPLE.md](scripts/USAGE_EXAMPLE.md) - 完整使用示例

---

## 📚 文档导航

### 📘 基础文档
- [README.md](README.md) - 主文档（本文件）
- [QUICK_START.md](QUICK_START.md) - 5 分钟快速开始
- [CHANGELOG.md](CHANGELOG.md) - 更新日志

### 📗 进阶文档
- [DISCORD_GUIDE.md](DISCORD_GUIDE.md) - Discord 平台完整指南
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - 项目结构说明

### 📙 脚本文档
- [scripts/README.md](scripts/README.md) - OSS 同步脚本说明
- [scripts/USAGE_EXAMPLE.md](scripts/USAGE_EXAMPLE.md) - 完整使用示例

---

## ❓ 常见问题

### Q: Discord 上能播放视频和音频吗？

✅ **完整支持**！插件在 Discord 上使用视频组件：
- 触发 Discord 原生媒体播放器
- 点击即可播放视频和音频
- 支持暂停、音量控制、全屏等功能

### Q: 为什么没有视频播放？

**检查清单**：
1. ✅ 配置中的 `video_json_url` 是否正确
2. ✅ JSON URL 是否可访问
3. ✅ JSON 格式是否正确

**解决方法**：
```bash
# 测试 JSON URL
curl https://your-json-url.com/videos.json

# 重新加载插件
发送: /reloadvideos
```

### Q: 如何更新视频列表？

**方法 1: 使用 OSS 同步脚本**
```bash
python scripts/sync_oss_videos.py
# 重新部署 JSON 文件
# 在 AstrBot 中发送: /reloadvideos
```

**方法 2: 手动编辑**
```bash
# 编辑 JSON 文件
# 重新部署
# 发送: /reloadvideos
```

### Q: Discord 上有交互式按钮吗？

目前 AstrBot 框架暂不支持 Discord 交互式按钮。

**替代方案**：
- 使用斜杠命令：`/rv` 获取新视频
- 命令简短，使用方便
- 功能效果相同

### Q: 如何节省 OSS 流量费用？

使用 **Cloudflare CDN**：
```env
# 在 scripts/.env 中配置
OSS_CUSTOM_DOMAIN=https://cdn.example.com
```

**优势**：
- ✅ 免费 CDN 流量
- ✅ 全球加速
- ✅ HTTPS 支持

---

## 📈 更新日志

### [v1.1.0] - 2025-10-02

#### ✨ 新增功能
- **Discord 原生视频播放器支持**
- 自动降级机制
- Discord 平台完整使用指南

#### 📚 文档更新
- 新增 DISCORD_GUIDE.md
- 更新 README 和 QUICK_START
- 新增 CHANGELOG.md

[查看完整更新日志](CHANGELOG.md)

### [v1.0.0] - 2025-10-02

#### 🎉 首次发布
- 核心随机播放功能
- OSS 自动同步工具
- 多平台支持
- 完整文档

---

## 🛠️ 技术栈

- **Python** 3.8+
- **AstrBot** v4.x
- **aiohttp** - 异步 HTTP 请求
- **oss2** - 阿里云 OSS SDK
- **python-dotenv** - 环境变量管理

---

## 📄 许可证

MIT License

---

## 🔗 相关链接

- **AstrBot 官方文档**: https://docs-v4.astrbot.app/
- **AstrBot GitHub**: https://github.com/AstrBotDevs/AstrBot
- **插件仓库**: https://github.com/marvinli001/astrbot_plugin_random_videos

---

## 🤝 贡献

欢迎贡献代码和建议！

1. Fork 本仓库
2. 创建功能分支
3. 提交更改
4. 开启 Pull Request

查看 [CHANGELOG.md](CHANGELOG.md) 了解贡献指南。

---

## 🎉 开始使用

1. **安装插件** - 复制到 `data/plugins` 目录
2. **配置 JSON URL** - 在 AstrBot 面板设置
3. **测试使用** - 发送 `/rv` 命令

**Discord 用户**：查看 [DISCORD_GUIDE.md](DISCORD_GUIDE.md) 获取最佳体验！

---

<div align="center">

**享受随机视频的乐趣！** 🎬

Made with ❤️ by Marvin

</div>
