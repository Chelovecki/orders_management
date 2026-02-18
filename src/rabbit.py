import asyncio
import aio_pika
from src.settings import RabbitSettings

rabbit_channel = None
rabbit_connection = None

async def init_rabbit(max_retries=10, delay=3):
    global rabbit_channel, rabbit_connection
    for attempt in range(max_retries):
        try:
            rabbit_connection = await aio_pika.connect_robust(RabbitSettings.URL)
            rabbit_channel = await rabbit_connection.channel()
            await rabbit_channel.declare_queue("new_order", durable=True)
            print("✅ Connected to RabbitMQ")
            return rabbit_channel
        except (aio_pika.exceptions.AMQPConnectionError, ConnectionRefusedError) as e:
            print(f"⏳ RabbitMQ not ready (attempt {attempt+1}/{max_retries}), retrying in {delay}s...")
            if attempt < max_retries - 1:
                await asyncio.sleep(delay)
            else:
                print("❌ Failed to connect to RabbitMQ after retries")
                raise  # если критично – приложение упадёт

async def close_rabbit():
    global rabbit_connection
    if rabbit_connection:
        await rabbit_connection.close()