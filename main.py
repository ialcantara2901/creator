# application.py

from handler import FileCreationHandler

def main():
    handler = FileCreationHandler()
    rabbitmq_service = handler.rabbitmq_service

    def callback(message):
        handler.handle_message(message)

    rabbitmq_service.consume_messages('creator_in', callback)

if __name__ == '__main__':
    main()
