from core.logger import logger


class EventHandler:
    """Handlers here run on the Discord asyncio thread (NOT the Tk main
    thread), since discord_client.py's event loop runs in a background
    thread. Any UI-touching code MUST go through self.app.ui.call(...)
    (utils/ui_queue.py) rather than touching widgets directly -- tkinter
    isn't thread-safe, and mixing direct calls with the queue invites
    subtle, hard-to-reproduce crashes."""

    def __init__(self, app):

        self.app = app

    async def on_ready(self):

        logger.info(f"Connected as {self.app.discord.client.user}")

        self.app.ui.call(self.app._on_ready)

    async def on_message(self, message):

        # Always cache, regardless of whether it's the currently open channel.
        self.app.cache.add(message)

        if self.app.state.get("active_channel_id") == message.channel.id:
            self.app.ui.call(self.app._on_message_received, message)

    async def on_typing(
        self,
        channel,
        user,
        when
    ):

        pass

    async def on_member_update(
        self,
        before,
        after
    ):

        pass

    async def on_disconnect(self):
        logger.warning("Disconnected from Discord")
        self.app.ui.call(self.app._on_disconnected)

    async def on_resumed(self):
        logger.info("Gateway connection resumed")
        self.app.ui.call(self.app._on_ready)