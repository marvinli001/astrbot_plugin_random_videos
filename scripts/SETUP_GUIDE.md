# 安装配置指南

## 🚀 一键安装

使用 `setup.py` 脚本可以自动完成所有安装和配置步骤。

### 基本用法

```bash
cd scripts
python setup.py
```

### 脚本功能

`setup.py` 会自动执行以下操作：

1. ✅ **检查配置文件**
   - 如果 `.env` 文件不存在，从 `.env.example` 复制创建
   - 如果已存在，跳过此步骤

2. ✅ **安装 Python 依赖**
   - 自动安装 `oss2` 和 `python-dotenv`
   - 使用 `pip install -r requirements.txt`

3. ✅ **提示编辑配置**
   - 提示用户编辑 `.env` 文件
   - 询问是否立即打开配置文件
   - 自动检测操作系统并使用合适的编辑器

### 交互流程

```
============================================================
  OSS 视频同步脚本 - 安装向导
============================================================

[!] 未找到配置文件，正在创建...
[✓] 已创建 .env 文件

============================================================
  [重要] 请编辑 .env 文件，填写您的阿里云 OSS 配置
============================================================

配置项说明：
  OSS_ACCESS_KEY_ID       - 阿里云 AccessKey ID
  OSS_ACCESS_KEY_SECRET   - 阿里云 AccessKey Secret
  OSS_ENDPOINT            - OSS 区域节点
  OSS_BUCKET_NAME         - OSS Bucket 名称
  OSS_PREFIX              - OSS 路径前缀（可选）
  OSS_CUSTOM_DOMAIN       - 自定义 CDN 域名（可选）


正在安装 Python 依赖...

Collecting oss2>=2.18.0
  ...
[✓] 依赖安装成功

============================================================
  下一步：编辑配置文件
============================================================

配置文件路径: /path/to/scripts/.env

请使用文本编辑器打开并填写配置。

是否现在打开配置文件？(y/n): y

[自动打开编辑器]

============================================================
  安装完成！
============================================================

使用方法：

  1. 编辑配置文件（如果还未编辑）
     配置文件: .env

  2. 运行同步脚本
     python sync_oss_videos.py

  3. 查看生成的 JSON 文件
     生成位置: videos.json

更多信息请查看: README.md
```

## 📝 配置说明

### 必填配置

编辑 `.env` 文件，填写以下必填项：

```env
OSS_ACCESS_KEY_ID=LTAI5tGh4xxx          # 阿里云 AccessKey ID
OSS_ACCESS_KEY_SECRET=aBcDeFg123xxx     # 阿里云 AccessKey Secret
OSS_ENDPOINT=oss-cn-hangzhou.aliyuncs.com  # OSS 区域节点
OSS_BUCKET_NAME=my-video-bucket         # OSS Bucket 名称
```

### 可选配置

```env
OSS_PREFIX=videos/                      # 只扫描特定目录
OSS_CUSTOM_DOMAIN=https://cdn.example.com  # 使用 CDN 域名
VIDEO_EXTENSIONS=.mp4,.avi,.mov         # 支持的视频格式
JSON_OUTPUT_FILE=videos.json            # 输出文件名
```

## 🔧 手动安装（备选方案）

如果 `setup.py` 脚本遇到问题，可以手动执行以下步骤：

### 步骤 1: 复制配置文件

**Windows:**
```bash
copy .env.example .env
```

**Linux/macOS:**
```bash
cp .env.example .env
```

### 步骤 2: 编辑配置

```bash
# Windows
notepad .env

# Linux/macOS
nano .env
# 或
vim .env
```

### 步骤 3: 安装依赖

```bash
pip install -r requirements.txt
```

### 步骤 4: 验证安装

```bash
python -c "import oss2; import dotenv; print('依赖安装成功')"
```

## ❓ 常见问题

### Q: setup.py 找不到 .env.example 文件

**解决方法：**
```bash
# 确保在 scripts 目录中运行
cd scripts
python setup.py
```

### Q: pip 安装依赖失败

**可能原因：**
- 网络连接问题
- Python 版本不兼容（需要 Python 3.8+）
- pip 版本过旧

**解决方法：**
```bash
# 升级 pip
python -m pip install --upgrade pip

# 使用国内镜像安装
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q: 配置文件无法自动打开

**解决方法：**
手动打开配置文件编辑：

```bash
# 查看配置文件路径
cd scripts
ls -la .env

# 手动编辑
notepad .env  # Windows
nano .env     # Linux/macOS
```

### Q: 已有 .env 文件，想重新配置

**解决方法：**
```bash
# 备份现有配置
cp .env .env.backup

# 删除现有配置
rm .env

# 重新运行 setup.py
python setup.py
```

## 🎯 下一步

安装完成后：

1. ✅ 确认 `.env` 文件已正确配置
2. ✅ 运行同步脚本：`python sync_oss_videos.py`
3. ✅ 查看生成的 `videos.json` 文件
4. ✅ 部署 JSON 文件到可访问的 URL
5. ✅ 在 AstrBot 插件中配置 `video_json_url`

## 📚 相关文档

- [README.md](README.md) - 完整使用说明
- [USAGE_EXAMPLE.md](USAGE_EXAMPLE.md) - 详细使用示例
- [.env.example](.env.example) - 配置文件模板

---

**提示**：如遇到任何问题，请先查看 [README.md](README.md) 中的常见问题部分。
