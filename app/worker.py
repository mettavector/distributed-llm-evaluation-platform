import sys 
from pathlib import Path

# Add the parent directory to the Python search path
parent_dir = str(Path(__file__).resolve().parent.parent)
sys.path.append(parent_dir)

# Now you can import your module normally
from evals import test_registry as registry

registry = registry.DEFAULT

import json
from rabbitmq_amqp_python_client import (
    AddressHelper,
    AMQPMessagingHandler, Event, Environment, Converter
)

from ollama import Client


queue_name = "runs_queue"
queue_address = AddressHelper.queue_address(queue_name)
environment = Environment(uri="amqp://guest:guest@queue:5672")
connection = environment.connection()
connection.dial()

class LLMHandler():
    def __init__(self):
        super().__init__()
        self.client = Client(host='http://host.docker.internal:11434', headers={'x-some-header': 'some-value'})

    def prompt_ollama(self, prompt):
        print('prompt was:' + str(prompt))
        response = self.client.chat(
        model='qwen3.6',
        messages=[
            {
            'role': 'user',
            'content': str(prompt), # should probably kind of sanitize this for some sorts
            },
        ],
        )
        # print(response['message']['content'])
        # or access fields directly from the response object
        # print(response.message.content)
        return response.message.content

class MessageHandler(AMQPMessagingHandler):
    def __init__(self):
        super().__init__()

    def on_message(self, event: Event):
        print('message recieved!')
        my_body_string = Converter.bytes_to_string(event.message.body)
        job = json.loads(my_body_string)

        case = job["case"]
        battery_id = case["battery_id"]
        test_case_id = case["test_case_id"]

        battery = registry[battery_id]

        print('body string is: ' + my_body_string)

        matched_test = None
        for test in battery:
            if test["test_case_id"] == test_case_id:
                matched_test = test
                break
        
        print('matched_test: ' + str(matched_test))

        newLLMHandler = LLMHandler().prompt_ollama(matched_test["input"])
        

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