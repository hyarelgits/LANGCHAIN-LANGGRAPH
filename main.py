from fastapi import FastAPI
from pydantic import BaseModel
from langgraph_flow import run_loan_flow

app = FastAPI(title="Hyarel Loan AI")

class LoanRequest(BaseModel):
    user_name: str = "Hyarel"
    question: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
def ask(req: LoanRequest):
    answer = run_loan_flow(req.question, req.user_name)
    return {"user_name": req.user_name, "question": req.question, "answer": answer}
