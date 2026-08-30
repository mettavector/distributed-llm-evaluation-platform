from fastapi import FastAPI


app = FastAPI(title="Distributed LLM Evaluation Platform")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
