import asyncio
import discord

from core.logger import logger


class DiscordManager:

    def __init__(self, app):

        self.app = app

        self.client = None

        self.loop = None

    def create_client(self):

        intents = discord.Intents.all()

        self.client = discord.Client(
            intents=intents
        )

        return self.client

    def start(self, token):

        self.loop = asyncio.new_event_loop()

        asyncio.set_event_loop(self.loop)

        self.create_client()

        self.register_events()

        logger.info("Connecting to Discord")

        self.loop.run_until_complete(

            self.client.start(token)

        )

    def stop(self):

        if self.client:

            asyncio.run_coroutine_threadsafe(

                self.client.close(),

                self.loop

            )

    def register_events(self):

        events = self.app.events

        @self.client.event
        async def on_ready():
            await events.on_ready()

        @self.client.event
        async def on_message(message):
            await events.on_message(message)

        @self.client.event
        async def on_typing(channel, user, when):
            await events.on_typing(channel, user, when)

        @self.client.event
        async def on_member_update(before, after):
            await events.on_member_update(before, after)

        @self.client.event
        async def on_disconnect():
            await events.on_disconnect()

        @self.client.event
        async def on_resumed():
            await events.on_resumed()

    def send_message(self, channel, content):
        """Schedules a message send on the Discord thread's event loop from
        the Tk main thread. Accepts the channel object directly (from the
        caller's own reference) rather than re-resolving by ID, so this
        doesn't depend on cache-lookup timing. Returns a
        concurrent.futures.Future -- callers that need the result can call
        .result(), but for fire-and-forget sends from the UI, that's not
        required."""
        return asyncio.run_coroutine_threadsafe(
            channel.send(content),
            self.loop,
        )

    def fetch_history(self, channel, limit):
        """Same threadsafe-scheduling pattern as send_message, but for
        pulling recent message history when a channel is first opened."""

        async def _fetch():
            messages = [m async for m in channel.history(limit=limit)]
            messages.reverse()  # oldest first, matches natural reading order
            return messages

        return asyncio.run_coroutine_threadsafe(_fetch(), self.loop)