#!/usr/bin/env python3
"""
阿里云 OSS 视频同步脚本
功能：扫描 OSS bucket 中的视频文件，自动添加新视频链接到 JSON 文件
"""

import os
import json
import sys
from pathlib import Path
from typing import List, Set
from urllib.parse import quote

try:
    import oss2
    from dotenv import load_dotenv
except ImportError:
    print("❌ 缺少必要的依赖库，请先安装：")
    print("   pip install oss2 python-dotenv")
    sys.exit(1)


class OSSVideoSync:
    def __init__(self):
        # 加载环境变量
        env_path = Path(__file__).parent / '.env'
        if not env_path.exists():
            print("⚠️  未找到 .env 文件，请从 .env.example 复制并配置")
            sys.exit(1)

        load_dotenv(env_path)

        # 读取 OSS 配置
        self.access_key_id = os.getenv('OSS_ACCESS_KEY_ID')
        self.access_key_secret = os.getenv('OSS_ACCESS_KEY_SECRET')
        self.endpoint = os.getenv('OSS_ENDPOINT')
        self.bucket_name = os.getenv('OSS_BUCKET_NAME')
        self.prefix = os.getenv('OSS_PREFIX', '')
        self.custom_domain = os.getenv('OSS_CUSTOM_DOMAIN', '').rstrip('/')

        # 读取视频格式配置
        video_ext_str = os.getenv('VIDEO_EXTENSIONS', '.mp4,.avi,.mov,.mkv,.flv,.wmv,.webm,.m4v')
        self.video_extensions = [ext.strip().lower() for ext in video_ext_str.split(',')]

        # JSON 文件路径
        json_file = os.getenv('JSON_OUTPUT_FILE', 'videos.json')
        self.json_path = Path(__file__).parent / json_file

        # 验证配置
        if not all([self.access_key_id, self.access_key_secret, self.endpoint, self.bucket_name]):
            print("❌ 缺少必要的 OSS 配置，请检查 .env 文件")
            sys.exit(1)

        # 初始化 OSS 客户端
        try:
            auth = oss2.Auth(self.access_key_id, self.access_key_secret)
            self.bucket = oss2.Bucket(auth, self.endpoint, self.bucket_name)
            print(f"✅ 成功连接到 OSS Bucket: {self.bucket_name}")
        except Exception as e:
            print(f"❌ 连接 OSS 失败: {str(e)}")
            sys.exit(1)

    def is_video_file(self, filename: str) -> bool:
        """检查文件是否为视频文件"""
        return any(filename.lower().endswith(ext) for ext in self.video_extensions)

    def generate_video_url(self, object_key: str) -> str:
        """生成视频访问 URL"""
        # URL 编码对象键
        encoded_key = quote(object_key, safe='/')

        if self.custom_domain:
            # 使用自定义域名（如 Cloudflare CDN）
            return f"{self.custom_domain}/{encoded_key}"
        else:
            # 使用默认 OSS 域名
            bucket_domain = self.endpoint.replace('oss-', f"{self.bucket_name}.oss-")
            return f"https://{bucket_domain}/{encoded_key}"

    def scan_oss_videos(self) -> List[str]:
        """扫描 OSS bucket 中的所有视频文件"""
        video_urls = []

        print(f"🔍 开始扫描 OSS bucket...")
        if self.prefix:
            print(f"   扫描路径: {self.prefix}")

        try:
            # 列举所有对象
            total_files = 0
            video_count = 0

            for obj in oss2.ObjectIterator(self.bucket, prefix=self.prefix):
                total_files += 1

                # 检查是否为视频文件
                if self.is_video_file(obj.key):
                    video_url = self.generate_video_url(obj.key)
                    video_urls.append(video_url)
                    video_count += 1
                    print(f"   ✓ 发现视频: {obj.key}")

            print(f"\n📊 扫描完成:")
            print(f"   总文件数: {total_files}")
            print(f"   视频文件数: {video_count}")

        except Exception as e:
            print(f"❌ 扫描 OSS 时出错: {str(e)}")
            sys.exit(1)

        return video_urls

    def load_existing_videos(self) -> Set[str]:
        """加载现有 JSON 文件中的视频链接"""
        if not self.json_path.exists():
            print(f"ℹ️  JSON 文件不存在，将创建新文件: {self.json_path}")
            return set()

        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()

                # 处理空文件
                if not content:
                    print(f"ℹ️  JSON 文件为空，将初始化")
                    return set()

                data = json.loads(content)

                # 支持多种格式
                if isinstance(data, list):
                    return set(data)
                elif isinstance(data, dict) and 'videos' in data:
                    return set(data['videos'])
                else:
                    print(f"⚠️  JSON 格式不符合预期，将重新生成")
                    return set()

        except json.JSONDecodeError as e:
            print(f"⚠️  JSON 文件格式错误: {str(e)}")
            print(f"   将备份原文件并重新生成")
            # 备份损坏的文件
            backup_path = self.json_path.with_suffix('.json.bak')
            self.json_path.rename(backup_path)
            return set()
        except Exception as e:
            print(f"❌ 读取 JSON 文件失败: {str(e)}")
            return set()

    def save_videos(self, video_urls: List[str]):
        """保存视频链接到 JSON 文件"""
        try:
            # 格式化 JSON 输出
            json_content = json.dumps(
                video_urls,
                ensure_ascii=False,
                indent=2
            )

            with open(self.json_path, 'w', encoding='utf-8') as f:
                f.write(json_content)
                # 确保文件以换行符结尾
                if not json_content.endswith('\n'):
                    f.write('\n')

            print(f"✅ 成功保存到: {self.json_path}")

        except Exception as e:
            print(f"❌ 保存 JSON 文件失败: {str(e)}")
            sys.exit(1)

    def sync(self):
        """执行同步操作"""
        print("=" * 60)
        print("🚀 阿里云 OSS 视频同步工具")
        print("=" * 60)
        print()

        # 1. 扫描 OSS 中的视频
        oss_videos = self.scan_oss_videos()

        if not oss_videos:
            print("\n⚠️  未在 OSS 中找到任何视频文件")
            return

        print()

        # 2. 加载现有视频列表
        existing_videos = self.load_existing_videos()
        print(f"📋 现有视频数量: {len(existing_videos)}")
        print()

        # 3. 找出新增的视频
        new_videos = [url for url in oss_videos if url not in existing_videos]

        if not new_videos:
            print("✨ 没有新增视频，JSON 文件已是最新")
            return

        print(f"🆕 发现 {len(new_videos)} 个新视频:")
        for i, url in enumerate(new_videos, 1):
            print(f"   {i}. {url}")
        print()

        # 4. 合并并保存
        all_videos = list(existing_videos) + new_videos
        all_videos.sort()  # 排序以保持一致性

        self.save_videos(all_videos)

        print()
        print("=" * 60)
        print(f"✅ 同步完成！总共 {len(all_videos)} 个视频")
        print("=" * 60)


def main():
    """主函数"""
    try:
        syncer = OSSVideoSync()
        syncer.sync()
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断操作")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 发生未预期的错误: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
