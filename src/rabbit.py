# src/rabbit.py
import aio_pika

from src.settings import RabbitSettings

rabbit_channel = None
rabbit_connection = None


async def init_rabbit():
    global rabbit_channel, rabbit_connection
    rabbit_connection = await aio_pika.connect_robust(RabbitSettings.URL)
    rabbit_channel = await rabbit_connection.channel()
    await rabbit_channel.declare_queue("new_order", durable=True)
    return rabbit_channel


async def close_rabbit():
    if rabbit_connection:
        await rabbit_connection.close()
