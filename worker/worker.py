import pika
import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.models import Base, Task, Order

DATABASE_URL = os.getenv("DATABASE_URL")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def callback(ch, method, properties, body):
    data = json.loads(body)
    db = SessionLocal()

    # ---------------- TASKS ----------------
    if data.get("type") == "task":
        task = db.query(Task).filter(Task.id == data["task_id"]).first()

        if not task:
            return

        if data["action"] == "create":
            task.status = "completed"

        elif data["action"] == "delete":
            db.delete(task)

        db.commit()
        print(f"Processed task {task.id}")

    # ---------------- ORDERS ----------------
    elif data.get("type") == "order":
        order = db.query(Order).filter(Order.id == data["order_id"]).first()

        if not order:
            return

        if data["action"] == "create":
            print(f"Processing order {order.id}")
            order.status = "processing"
            db.commit()

            # Simular trabajo pesado
            import time
            time.sleep(3)

            order.status = "completed"

        db.commit()
        print(f"Processed order {order.id}")

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBITMQ_HOST)
)

channel = connection.channel()
channel.queue_declare(queue='tasks')

channel.basic_consume(
    queue='tasks',
    on_message_callback=callback,
    auto_ack=True
)

print("Worker started...")
channel.start_consuming()