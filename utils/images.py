import threading
import requests

from io import BytesIO
from PIL import Image, ImageTk

from core.logger import logger


class ImageLoader:

    def __init__(self):

        self.cache = {}

    def load_async(self, url, callback):

        if url in self.cache:
            callback(self.cache[url])
            return

        def worker():

            try:

                response = requests.get(
                    url,
                    timeout=10
                )

                image = Image.open(
                    BytesIO(response.content)
                )

                image.thumbnail((200, 200))

                photo = ImageTk.PhotoImage(image)

                self.cache[url] = photo

                callback(photo)

            except Exception:
                logger.exception("Image download failed")

        threading.Thread(
            target=worker,
            daemon=True
        ).start()