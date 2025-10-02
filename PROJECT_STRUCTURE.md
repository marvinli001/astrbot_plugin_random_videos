# 项目结构说明

## 📁 完整目录结构

```
astrbot_plugin_random_videos/
│
├── 📄 main.py                      # 插件主逻辑文件
├── 📄 metadata.yaml                # 插件元数据配置
├── 📄 _conf_schema.json            # 插件配置选项定义
├── 📄 requirements.txt             # 插件 Python 依赖
├── 📄 LICENSE                      # MIT 许可证
│
├── 📘 README.md                    # 主文档（插件使用说明）
├── 📗 QUICK_START.md              # 快速开始指南
├── 📙 PROJECT_STRUCTURE.md        # 本文件（项目结构说明）
│
├── 📄 example_videos.json         # JSON 格式示例文件
├── 📄 .gitignore                  # Git 忽略规则
│
└── 📂 scripts/                    # OSS 同步脚本目录
    ├── 🐍 sync_oss_videos.py      # OSS 视频同步主脚本
    ├── 📄 requirements.txt         # 脚本依赖（oss2, python-dotenv）
    │
    ├── 📄 .env.example             # 环境变量配置模板
    ├── 🔒 .env                     # 实际环境变量（已忽略）
    │
    ├── 📜 setup.bat                # Windows 安装脚本
    ├── 📜 setup.sh                 # Linux/macOS 安装脚本
    │
    ├── 📘 README.md                # 脚本详细文档
    ├── 📗 USAGE_EXAMPLE.md        # 完整使用示例
    │
    └── 📄 videos.json              # 生成的视频链接文件（已忽略）
```

## 📄 核心文件说明

### 插件核心文件

#### `main.py`
- **作用**: AstrBot 插件主逻辑
- **功能**:
  - 从远程 JSON URL 加载视频列表
  - 实现智能随机播放（防重复）
  - 处理命令（/randomvideo, /videoinfo, /reloadvideos）
  - 多平台适配（Discord, QQ, Telegram 等）
  - 会话隔离的播放历史管理

#### `metadata.yaml`
- **作用**: 插件元数据
- **内容**:
  ```yaml
  name: random_videos
  desc: 随机视频播放插件
  version: v1.0.0
  author: Marvin
  repo: https://github.com/marvinli001/astrbot_plugin_random_videos
  ```

#### `_conf_schema.json`
- **作用**: 定义插件配置项
- **配置项**:
  - `video_json_url`: JSON 文件链接（必填）
  - `command_name`: 自定义命令名（可选）

#### `requirements.txt`
- **作用**: 插件依赖
- **内容**: `aiohttp>=3.8.0`

### 文档文件

#### `README.md`
- **主文档**: 插件功能介绍和使用说明
- **包含**: 安装、配置、命令、FAQ

#### `QUICK_START.md`
- **快速指南**: 5 分钟快速部署教程
- **适合**: 新手用户快速上手

#### `PROJECT_STRUCTURE.md`
- **本文件**: 项目结构和文件说明
- **适合**: 开发者了解项目架构

### 示例文件

#### `example_videos.json`
- **作用**: JSON 格式示例
- **用途**: 帮助用户理解 JSON 格式要求

## 📂 Scripts 目录详解

### 核心脚本

#### `sync_oss_videos.py`
- **作用**: 阿里云 OSS 视频同步脚本
- **功能**:
  - 连接阿里云 OSS
  - 扫描指定路径下的视频文件
  - 生成视频访问 URL（支持自定义 CDN 域名）
  - 对比现有 JSON，只添加新视频
  - 格式化输出 JSON 文件

#### `requirements.txt`
- **作用**: 脚本依赖
- **内容**:
  ```
  oss2>=2.18.0
  python-dotenv>=1.0.0
  ```

### 配置文件

#### `.env.example`
- **作用**: 环境变量配置模板
- **配置项**:
  - OSS 连接信息（AccessKey、Endpoint、Bucket）
  - OSS 路径前缀
  - 自定义 CDN 域名
  - 视频格式过滤
  - 输出文件名

#### `.env`
- **作用**: 实际环境变量（不提交到 Git）
- **创建**: 复制 `.env.example` 并填写真实配置

### 安装脚本

#### `setup.bat` (Windows)
- **作用**: 一键安装依赖
- **功能**:
  - 检查 .env 文件
  - 自动创建配置
  - 安装 Python 依赖

#### `setup.sh` (Linux/macOS)
- **作用**: 一键安装依赖
- **功能**: 同 setup.bat，适用于 Unix 系统

### 文档文件

#### `scripts/README.md`
- **作用**: 脚本详细文档
- **内容**:
  - 功能介绍
  - 配置说明
  - 使用方法
  - CDN 配置
  - 定时任务设置
  - 常见问题

#### `scripts/USAGE_EXAMPLE.md`
- **作用**: 完整使用示例
- **内容**:
  - 从零开始的完整流程
  - 实际场景演示
  - GitHub Actions 自动化
  - 问题排查指南

