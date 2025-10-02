#!/usr/bin/env python3
"""
OSS 视频同步工具 - 安装配置脚本
一键安装依赖并配置环境变量
"""

import os
import sys
import subprocess
from pathlib import Path


def print_banner():
    """打印欢迎横幅"""
    print("=" * 60)
    print("  OSS 视频同步脚本 - 安装向导")
    print("=" * 60)
    print()


def check_env_file():
    """检查并创建 .env 文件"""
    env_path = Path(__file__).parent / '.env'
    env_example_path = Path(__file__).parent / '.env.example'

    if env_path.exists():
        print("[✓] 已找到配置文件 .env")
        return True
    else:
        print("[!] 未找到配置文件，正在创建...")
        if not env_example_path.exists():
            print("[✗] 错误：找不到 .env.example 文件")
            return False

        # 复制示例文件
        with open(env_example_path, 'r', encoding='utf-8') as f:
            content = f.read()

        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print("[✓] 已创建 .env 文件")
        print()
        print("=" * 60)
        print("  [重要] 请编辑 .env 文件，填写您的阿里云 OSS 配置")
        print("=" * 60)
        print()
        print("配置项说明：")
        print("  OSS_ACCESS_KEY_ID       - 阿里云 AccessKey ID")
        print("  OSS_ACCESS_KEY_SECRET   - 阿里云 AccessKey Secret")
        print("  OSS_ENDPOINT            - OSS 区域节点")
        print("  OSS_BUCKET_NAME         - OSS Bucket 名称")
        print("  OSS_PREFIX              - OSS 路径前缀（可选）")
        print("  OSS_CUSTOM_DOMAIN       - 自定义 CDN 域名（可选）")
        print()
        return False


def install_dependencies():
    """安装 Python 依赖"""
    requirements_path = Path(__file__).parent / 'requirements.txt'

    if not requirements_path.exists():
        print("[✗] 错误：找不到 requirements.txt 文件")
        return False

    print("正在安装 Python 依赖...")
    print()

    try:
        # 使用 pip 安装依赖
        subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '-r', str(requirements_path)],
            check=True
        )
        print()
        print("[✓] 依赖安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print()
        print(f"[✗] 依赖安装失败: {str(e)}")
        print()
        print("请手动运行：")
        print(f"  pip install -r {requirements_path}")
        return False


def open_env_file():
    """打开 .env 文件供用户编辑"""
    env_path = Path(__file__).parent / '.env'

    print()
    print("=" * 60)
    print("  下一步：编辑配置文件")
    print("=" * 60)
    print()
    print(f"配置文件路径: {env_path}")
    print()
    print("请使用文本编辑器打开并填写配置。")
    print()

    # 询问是否现在编辑
    response = input("是否现在打开配置文件？(y/n): ").strip().lower()

    if response in ['y', 'yes', '是']:
        import platform

        try:
            system = platform.system()

            if system == 'Windows':
                os.startfile(str(env_path))
            elif system == 'Darwin':  # macOS
                subprocess.run(['open', str(env_path)])
            else:  # Linux
                # 尝试常用编辑器
                editors = ['nano', 'vim', 'vi', 'gedit', 'kate']
                for editor in editors:
                    if subprocess.run(['which', editor], capture_output=True).returncode == 0:
                        subprocess.run([editor, str(env_path)])
                        break
                else:
                    print(f"请手动编辑: {env_path}")
        except Exception as e:
            print(f"无法自动打开文件: {str(e)}")
            print(f"请手动编辑: {env_path}")


def print_usage():
    """打印使用说明"""
    print()
    print("=" * 60)
    print("  安装完成！")
    print("=" * 60)
    print()
    print("使用方法：")
    print()
    print("  1. 编辑配置文件（如果还未编辑）")
    print("     配置文件: .env")
    print()
    print("  2. 运行同步脚本")
    print("     python sync_oss_videos.py")
    print()
    print("  3. 查看生成的 JSON 文件")
    print("     生成位置: videos.json")
    print()
    print("更多信息请查看: README.md")
    print()


def main():
    """主函数"""
    print_banner()

    # 检查并创建 .env 文件
    env_exists = check_env_file()

    print()

    # 安装依赖
    if not install_dependencies():
        print()
        print("安装过程中出现错误，请检查后重试。")
        sys.exit(1)

    # 如果 .env 文件是新创建的，提示用户编辑
    if not env_exists:
        open_env_file()

    # 打印使用说明
    print_usage()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        print()
        print("安装已取消")
        sys.exit(0)
    except Exception as e:
        print()
        print(f"发生错误: {str(e)}")
        sys.exit(1)
