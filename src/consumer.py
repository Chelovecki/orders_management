import asyncio
import json
import aio_pika
from src.api.orders.tasks import process_order_task
from src.settings import RabbitSettings

async def wait_for_rabbit(max_retries=10, delay=3):
    for attempt in range(max_retries):
        try:
            connection = await aio_pika.connect_robust(RabbitSettings.URL)
            await connection.close()
            print("✅ RabbitMQ ready")
            return
        except (aio_pika.exceptions.AMQPConnectionError, ConnectionRefusedError):
            print(f"⏳ Waiting for RabbitMQ (attempt {attempt+1}/{max_retries})...")
            await asyncio.sleep(delay)
    raise Exception("❌ RabbitMQ not available after retries")

async def main():
    await wait_for_rabbit()
    connection = await aio_pika.connect_robust(RabbitSettings.URL)
    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)
        queue = await channel.declare_queue("new_order", durable=True)
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    data = json.loads(message.body.decode())
                    order_id = data["order_id"]
                    print(f"📦 Получен заказ: {order_id}")
                    process_order_task.delay(order_id)
                    print(f"✅ Отправлено в Celery: {order_id}")

if __name__ == "__main__":
    asyncio.run(main())