### 生成文件

#### `videos.json`
- **作用**: 同步生成的视频链接文件
- **格式**:
  ```json
  [
    "https://cdn.example.com/video1.mp4",
    "https://cdn.example.com/video2.mp4"
  ]
  ```
- **注意**: 此文件会被 .gitignore 忽略

## 🔄 工作流程

### 1. 插件运行流程

```
用户发送 /rv 命令
    ↓
main.py 接收命令
    ↓
从 video_json_url 加载视频列表
    ↓
检查会话播放历史
    ↓
随机选择未播放视频
    ↓
根据平台发送视频
    ↓
更新播放历史
```

### 2. OSS 同步流程

```
运行 sync_oss_videos.py
    ↓
读取 .env 配置
    ↓
连接阿里云 OSS
    ↓
扫描视频文件
    ↓
生成视频 URL（使用 CDN 域名）
    ↓
读取现有 videos.json
    ↓
对比找出新视频
    ↓
合并并保存 JSON
    ↓
上传到服务器/OSS
```

### 3. 完整部署流程

```
1. 配置 OSS 同步脚本
   ├── 复制 .env.example → .env
   ├── 填写 OSS 配置
   └── 配置 CDN 域名（可选）

2. 运行同步
   └── python sync_oss_videos.py

3. 部署 JSON 文件
   ├── 上传到 OSS
   ├── 或 GitHub Gist
   └── 或自己的服务器

4. 配置 AstrBot 插件
   ├── 设置 video_json_url
   └── 重启插件

5. 测试使用
   └── 发送 /rv 命令
```

## 🔐 安全考虑

### 敏感文件（已在 .gitignore 中）

- `scripts/.env` - 包含 OSS 凭证
- `scripts/videos.json` - 可能包含内部 URL
- `scripts/*.log` - 可能包含敏感信息
- `scripts/*.bak` - 备份文件

### 权限建议

- OSS AccessKey 建议使用只读权限的 RAM 子账号
- JSON 文件建议设置公共读权限
- 不要在公开仓库提交 `.env` 文件

## 📦 依赖关系

### 插件依赖

```
astrbot_plugin_random_videos
    └── aiohttp (用于异步 HTTP 请求)
```

### 脚本依赖

```
sync_oss_videos.py
    ├── oss2 (阿里云 OSS SDK)
    └── python-dotenv (环境变量管理)
```

### 系统要求

- Python 3.8+
- AstrBot v4+
- 网络连接（访问远程 JSON 和视频）

## 🛠️ 开发者指南

### 修改插件

1. **添加新命令**
   - 在 `main.py` 中添加新的 `@filter.command()` 装饰器方法

2. **修改配置项**
   - 编辑 `_conf_schema.json` 添加新配置
   - 在 `main.py` 中读取配置

3. **支持新平台**
   - 在 `random_video_command()` 方法中添加平台判断逻辑

### 修改同步脚本

1. **支持其他云存储**
   - 参考 `sync_oss_videos.py` 结构
   - 替换 OSS SDK 为其他云存储 SDK
   - 保持相同的输出格式

2. **添加新功能**
   - 修改 `OSSVideoSync` 类
   - 添加新的配置项到 `.env.example`

## 📊 文件大小参考

| 文件 | 大小 | 说明 |
|------|------|------|
| main.py | ~7KB | 插件主逻辑 |
| sync_oss_videos.py | ~8KB | 同步脚本 |
| README.md | ~4KB | 主文档 |
| QUICK_START.md | ~7KB | 快速指南 |
| scripts/README.md | ~6KB | 脚本文档 |
| USAGE_EXAMPLE.md | ~9KB | 使用示例 |

## 🔗 相关链接

- **AstrBot 文档**: https://docs-v4.astrbot.app/
- **阿里云 OSS SDK**: https://help.aliyun.com/document_detail/32026.html
- **Python aiohttp**: https://docs.aiohttp.org/
- **Python-dotenv**: https://pypi.org/project/python-dotenv/

## 📝 维护说明

### 更新清单

更新插件时，确保同步更新以下文件：
- [ ] `main.py` - 代码逻辑
- [ ] `metadata.yaml` - 版本号
- [ ] `README.md` - 功能说明
- [ ] `QUICK_START.md` - 如有新步骤
- [ ] `PROJECT_STRUCTURE.md` - 如有新文件

### 版本发布

1. 更新 `metadata.yaml` 中的版本号
2. 更新所有文档中的版本引用
3. 提交到 Git: `git commit -m "Release v1.x.x"`
4. 打标签: `git tag v1.x.x`
5. 推送: `git push && git push --tags`

## 🎯 后续计划

可能的功能扩展：

- [ ] 支持视频分类
- [ ] 添加视频缓存
- [ ] 支持视频评分系统
- [ ] Web 管理界面
- [ ] 多语言支持
- [ ] 视频播放统计

欢迎贡献代码和建议！
