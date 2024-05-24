# handler.py

from service import RabbitMQService
import os
import subprocess

class FileCreationHandler:
    def __init__(self):
        self.rabbitmq_service = RabbitMQService()

    def create_file(self, filename, content):
        # Certifique-se de que o diretório ./tmp existe
        filepath = os.path.join('tmp', filename)
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)

    def process_input(self, input_data):
        # Carregar o JSON
        data = input_data

        # Criar arquivos
        self.create_file('service.py', data['service'])
        self.create_file('handler.py', data['handler'])
        self.create_file('application.py', data['application'])
        self.create_file('.env', data['env'])
        # Criar requirements.txt na pasta ./tmp
        self.create_file('requirements.txt', data['requirements'])

        # Criar Dockerfile
        dockerfile_content = '''
# Dockerfile
FROM python:3.9-alpine

WORKDIR /app

COPY . /app

# Instale as dependências Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "application.py"]
        '''
        self.create_file('Dockerfile', dockerfile_content)

        # Criar arquivo de deploy (docker-compose.yml para Swarm)
        docker_compose_content = '''
version: '3.8'
services:
  url-status-checker:
    image: igoralcantara/app:v0.01
    build: .
    deploy:
      replicas: 1
      restart_policy:
        condition: on-failure
    networks:
      - minha_rede
networks:
  minha_rede:
    external: true
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
        docker build . -t igoralcantara/app:v0.01
    - name: publish
        run: |
        docker login -u igoralcantara -p ${{ secrets.DOCKER_HUB_TOKEN }}
        docker push igoralcantara/app:v0.01
        '''
        self.create_file('.github/workflows/publish-image.yaml', publish_image_content)

        print("Arquivos criados com sucesso.")
        
        # Retornar uma mensagem de sucesso
        return {"status": "success", "message": "Files created successfully"}

    def run_git_commands(self):
        #github_username = os.getenv('GITHUB_USERNAME')
        github_username = "ialcantara2901"
        #github_token = os.getenv('GITHUB_TOKEN')
        g_token = "${{ secrets.G_TOKEN }}"
        repository_url = f'https://{github_username}:{g_token}@github.com/{github_username}/creator.git'
        
        commands = [
            "git init",
            f"git remote add origin {repository_url}",
            "git add .",
            'git commit -m "Start IA app"',
            "git branch -M main",
            "git push -u origin main"
        ]
        cwd = './tmp'
        for command in commands:
            subprocess.run(command, cwd=cwd, shell=True, check=True)
        print("Comandos Git executados com sucesso.")
        
        cwd = './tmp'
        for command in commands:
            subprocess.run(command, cwd=cwd, shell=True, check=True)
        print("Comandos Git executados com sucesso.")

    def handle_message(self, message):
        result = self.process_input(message)
        self.rabbitmq_service.send_message('creator_out', result)
