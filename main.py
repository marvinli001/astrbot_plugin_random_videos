import random
import aiohttp
import json
from typing import List, Dict, Set
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import astrbot.api.message_components as Comp

@register("random_videos", "YourName", "随机视频播放插件 - 支持从 JSON 文件随机播放视频", "1.0.0")
class RandomVideosPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.video_urls: List[str] = []
        self.session_history: Dict[str, Set[str]] = {}  # 记录每个会话已播放的视频

    async def initialize(self):
        """插件初始化时加载视频列表"""
        await self.load_videos()

    async def load_videos(self):
        """从配置的 JSON URL 加载视频列表"""
        # AstrBot 会自动将配置注入到 self.config 属性
        config = getattr(self, 'config', {})

        # 如果 self.config 不存在，尝试其他方式
        if not config:
            logger.info("尝试从 context 获取配置...")
            try:
                # 尝试获取插件配置
                all_config = self.context.get_config()
                logger.info(f"获取到的配置: {all_config}")
                config = all_config.get('plugin_config', {}).get('random_videos', {})
            except Exception as e:
                logger.error(f"获取配置失败: {str(e)}")
                config = {}

        logger.info(f"最终使用的配置: {config}")
        video_json_url = config.get("video_json_url", "")

        if not video_json_url:
            logger.warning("未配置视频 JSON URL，请在插件配置中设置 video_json_url")
            return

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(video_json_url) as response:
                    if response.status == 200:
                        data = await response.json()

                        # 支持多种 JSON 格式
                        if isinstance(data, list):
                            # 格式 1: ["url1", "url2", ...]
                            self.video_urls = [url for url in data if isinstance(url, str)]
                        elif isinstance(data, dict):
                            # 格式 2: {"videos": ["url1", "url2", ...]}
                            if "videos" in data:
                                self.video_urls = data["videos"]
                            # 格式 3: {"video1": "url1", "video2": "url2", ...}
                            else:
                                self.video_urls = list(data.values())

                        logger.info(f"成功加载 {len(self.video_urls)} 个视频链接")
                    else:
                        logger.error(f"加载视频 JSON 失败，HTTP 状态码: {response.status}")
        except Exception as e:
            logger.error(f"加载视频列表时出错: {str(e)}")

    def get_random_video(self, session_id: str) -> str:
        """获取随机视频 URL，确保在当前轮次不重复"""
        if not self.video_urls:
            return None

        # 获取当前会话的历史记录
        if session_id not in self.session_history:
            self.session_history[session_id] = set()

        history = self.session_history[session_id]

        # 如果所有视频都已播放过，开始新一轮
        if len(history) >= len(self.video_urls):
            logger.info(f"会话 {session_id} 已播放所有视频，开始新一轮")
            history.clear()

        # 获取未播放的视频
        available_videos = [url for url in self.video_urls if url not in history]

        # 随机选择一个视频
        selected_video = random.choice(available_videos)
        history.add(selected_video)

        return selected_video

    @filter.command("randomvideo", alias=["rv", "随机视频"])
    async def random_video_command(self, event: AstrMessageEvent):
        """随机视频指令"""
        # 如果视频列表为空，尝试重新加载
        if not self.video_urls:
            await self.load_videos()

        if not self.video_urls:
            yield event.plain_result("❌ 未找到可用的视频。请检查插件配置中的 video_json_url 是否正确。")
            return

        # 获取会话 ID
        session_id = event.get_session_id()

        # 获取随机视频
        video_url = self.get_random_video(session_id)

        if video_url:
            # 构建消息链
            message_chain = []

            # 获取平台信息
            platform_name = event.get_platform_name()

            # 根据平台不同，使用不同的发送方式
            if platform_name.lower() == "discord":
                # Discord 平台：使用视频组件发送，触发原生播放器
                try:
                    # 尝试使用视频组件（可以触发 Discord 媒体控件）
                    message_chain.append(Comp.Video.fromURL(url=video_url))

                    # 添加描述文本
                    history_count = len(self.session_history.get(session_id, set()))
                    total_count = len(self.video_urls)
                    message_chain.append(Comp.Plain(f"\n📊 本轮已播放: {history_count}/{total_count}"))
                    message_chain.append(Comp.Plain(f"\n💡 发送 '/rv' 获取下一个视频"))
                except Exception as e:
                    # 如果视频组件失败，降级为纯链接（Discord 会自动嵌入）
                    logger.warning(f"Discord 视频组件发送失败，降级为链接: {str(e)}")
                    message_chain.append(Comp.Plain(f"🎬 随机视频:\n{video_url}"))

                    history_count = len(self.session_history.get(session_id, set()))
                    total_count = len(self.video_urls)
                    message_chain.append(Comp.Plain(f"\n\n📊 本轮已播放: {history_count}/{total_count}"))
                    message_chain.append(Comp.Plain(f"\n💡 发送 '/rv' 获取下一个视频"))
            else:
                # 其他平台：尝试发送视频组件
                try:
                    message_chain.append(Comp.Video.fromURL(url=video_url))
                except:
                    # 如果视频组件失败，发送链接
                    message_chain.append(Comp.Plain(f"🎬 随机视频:\n{video_url}"))

                # 添加提示信息
                history_count = len(self.session_history.get(session_id, set()))
                total_count = len(self.video_urls)
                message_chain.append(Comp.Plain(f"\n\n📊 本轮已播放: {history_count}/{total_count}"))
                message_chain.append(Comp.Plain(f"\n💡 发送 '/randomvideo' 或 '/rv' 获取下一个视频"))

            yield event.chain_result(message_chain)
        else:
            yield event.plain_result("❌ 获取视频失败，请稍后重试")

    @filter.command("reloadvideos", alias=["重载视频"])
    async def reload_videos_command(self, event: AstrMessageEvent):
        """重新加载视频列表"""
        # 检查是否为管理员
        if not event.is_admin():
            yield event.plain_result("❌ 此命令仅管理员可用")
            return

        await self.load_videos()

        if self.video_urls:
            yield event.plain_result(f"✅ 成功重新加载 {len(self.video_urls)} 个视频链接")
        else:
            yield event.plain_result("❌ 重新加载失败，请检查配置")

    @filter.command("videoinfo", alias=["视频信息"])
    async def video_info_command(self, event: AstrMessageEvent):
        """查看视频库信息"""
        if not self.video_urls:
            yield event.plain_result("❌ 暂无可用视频")
            return

        session_id = event.get_session_id()
        history_count = len(self.session_history.get(session_id, set()))
        total_count = len(self.video_urls)

        info_text = f"""📹 视频库信息
━━━━━━━━━━━━━━━━
📚 总视频数: {total_count}
✅ 本轮已播放: {history_count}
⏳ 本轮剩余: {total_count - history_count}
━━━━━━━━━━━━━━━━
💡 命令说明:
  /randomvideo 或 /rv - 随机播放视频
  /reloadvideos - 重新加载视频列表(仅管理员)
  /videoinfo - 查看此信息"""

        yield event.plain_result(info_text)

    async def terminate(self):
        """插件卸载时清理资源"""
        self.video_urls.clear()
        self.session_history.clear()
        logger.info("RandomVideosPlugin 已卸载")
