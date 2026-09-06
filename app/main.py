from fastapi import FastAPI
from uuid import UUID, uuid4

app = FastAPI(title="Distributed LLM Evaluation Platform")


@app.get("/health")
def health() -> dict[str, str]: 
    print("Health check")
    return {"status": "ok"}

'''
LLM Evaluation Platform
1. Happy path - get runs endpoint set up.
2. Pushes to database, push runs to queue. 
3. Worker thread polls queue. It starts up and executes the run. 

Redis for queue?

Worker on dev - a python server that keeps running

Questions
1. I think uvicorn isn't updating the app bc updating print statements aren't taking effect. 

Remidner: 
    - Don't defer pydantic too long
'''

@app.post("/runs")
def create_run() -> dict[str, UUID]:
    run_id: UUID = uuid4()
    print(f"Created run ifd: {run_id}")
    '''
        {
            "run_id": "...",
            "case_execution_id": "..."
        }
    '''
    # Add to queue 
    return {"run_id": run_id, "case_execution_id": case_execution_id}

