# src/celery_app.py
import time

from celery import Celery

from src.settings import RedisSettings as r

celery_app = Celery(
    "orders",
    broker=f"redis://{r.HOST}:{r.PORT}/{r.DB_CELERY}",
    backend=f"redis://{r.HOST}:{r.PORT}/{r.DB_CELERY}",
)


@celery_app.task
def process_order_task(order_id: str):
    print(f"🔄 Начинаем обработку заказа {order_id}")
    time.sleep(2)
    print(f"✅ Заказ {order_id} обработан")
    return f"Order {order_id} processed"
