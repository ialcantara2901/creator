# handler.py

from service import RabbitMQService

class FileCreationHandler:
    def __init__(self):
        self.rabbitmq_service = RabbitMQService()

    def create_file(self, filename, content):
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)

    def process_input(self, input_data):
        # Carregar o JSON
        data = input_data

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
        
        RUN pip install requests
        
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

        print("Arquivos criados com sucesso.")
        
        # Retornar uma mensagem de sucesso
        return {"status": "success", "message": "Files created successfully"}

    def handle_message(self, message):
        result = self.process_input(message)
        self.rabbitmq_service.send_message('creator_out', result)
