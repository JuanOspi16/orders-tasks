# Sistema de Procesamiento Asíncrono con Docker, RabbitMQ y Python

## Descripción general

Este proyecto implementa un sistema distribuido basado en arquitectura orientada a eventos, donde se procesan **Tasks** y **Orders** de manera asíncrona utilizando una cola de mensajes.

El sistema permite:

* Crear tareas (`tasks`)
* Crear órdenes (`orders`)
* Procesarlas de forma asíncrona
* Consultar su estado
* Eliminar tareas

---

## Arquitectura del sistema

> Insertar aquí la imagen de la arquitectura:

![Arquitectura del sistema](./arquitectura.png)

---

## Componentes

El sistema está compuesto por:

### 1. API REST (FastAPI)

* Expone endpoints HTTP
* Recibe solicitudes del cliente
* Publica mensajes en RabbitMQ
* Consulta el estado en la base de datos

### 2. RabbitMQ

* Actúa como broker de mensajes
* Maneja la comunicación asíncrona entre servicios

### 3. Worker (Consumer)

* Consume mensajes desde RabbitMQ
* Ejecuta la lógica de negocio
* Actualiza la base de datos

### 4. PostgreSQL

* Almacena:

  * `tasks`
  * `orders`

---

## Flujo del sistema

1. Cliente hace una petición (POST /tasks o POST /orders)
2. La API:

   * Guarda el registro en la base de datos
   * Envía un mensaje a RabbitMQ
3. El worker:

   * Consume el mensaje
   * Procesa la tarea u orden
   * Actualiza su estado
4. El cliente consulta el estado mediante GET

---

## Tecnologías utilizadas

* Python 3.11
* FastAPI
* RabbitMQ
* PostgreSQL
* Docker
* Docker Compose

---

## Cómo ejecutar el proyecto

### 1. Construir y levantar los servicios

```bash
docker compose up --build
```

### 2. Ejecutar en segundo plano (opcional)

```bash
docker compose up -d
```

---

## Endpoints disponibles

### Crear una Task

```bash
curl -X POST http://localhost:8000/tasks
```

---

### Obtener una Task

```bash
curl http://localhost:8000/tasks/1
```

---

### Eliminar una Task (asíncrono)

```bash
curl -X DELETE http://localhost:8000/tasks/1
```

---

### Crear una Order

```bash
curl -X POST http://localhost:8000/orders
```

---

### Obtener una Order

```bash
curl http://localhost:8000/orders/1
```

---

## Estados del sistema

### Tasks:

* `pending`
* `completed`

### Orders:

* `created`
* `processing`
* `completed`

---

## Pruebas rápidas

Crear múltiples órdenes:

```bash
for i in {1..5}; do curl -X POST http://localhost:8000/orders; done
```

---

## Panel de RabbitMQ

Puedes acceder a la interfaz web en:

```
http://localhost:15672
```

Credenciales:

```
usuario: guest
contraseña: guest
```

---

## Acceso a la base de datos

```bash
docker exec -it orders-tasks-db-1 psql -U user -d tasksdb
```

Comandos útiles:

```sql
\dt
SELECT * FROM tasks;
SELECT * FROM orders;
```

---

## Características clave

* Procesamiento asíncrono con colas
* Separación de responsabilidades
* Escalable (puedes agregar múltiples workers)
* Arquitectura tipo microservicios (base)

---

## Posibles mejoras

* Reintentos automáticos (retry)
* Dead Letter Queue
* Autenticación en la API
* Logs centralizados
* Monitoreo (Prometheus/Grafana)
* Separación completa en microservicios

---

## Autor

Proyecto desarrollado como implementación de arquitectura distribuida con mensajería asíncrona usando Docker.
