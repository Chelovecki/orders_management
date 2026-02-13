# src/api/orders/tasks.py
import time

from src.celery_app import celery_app


@celery_app.task
def process_order_task(order_id: str):
    time.sleep(2)
    print(f"✅ Order {order_id} processed")
