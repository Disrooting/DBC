import discord

from utils.helpers import run_async


class UploadManager:

    def __init__(self, loop):

        self.loop = loop

    def upload(
        self,
        channel,
        filepath,
        filename
    ):

        with open(filepath, "rb") as f:

            run_async(

                self.loop,

                channel.send(
                    file=discord.File(
                        f,
                        filename
                    )
                )

            )