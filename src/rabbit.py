import logging

import aio_pika

from src.settings import RabbitSettings

logger = logging.getLogger(__name__)

_rabbit_channel = None
_rabbit_connection = None


async def init_rabbit():
    global _rabbit_channel, _rabbit_connection
    _rabbit_connection = await aio_pika.connect_robust(RabbitSettings.URL)
    _rabbit_channel = await _rabbit_connection.channel()
    await _rabbit_channel.declare_queue("new_order", durable=True)
    logger.info("Connected to RabbitMQ")
    return _rabbit_channel


async def close_rabbit():
    global _rabbit_connection
    if _rabbit_connection:
        await _rabbit_connection.close()
