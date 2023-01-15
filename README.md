# Y_Lab FastAPI education project

Homework project for Y_Lab University

## Description:

Educational FastAPI project with full CRUD functionality and async operations.

## Tech:

Based on:
- Python 3.10
- FastAPI 0.89.1
- SQLModel 0.0.8
- Alembic 1.9.1
- Uvicorn 0.20.0
- PostgreSQL 15.0

## Setup Guide

### Download or clone GitHub repository

https://github.com/john-neg/ylab_fastapi_project.git

### Make .env file with database settings data in project root directory

```
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```
If you run app on local machine you can bypass this step and the app will use 
the default above settings. 

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