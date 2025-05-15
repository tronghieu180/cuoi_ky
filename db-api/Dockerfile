FROM python:3.11-slim

COPY requirements.txt .

RUN apt-get update && apt-get install -y gcc libpq-dev

RUN pip install -r requirements.txt

WORKDIR /app

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]