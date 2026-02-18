import logging
import time

from src.celery_app import celery_app

logger = logging.getLogger("celery")


@celery_app.task
def process_order_task(order_id: str):
    logger.info(f"Начинаем обработку заказа {order_id}")
    time.sleep(2)
    logger.info(f"Заказ {order_id} обработан")
    return f"Order {order_id} processed"
