import threading
import customtkinter as ctk

from ui.window import MainWindow
from ui.toolbar import Toolbar
from ui.chat import ChatPanel
from ui.servers import ServerPanel
from ui.channels import ChannelPanel
from ui.members import MemberPanel
from ui.dialogs import TokenDialog, MessageDialog

from utils.ui_queue import UIQueue
from utils.images import ImageLoader

from core.config import ConfigManager
from core.logger import logger

from Engine.cache import MessageCache
from Engine.discord_client import DiscordManager
from Engine.events import EventHandler
from Engine.reconnect import ReconnectManager
from Engine.uploads import UploadManager

import discord


class Application:

    def __init__(self):

        logger.info("Starting application")

        self.config = ConfigManager()

        self.cache = MessageCache()

        self.ui = UIQueue()

        self.images = ImageLoader()

        self.reconnect_manager = ReconnectManager()

        # Simple shared state -- which guild/channel is currently open,
        # so incoming events know whether to touch the visible chat. Keeps
        # the actual channel object too, not just its ID, so sending/
        # fetching history doesn't depend on discord.py's internal cache
        # lookup timing -- we already hold a live reference from the click.
        self.state = {
            "active_guild_id": None,
            "active_channel_id": None,
            "active_channel": None,
        }

        # Apply the saved theme before building any widgets.
        ctk.set_appearance_mode(self.config.get_theme())

        self.window = MainWindow()

        self.root = self.window.root

        self.toolbar = Toolbar(
            self.root,
            on_connect_click=self.handle_connect_click,
            on_theme_toggle=self.toggle_theme,
        )

        self.servers = ServerPanel(self.root, image_loader=self.images)

        self.channels = ChannelPanel(self.root)

        self.chat = ChatPanel(self.root, on_send=self.send_message, on_attach=self.send_file)

        self.members = MemberPanel(self.root, image_loader=self.images)

        self.events = EventHandler(self)

        self.discord = DiscordManager(self)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.setup_events()

        # Start processing UI updates
        self.process_ui()

        # Auto-connect if a token is already saved.
        token = self.config.get_token()
        if token:
            self.connect(token)

    def process_ui(self):
        self.ui.process()
        self.root.after(20, self.process_ui)

    def setup_events(self):
        logger.info("Connecting UI events")

    # ---------------- theme ----------------

    def toggle_theme(self):
        current = self.config.get_theme()
        new_theme = "light" if current == "dark" else "dark"
        ctk.set_appearance_mode(new_theme)
        self.config.set_theme(new_theme)

    # ---------------- connection lifecycle ----------------

    def handle_connect_click(self):
        if self.discord.client is not None and not self.discord.client.is_closed():
            self.discord.stop()
            self.toolbar.set_status("Disconnected", "disconnected")
            self.servers.clear()
            self.channels.clear()
            self.members.clear()
            self.chat.clear_messages()
            return

        dialog = TokenDialog(self.root, on_submit=self._on_token_submitted, initial_value=self.config.get_token())
        dialog.focus()

    def _on_token_submitted(self, token, remember):
        if remember:
            self.config.save_token(token)
        else:
            self.config.set("remember_token", False)
        self.connect(token)

    def connect(self, token):
        self.toolbar.set_status("Connecting...", "connecting")
        thread = threading.Thread(target=self._connect_thread, args=(token,), daemon=True)
        thread.start()

    def _connect_thread(self, token):
        # A bad/expired token or missing intents will fail every attempt in
        # the same way -- retrying those blindly just delays telling the
        # user something they need to fix. Only genuinely transient
        # connection issues get the retry-with-backoff treatment.
        try:
            if self.config.get("auto_reconnect", True):
                self.reconnect_manager.execute(lambda: self.discord.start(token))
            else:
                self.discord.start(token)
        except discord.LoginFailure:
            self.ui.call(self._on_connect_error, "Invalid token -- Discord rejected it.")
        except discord.PrivilegedIntentsRequired:
            self.ui.call(
                self._on_connect_error,
                "This bot needs privileged intents (Server Members / Message Content) "
                "enabled in the Discord Developer Portal.",
            )
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            self.ui.call(self._on_connect_error, f"Connection failed: {e}")

    def _on_connect_error(self, message):
        self.toolbar.set_status("Disconnected", "disconnected")
        MessageDialog(self.root, "Connection Failed", message, error=True)

    def _on_ready(self):
        self.toolbar.set_status(f"Connected as {self.discord.client.user}", "connected")
        self.servers.clear()
        for guild in self.discord.client.guilds:
            icon_url = str(guild.icon.url) if guild.icon else None
            self.servers.add_server(guild.name, lambda g=guild: self.select_server(g), icon_url=icon_url)

    def _on_disconnected(self):
        self.toolbar.set_status("Disconnected", "disconnected")

    # ---------------- navigation ----------------

    def select_server(self, guild):
        self.state["active_guild_id"] = guild.id
        self.state["active_channel_id"] = None
        self.state["active_channel"] = None

        self.channels.clear()
        for channel in guild.text_channels:
            self.channels.add_channel(channel.name, lambda c=channel: self.select_channel(c))

        self.members.clear()
        member_data = []
        for member in guild.members:
            status = str(member.status) if member.status else "offline"
            avatar_url = str(member.display_avatar.url) if member.display_avatar else None
            member_data.append({
                "name": member.display_name,
                "bot": member.bot,
                "status": status,
                "avatar_url": avatar_url,
            })
        self.members.add_members_sorted(member_data)

        self.chat.clear_messages()
        self.chat.set_channel("Select a channel")

    def select_channel(self, channel):
        self.state["active_channel_id"] = channel.id
        self.state["active_channel"] = channel
        self.chat.set_channel(channel.name)
        self.chat.clear_messages()

        if not self.config.get("load_history", True):
            return

        limit = self.config.get("history_limit", 100)
        future = self.discord.fetch_history(channel, limit)
        future.add_done_callback(lambda f: self._on_history_loaded(channel.id, f))

    def _on_history_loaded(self, channel_id, future):
        try:
            messages = future.result()
        except Exception as e:
            logger.error(f"Failed to load history: {e}")
            return
        # If the user has since switched channels, don't paint stale history.
        if self.state.get("active_channel_id") != channel_id:
            return
        self.ui.call(self._display_history, messages)

    def _display_history(self, messages):
        for message in messages:
            self._render_message(message)

    # ---------------- messaging ----------------

    def send_message(self, content):
        channel = self.state.get("active_channel")
        if channel is None:
            MessageDialog(self.root, "No Channel Selected", "Pick a channel before sending a message.")
            return
        try:
            self.discord.send_message(channel, content)
        except Exception as e:
            logger.error(f"Failed to send message: {e}")

    def send_file(self, filepath):
        channel = self.state.get("active_channel")
        if channel is None:
            MessageDialog(self.root, "No Channel Selected", "Pick a channel before sending a file.")
            return
        if self.discord.loop is None:
            MessageDialog(self.root, "Not Connected", "Connect before sending files.", error=True)
            return
        try:
            filename = filepath.split("/")[-1].split("\\")[-1]
            uploader = UploadManager(self.discord.loop)
            uploader.upload(channel, filepath, filename)
        except Exception as e:
            logger.error(f"Failed to send file: {e}")
            MessageDialog(self.root, "Upload Failed", str(e), error=True)

    def _on_message_received(self, message):
        self._render_message(message)

    def _render_message(self, message):
        is_self = self.discord.client.user is not None and message.author.id == self.discord.client.user.id
        timestamp = message.created_at.strftime("%H:%M") if message.created_at else None

        parts = []
        if message.content:
            parts.append(message.content)
        for attachment in message.attachments:
            parts.append(f"[attachment: {attachment.filename}] {attachment.url}")
        for embed in message.embeds:
            title = embed.title or "(embed)"
            parts.append(f"[embed: {title}]")
        content = "\n".join(parts) if parts else "[empty message]"

        self.chat.add_message(message.author.display_name, content, timestamp=timestamp, is_self=is_self)

    # ---------------- shutdown ----------------

    def on_close(self):
        try:
            self.discord.stop()
        except Exception:
            pass
        self.root.destroy()

    def run(self):
        self.window.run()


if __name__ == "__main__":
    Application().run()
