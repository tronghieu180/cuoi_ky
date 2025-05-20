# Microservice with FastAPI, React, Docker and Nginx

A microservice-based application that **crawls data** from [MobileCity.vn](https://mobilecity.vn) using **RSS feeds**, and provides a **simple search web** to explore available products.


## 🧩 Features

- ✅ FastAPI microservices (`crawler`, `ingestion`, `api`)
- ✅ PostgreSQL database
- ✅ Frontend built with React + Vite
- ✅ Nginx reverse proxy


## 🗂️ Services Overview

| Service     | Description                            |
|-------------|----------------------------------------|
| `crawler`   | Fetches RSS feed, extracts product info |
| `ingestion` | Validates and stores data in DB        |
| `api`       | Exposes API endpoints for the frontend |
| `frontend`  | Search UI built with React + Vite      |


## 🔧 Run Setup

### Setup .env

```bash
DB_USER=username
DB_PASSWORD=password
DB_NAME=mydb

CRAWL_HOUR=0
CRAWL_MINUTE=0
```

### Run command

```bash
docker-compose up --build
```

- Access the app: [http://localhost:8080](http://localhost:8080)

- Access crawler Swagger UI: [http://localhost:8080/crawler/docs](http://localhost:8080/crawler/docs)

- Access database API Swagger UI: [http://localhost:8080/db/docs](http://localhost:8080/db/docs)


## 🛠️ Tech Stack

- 🐍 Python (FastAPI)
- 🐘 PostgreSQL
- ⚛️ React + Vite (frontend)
- 🐳 Docker, Docker Compose
- 🌐 Nginx


## 📁 Folder Structure

```
project/
├───crawler
│   └───app
│       ├───routes
│       └───services
├───db-api
│   └───app
│       ├───database
│       └───routes
├───frontend
│   ├───public
│   └───src
│       ├───assets
│       └───Component
├───ingestion
│   └───app
│       ├───routes
│       └───services
├───landing_zone
└───nginx
```
