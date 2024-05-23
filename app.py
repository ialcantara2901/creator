# main.py

import json
import os

# Função para criar arquivos
def create_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

# Função principal
if __name__ == '__main__':
    # JSON de entrada
    input_json = '''
    {
        "applicationName": "URL Status Checker",
        "Description": "Verifica se a URL 'https://aalc.com.br' está ativa a cada 60 segundos.",
        "service": "# service.py\\n\\nimport requests\\nfrom datetime import datetime\\n\\nclass URLService:\\n    @staticmethod\\n    def check_url_status(url):\\n        try:\\n            response = requests.get(url)\\n            status = response.status_code == 200\\n        except requests.RequestException:\\n            status = False\\n        return status\\n\\n    @staticmethod\\n    def get_current_datetime():\\n        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')",
        "handler": "# handler.py\\n\\nfrom service import URLService\\n\\nclass URLStatusHandler:\\n    def __init__(self, url):\\n        self.url = url\\n\\n    def get_status(self):\\n        status = URLService.check_url_status(self.url)\\n        date_time = URLService.get_current_datetime()\\n        return {'hrl': self.url, 'status': status, 'dateTime': date_time}",
        "application": "# application.py\\n\\nimport time\\nimport json\\nfrom handler import URLStatusHandler\\n\\nURL_TO_CHECK = 'https://aalc.com.br'\\n\\nif __name__ == '__main__':\\n    handler = URLStatusHandler(URL_TO_CHECK)\\n    while True:\\n        status_data = handler.get_status()\\n        print(json.dumps(status_data))\\n        time.sleep(60)",
        "env": "# env.py\\n\\n# Este arquivo pode conter variáveis de ambiente ou configuração futura\\n# Atualmente não é necessário para a aplicação básica\\n"
    }
    '''
    
    # Carregar o JSON
    data = json.loads(input_json)
    
    # Criar arquivos
    create_file('service.py', data['service'])
    create_file('handler.py', data['handler'])
    create_file('application.py', data['application'])
    create_file('env.py', data['env'])
    
    # Criar Dockerfile
    dockerfile_content = '''
    # Dockerfile
    FROM python:3.9-slim
    
    WORKDIR /app
    
    COPY . /app
    
    RUN pip install requests
    
    CMD ["python", "application.py"]
    '''
    create_file('Dockerfile', dockerfile_content)
    
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
    create_file('docker-compose.yml', docker_compose_content)
    
    print("Arquivos criados com sucesso.")
