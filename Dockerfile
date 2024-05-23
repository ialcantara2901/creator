# Dockerfile
FROM python:3.9-alpine

WORKDIR /app

COPY . /app

# Instale as dependências Python
RUN pip install --upgrade pip
RUN pip install pika
RUN pip install python-dotenv

CMD ["python", "main.py"]