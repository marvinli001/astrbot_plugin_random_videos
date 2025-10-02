# AstrBot 随机视频插件

一个支持从 JSON 文件随机播放视频的 AstrBot 插件，具有防重复播放功能。

## ✨ 功能特性

- 📹 从远程 JSON 文件加载视频链接
- 🎲 智能随机播放，确保当前轮次不重复
- 🔄 自动轮次管理：播放完所有视频后自动开始新一轮
- 📊 实时显示播放进度
- 🌐 多平台支持（Discord、QQ、Telegram 等）
- 🎯 针对 Discord 优化的视频链接展示

## 📦 安装

1. 将本插件文件夹放入 AstrBot 的 `data/plugins` 目录
2. 重启 AstrBot 或在控制台重载插件

> 💡 **Discord 用户**：查看 [Discord 使用指南](DISCORD_GUIDE.md) 了解详细的 Discord 平台使用说明

## ⚙️ 配置

在 AstrBot 管理面板中配置以下选项：

### video_json_url (必填)
视频链接 JSON 文件的 URL 地址

**支持的 JSON 格式：**

```json
// 格式 1: 简单数组
[
  "https://example.com/video1.mp4",
  "https://example.com/video2.mp4",
  "https://example.com/video3.mp4"
]

// 格式 2: 带 videos 键的对象
{
  "videos": [
    "https://example.com/video1.mp4",
    "https://example.com/video2.mp4"
  ]
}

// 格式 3: 键值对对象
{
  "video1": "https://example.com/video1.mp4",
  "video2": "https://example.com/video2.mp4"
}
```

### command_name (可选)
触发命令名称，默认为 `randomvideo`

## 🎮 使用方法

### 基础命令

- `/randomvideo` 或 `/rv` - 随机播放一个视频
- `/videoinfo` - 查看视频库信息和播放进度
- `/reloadvideos` - 重新加载视频列表（仅管理员）

### 命令别名

- `/randomvideo` = `/rv` = `/随机视频`
- `/reloadvideos` = `/重载视频`
- `/videoinfo` = `/视频信息`

## 🔧 工作原理

1. **加载视频列表**：插件初始化时从配置的 JSON URL 加载视频链接
2. **随机选择**：每次请求时随机选择一个未播放的视频
3. **防重复机制**：记录每个会话已播放的视频，确保本轮不重复
4. **自动重置**：当所有视频都播放过后，自动清空历史，开始新一轮

## 🌐 平台适配

### Discord
- ✅ **使用视频组件发送**：触发 Discord 原生媒体播放器
- ✅ **支持音视频播放**：可以直接点击播放，听到音频
- ✅ **自动降级机制**：如果视频组件失败，自动降级为链接（Discord 会自动嵌入预览）
- ✅ **播放进度显示**：实时显示本轮已播放进度
- ✅ **使用提示**：发送 `/rv` 获取下一个随机视频

### 其他平台
- 尝试使用平台原生视频组件
- 失败时降级为链接方式发送

## 📝 使用示例

### Discord 平台
```
用户: /rv

Bot: [发送视频组件 - Discord 原生播放器]
     📊 本轮已播放: 1/10
     💡 发送 '/rv' 获取下一个视频

效果：
- 视频以 Discord 原生播放器形式显示
- 可以直接点击播放按钮观看
- 支持音频播放、暂停、音量控制等
- 支持全屏播放
```

### 其他平台（QQ、Telegram 等）
```
用户: /randomvideo

Bot: [视频组件/链接]

     📊 本轮已播放: 1/10
     💡 发送 '/randomvideo' 或 '/rv' 获取下一个视频
```

## 🔧 OSS 视频同步工具

本插件包含一个强大的阿里云 OSS 视频同步脚本，可以自动扫描 OSS 中的视频并生成 JSON 文件。

### 功能特性

- ✅ 自动扫描阿里云 OSS bucket 中的视频文件
- ✅ 智能对比，只添加新视频
- ✅ 支持 Cloudflare CDN 等自定义域名（节省流量费用）
- ✅ 支持多种视频格式
- ✅ 自动处理空文件和错误

### 快速开始

```bash
# 进入脚本目录
cd scripts

# 一键安装配置
python setup.py

# 按提示编辑 .env 文件
# 填写阿里云 OSS 配置和可选的 CDN 域名

# 运行同步
python sync_oss_videos.py
```

详细文档请查看：[scripts/README.md](scripts/README.md)

## 🔍 常见问题

**Q: 为什么没有视频播放？**
A: 请检查配置中的 `video_json_url` 是否正确，并使用 `/reloadvideos` 命令重新加载

**Q: 如何更新视频列表？**
A: 修改 JSON 文件内容后，使用 `/reloadvideos` 命令（需要管理员权限）

**Q: Discord 上能播放视频和音频吗？**
A: ✅ 可以！插件会在 Discord 上使用视频组件发送，触发 Discord 原生播放器，支持：
- 点击播放按钮观看视频
- 听到视频中的音频
- 音量控制、暂停/播放、全屏等功能
- 如果视频组件失败，会自动降级为链接（Discord 仍会嵌入预览）

**Q: Discord 上有交互式按钮可以切换视频吗？**
A: 目前 AstrBot 框架暂不支持 Discord 的交互式按钮组件。使用斜杠命令替代：
- 发送 `/rv` 或 `/randomvideo` 获取下一个随机视频
- 每次发送命令都会返回一个新的随机视频

**Q: 如何自动同步 OSS 中的新视频？**
A: 使用 `scripts` 目录下的 OSS 同步脚本，支持自动扫描和增量更新。详见 [scripts/README.md](scripts/README.md)

## 🛠️ 开发信息

- 基于 AstrBot v4 API
- 使用 aiohttp 异步加载远程 JSON
- 支持多会话隔离的播放历史

## 📄 许可证

MIT License

## 🔗 相关链接

- [AstrBot 官方文档](https://astrbot.app/)
- [AstrBot GitHub](https://github.com/AstrBotDevs/AstrBot)
