from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.graph import create_graph

app = FastAPI(title="Insurance Agentic AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = create_graph()


class QueryRequest(BaseModel):
    question: str


@app.post("/analyze")
def analyze(req: QueryRequest):
    state = {"question": req.question}

    result = graph.invoke(state)

    if "final_answer" not in result:
        return JSONResponse(
            status_code=200,
            content={
                "question": req.question,
                "decision": {"decision": "Not Covered", "reason": "No relevant policy context found."},
                "final_answer": "No matching policy information was found for this query."
            }
        )

    return {
        "question": req.question,
        "decision": result["decision"],
        "final_answer": result["final_answer"]
    }
