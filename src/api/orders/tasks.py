# src/api/orders/tasks.py
import time

from src.celery_app import celery_app


@celery_app.task
def process_order_task(order_id: str):
    print(f"🔄 Начинаем обработку заказа {order_id}")
    time.sleep(2)
    print(f"✅ Заказ {order_id} обработан")
    return f"Order {order_id} processed"
