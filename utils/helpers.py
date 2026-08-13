import asyncio

from core.logger import logger


def run_async(loop, coro, timeout=30):

    future = asyncio.run_coroutine_threadsafe(

        coro,

        loop

    )

    try:

        return future.result(timeout)

    except Exception:

        logger.exception("Coroutine failed")

        raise