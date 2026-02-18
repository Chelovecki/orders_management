import asyncio
import json
import logging

import aio_pika

from src.api.orders.tasks import process_order_task
from src.settings import RabbitSettings

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def wait_for_rabbit(max_retries=10, delay=3):
    for attempt in range(max_retries):
        try:
            connection = await aio_pika.connect_robust(RabbitSettings.URL)
            await connection.close()
            logger.info("RabbitMQ ready")
            return
        except (aio_pika.exceptions.AMQPConnectionError, ConnectionRefusedError) as e:
            logger.error(
                f"Waiting for RabbitMQ ({attempt + 1}/{max_retries})... Error: {e}"
            )
        await asyncio.sleep(delay)
    raise Exception("RabbitMQ not available after retries")


async def main():
    logger.info("Consumer started")
    logger.info(f"Connecting to: {RabbitSettings.URL}")

    await wait_for_rabbit()
    logger.info("wait_for_rabbit passed")

    try:
        logger.info("Creating permanent connection...")
        connection = await aio_pika.connect_robust(RabbitSettings.URL)
        logger.info("Connection established")

        async with connection:
            logger.info("Creating channel...")
            channel = await connection.channel()
            logger.info("Channel created")

            await channel.set_qos(prefetch_count=1)
            logger.info("QoS set")

            logger.info("Declaring queue 'new_order'...")
            queue = await channel.declare_queue("new_order", durable=True)
            logger.info("Queue declared")

            logger.info("Waiting for messages...")
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        data = json.loads(message.body.decode())
                        order_id = data["order_id"]
                        logger.info(f"Received order: {order_id}")
                        process_order_task.delay(order_id)
                        logger.info(f"Sent to Celery: {order_id}")
    except Exception as e:
        logger.exception(f"Consumer crashed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
