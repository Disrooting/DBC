import time
from core.logger import logger


class ReconnectManager:

    def __init__(self):
        self.max_attempts = 5

    def execute(self, func):

        attempt = 0

        while attempt < self.max_attempts:

            try:
                return func()

            except Exception:
                delay = min(2 ** attempt, 30)

                logger.exception(
                    "Reconnect attempt %s failed. Retrying in %s seconds.",
                    attempt + 1,
                    delay
                )

                time.sleep(delay)

                attempt += 1

        raise RuntimeError("Maximum reconnect attempts reached.")