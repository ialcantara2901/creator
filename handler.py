# handler.py

from service import RabbitMQService
import os, json

class FileCreationHandler:
    def __init__(self):
        self.rabbitmq_service = RabbitMQService()

    def create_file(self, filename, content):
        # Certifique-se de que o diretório existe
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)

    def process_input(self, input_data):
        # Carregar o JSON
        data = json.loads(input_data)

        # Criar arquivos
        self.create_file('service.py', data['service'])
        self.create_file('handler.py', data['handler'])
        self.create_file('application.py', data['application'])
        self.create_file('.env', data['env'])

        # Criar Dockerfile
        dockerfile_content = '''
        # Dockerfile
        FROM python:3.9-alpine
        
        WORKDIR /app
        
        COPY . /app
        
        # Instale as dependências Python
        RUN pip install --upgrade pip
        RUN pip install pika
        RUN pip install python-dotenv
        
        CMD ["python", "application.py"]
        '''
        self.create_file('Dockerfile', dockerfile_content)

        # Criar arquivo de deploy (docker-compose.yml para Swarm)
        docker_compose_content = '''
        version: '3.8'
        services:
          url-status-checker:
            image: url_status_checker:latest
            build: .
            deploy:
              replicas: 1
              restart_policy:
                condition: on-failure
            networks:
              - url-net
        networks:
          url-net:
        '''
        self.create_file('docker-compose.yml', docker_compose_content)

        # Criar arquivo publish-image.yaml
        publish_image_content = '''
        name: Publish image docker hub
        on:
        push:
            branches:
            - 'main'

        jobs:
        publish_image:
            runs-on: ubuntu-latest
            steps:
            - name: checkout
                uses: actions/checkout@v4
            - name: build
                run: |
                docker build . -t igoralcantara/app:creator1-v0.01
            - name: publish
                run: |
                docker login -u igoralcantara -p ${{ secrets.DOCKER_HUB_TOKEN }}
                docker push igoralcantara/app:creator1-v0.01
        '''
        self.create_file('.github/workflows/publish-image.yaml', publish_image_content)

        print("Arquivos criados com sucesso.")
        
        # Retornar uma mensagem de sucesso
        return {"status": "success", "message": "Files created successfully"}

    def handle_message(self, message):
        result = self.process_input(message)
        self.rabbitmq_service.send_message('creator_out', result)
