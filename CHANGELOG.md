# 更新日志

## [1.1.2] - 2025-10-02

### 🐛 Bug 修复
- **修复插件初始化错误** ⭐
  - 按照 AstrBot v4 官方文档规范修正 `__init__` 方法签名
  - 添加 `config: AstrBotConfig` 参数接收插件配置
  - 修复 `TypeError: __init__() got an unexpected keyword argument 'config'` 错误
  - 修复 `AttributeError: 'Context' object has no attribute 'get_plugin_config'` 错误

### 🔧 技术改进
- 使用官方标准的配置读取方式：`self.config.get("video_json_url")`
- 导入 `AstrBotConfig` 类型提示
- 代码完全符合 [AstrBot v4 插件开发规范](https://docs-v4.astrbot.app/dev/star/plugin.html)

---

## [1.1.1] - 2025-10-02

### 🐛 Bug 修复
- **修复插件配置读取问题**
  - 添加详细的配置获取日志
  - 尝试多种配置获取方式（self.config、context.get_config()）
  - 修复插件配置 video_json_url 无法正确读取的问题
- **修复版本号格式问题** ⭐
  - 移除版本号 `v` 前缀，使用纯数字格式（1.1.1）
  - 修复 AstrBot 无法检测插件更新的问题
  - 版本号格式符合 AstrBot 更新检测要求

### 🔧 技术改进
- 优先使用 `self.config` 属性获取插件配置
- 降级尝试从 `context.get_config()` 获取配置
- 添加详细的调试日志，方便排查配置问题

### 📝 其他
- 更新作者信息为 Marvin
- 更新插件描述信息

---

## [v1.1.0] - 2025-10-02

### ✨ 新增功能
- **Discord 原生视频播放器支持**
  - 在 Discord 平台使用视频组件发送，触发原生媒体播放器
  - 支持点击播放、音频播放、音量控制、全屏等功能
  - 自动降级机制：视频组件失败时自动使用链接（Discord 仍会嵌入预览）

### 📚 文档更新
- 新增 [DISCORD_GUIDE.md](DISCORD_GUIDE.md) - Discord 平台完整使用指南
- 更新 [README.md](README.md) - 添加 Discord 功能说明
- 更新 [QUICK_START.md](QUICK_START.md) - 添加 Discord 视频播放 FAQ

### 🐛 Bug 修复
- 优化 Discord 平台视频发送逻辑
- 改进错误处理和日志记录

### 🔧 技术改进
- Discord 平台优先使用 `Comp.Video.fromURL()` 发送视频
- 添加异常捕获和降级处理
- 优化平台检测逻辑

---

## [v1.0.0] - 2025-10-02

### 🎉 首次发布

#### 核心功能
- ✅ 从远程 JSON URL 加载视频列表
- ✅ 智能随机播放（防重复机制）
- ✅ 自动轮次管理
- ✅ 会话隔离的播放历史
- ✅ 多平台支持（Discord、QQ、Telegram 等）

#### 命令系统
- `/randomvideo` (别名: `/rv`, `/随机视频`) - 随机播放视频
- `/videoinfo` (别名: `/视频信息`) - 查看视频库信息
- `/reloadvideos` (别名: `/重载视频`) - 重新加载视频列表（管理员）

#### OSS 同步工具
- 🔧 阿里云 OSS 视频自动扫描
- 🔧 智能对比，只添加新视频
- 🔧 支持 Cloudflare CDN 等自定义域名
- 🔧 支持多种视频格式
- 🔧 一键安装脚本（Windows/Linux/macOS）

#### 文档
- 📚 完整的 README 文档
- 📚 快速开始指南
- 📚 项目结构说明
- 📚 OSS 同步脚本文档
- 📚 完整使用示例

#### 配置
- ⚙️ `video_json_url` - JSON 文件链接
- ⚙️ `command_name` - 自定义命令名（可选）

#### 支持的 JSON 格式
- 格式 1: 简单数组 `["url1", "url2"]`
- 格式 2: 对象格式 `{"videos": ["url1"]}`
- 格式 3: 键值对 `{"video1": "url1"}`

---

## 版本说明

### 语义化版本控制

本项目遵循 [语义化版本控制 2.0.0](https://semver.org/lang/zh-CN/)：

- **主版本号（Major）**：不兼容的 API 修改
- **次版本号（Minor）**：向下兼容的功能性新增
- **修订号（Patch）**：向下兼容的问题修正

### 版本计划

#### v1.2.0（计划中）
- [ ] 视频分类功能
- [ ] 视频缓存机制
- [ ] 播放统计功能

#### v2.0.0（未来规划）
- [ ] Web 管理界面
- [ ] 视频评分系统
- [ ] 多语言支持
- [ ] 播放列表功能

---

## 贡献指南

欢迎贡献代码和建议！

### 提交 Issue
- 使用清晰的标题描述问题
- 提供复现步骤
- 包含错误日志（如有）
- 说明环境信息（AstrBot 版本、平台等）

### 提交 Pull Request
1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 开发规范
- 遵循 PEP 8 代码规范
- 添加必要的注释和文档
- 更新 CHANGELOG.md
- 测试新功能

---

## 致谢

感谢以下项目和贡献者：

- [AstrBot](https://github.com/AstrBotDevs/AstrBot) - 强大的多平台聊天机器人框架
- 所有使用和反馈的用户
- 所有贡献代码的开发者

---

**完整文档**：
- [主文档](README.md)
- [快速开始](QUICK_START.md)
- [Discord 指南](DISCORD_GUIDE.md)
- [项目结构](PROJECT_STRUCTURE.md)
- [OSS 同步脚本](scripts/README.md)
