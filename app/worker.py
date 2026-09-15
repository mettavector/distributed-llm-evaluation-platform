from rabbitmq_amqp_python_client import (
    AddressHelper,
    AMQPMessagingHandler, Event, Environment, Converter
)

queue_name = "runs_queue"
queue_address = AddressHelper.queue_address(queue_name)
environment = Environment(uri="amqp://guest:guest@queue:5672")
connection = environment.connection()
connection.dial()
print('Connection success!')

class MessageHandler(AMQPMessagingHandler):
    def __init__(self):
        super().__init__()

    def on_message(self, event: Event):
        print('message recieved!')
        my_body_string = Converter.bytes_to_string(event.message.body)
        print('body string is' + my_body_string)
        self.delivery_context.accept(event)
    
queue_address = AddressHelper.queue_address('runs_queue')
consumer = connection.consumer(queue_address, message_handler=MessageHandler())

try:
    print(" [*] Worker started. Waiting for messages...")
    consumer.run()  # Blocks here, actively listening and handling I/O
except KeyboardInterrupt:
    print(" [*] Stopping worker gracefully...")
finally:
    consumer.close()
    connection.close()