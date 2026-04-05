from fastapi import FastAPI
from sqlalchemy.orm import Session
import pika
import json
import os

from api.db import SessionLocal, engine
from api.models import Base, Task, Order

Base.metadata.create_all(bind=engine)

app = FastAPI()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")

def publish_message(message):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    channel = connection.channel()

    channel.queue_declare(queue='tasks')

    channel.basic_publish(
        exchange='',
        routing_key='tasks',
        body=json.dumps(message)
    )

    connection.close()


@app.post("/tasks")
def create_task():
    db: Session = SessionLocal()

    task = Task(status="pending")
    db.add(task)
    db.commit()
    db.refresh(task)

    publish_message({
        "type": "task",
        "task_id": task.id,
        "action": "create"
    })

    return {"task_id": task.id}


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    db: Session = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()

    return {
        "id": task.id,
        "status": task.status
    }


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    publish_message({
        "type": "task",
        "task_id": task_id,
        "action": "delete"
    })

    return {"message": "Delete requested"}

@app.post("/orders")
def create_order():
    db: Session = SessionLocal()

    order = Order(status="created")
    db.add(order)
    db.commit()
    db.refresh(order)

    publish_message({
        "type": "order",
        "order_id": order.id,
        "action": "create"
    })

    return {"order_id": order.id}


@app.get("/orders/{order_id}")
def get_order(order_id: int):
    db: Session = SessionLocal()
    order = db.query(Order).filter(Order.id == order_id).first()

    return {
        "id": order.id,
        "status": order.status
    }