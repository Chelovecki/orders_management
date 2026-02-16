# src/celery_app.py
import time

from celery import Celery

from src.settings import RedisSettings as r

celery_app = Celery(
    "orders",
    broker=f"redis://{r.HOST}:{r.PORT}/{r.DB_CELERY}",
    backend=f"redis://{r.HOST}:{r.PORT}/{r.DB_CELERY}",
)
