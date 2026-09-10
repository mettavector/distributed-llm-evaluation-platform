import json
from fastapi import FastAPI
from uuid import UUID, uuid4
from rabbitmq_amqp_python_client import (Connection, Message, Environment)
from contextlib import asynccontextmanager


# def create_connection() -> Connection: 
#     connection.dial()
#     return connection
connection = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    exchange_name = "runs"
    queue_name = "runs_queue"
    routing_key = "runs"
    environment = Environment(uri="amqp://guest:guest@queue:5672")
    connection = environment.connection()
    connection.dial()
    yield
    environment.close()

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
def create_run() -> dict[str, UUID]:
    run_id: UUID = uuid4()
    print(f"Created run ifd: {run_id}")
    job = {
                "run_id": "xyz", "case": {
                    "test_case_id": "lexical_count_01", 
                    "battery_id": "battery_01"
                },
                "model_config": {
                    "name": "fake_model",
                    "provider": "mock",
                    "temperature": 0
                }
    }
    


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