# Y_Lab FastAPI education project

![](https://img.shields.io/badge/python-3.10-blue?style=flat-square)
![](https://img.shields.io/badge/fastapi-0.89.1-critical?style=flat-square)
![](https://img.shields.io/badge/aoiredis-2.0.1-red?style=flat-square)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

Homework project for Y_Lab University

## Description:

Educational FastAPI project with full CRUD functionality and async operations.
API Documentation and Schema available on title page (http://0.0.0.0:8000,
http://localhost:8000 or http://127.0.0.1:8000 depending on operating system
and software versions)

## Tech:

Based on:
- Python 3.10
- FastAPI 0.89.1
- SQLModel 0.0.8
- Alembic 1.9.2
- Uvicorn 0.20.0
- PostgreSQL 15.1
- Docker 20.10.22
- Redis 7.0.1
- Celery 5.2.7
- RabbitMQ 3.11.8

## Setup Guide

### Download or clone GitHub repository

https://github.com/john-neg/ylab_fastapi_project.git

## Running Docker container

### Make .env file with database settings data in project root directory

```
SERVER_NAME=localhost
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_CACHE_TIME=3600
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_DEFAULT_USER=rabbit
RABBITMQ_DEFAULT_PASS=rabbit
```

```sh
docker-compose up -d
```
To run tests container use next command
```sh
docker-compose -f docker-compose.tests.yaml up -d
```

## Running locally

### Make .env file with database settings data in project root directory

```
SERVER_NAME=localhost
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_CACHE_TIME=3600
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_DEFAULT_USER=rabbit
RABBITMQ_DEFAULT_PASS=rabbit
```

### Setup and activate venv

```sh
python3 -m venv venv
```

```sh
source venv/bin/activate
```

### Install requirements

```sh
pip install -r requirements.txt
```

### Create DB tables and apply migrations

```sh
alembic upgrade head
```

### Start App

```sh
python3 run.py
```

## Author info:
Evgeny Semenov

## License
MIT
