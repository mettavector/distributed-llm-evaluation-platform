import json
from datetime import (timedelta, datetime)
from zoneinfo import ZoneInfo

from fastapi import FastAPI, Request
from uuid import UUID, uuid4
from rabbitmq_amqp_python_client import (
    Connection, Message, Environment, 
    ClassicQueueSpecification, ExchangeSpecification, AddressHelper
)
from contextlib import asynccontextmanager

exchange_name = "runs"
queue_name = "runs_queue"
routing_key = "runs"
queue_address = AddressHelper.queue_address(queue_name)

@asynccontextmanager
async def lifespan(app: FastAPI):
    environment = Environment(uri="amqp://guest:guest@queue:5672")
    connection = environment.connection()
    connection.dial()

    app.state.connection = connection

    # Declare queue
    management = connection.management()

    # management.delete_queue(name=queue_name)

    management.declare_queue(
        ClassicQueueSpecification(
            name=queue_name,
            message_ttl=timedelta(minutes=10),
            max_len_bytes=100000000 # 100MB
        ),
    )       
    
    publisher = connection.publisher() # declares a publisher?
    app.state.publisher = publisher
    
    try:
        yield
    finally:
        environment.close()

    # Close publisher

def send_message(message, publisher):
    message = Message(body=message.encode("utf-8"))
    message = AddressHelper.message_to_address_helper(message, queue_address)
    publisher.publish(message)

app = FastAPI(title="Distributed LLM Evaluation Platform", lifespan=lifespan)

@app.get("/health")
def health() -> dict[str, str]: 
    print("Health check")
    return {"status": "ok"}

'''
LLM Evaluation Platform
1. Happy path - get runs endpoint set up.
2. Pushes to database, push runs to queue. 
3. Worker thread polls queue. It starts up and executes the run. 


Worker on dev - a python server that keeps running

Questions
1. I think uvicorn isn't updating the app bc updating print statements aren't taking effect. 

On 

Remidner: 
    - Don't defer pydantic too long
'''

@app.post("/runs")
def create_run(request: Request) -> dict[str, UUID]:
    run_id: UUID = uuid4()
    case_execution_id: UUID = uuid4()
    print(f"Created run ifd: {run_id}")
    job = {
                "run_id": str(run_id), 
                "case_execution_id": str(case_execution_id),
                "case": {
                    "test_case_id": "lexical_count_01", 
                    "battery_id": "battery_01"
                },
                "model_config": {
                    "name": "fake_model",
                    "provider": "mock",
                    "temperature": 0
                }
    }
    
    # Enqueue job
    send_message(
        json.dumps(job), request.app.state.publisher
    )

    return {"run_id": run_id, "case_execution_id": case_execution_id}

TEST_REGISTRY = {
    "battery_01": [
        {
            "test_case_id": "lexical_count_01",
            "input": "How many R's in racecar?",
            "expected": "2"
        }, 
        {
            "test_case_id": "geographical_knowledge_01",
            "input": "What's the capital of the state to the south of Oregon?",
            "expected": "Sacramento"
        }, 
        
    ]
}