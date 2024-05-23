        # Dockerfile
        FROM python:3.9-alpine
        
        WORKDIR /app
        
        COPY . /app
        
        RUN pip install requests
        
        CMD ["python", "application.py"]