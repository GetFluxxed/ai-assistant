from fastapi import FastAPI
from pydantic import BaseModel

from rag import answer_question


app = FastAPI(
    title="Company Knowledge AI"
)


class QuestionRequest(BaseModel):

    question: str


@app.post("/ask")
def ask_question(
    request: QuestionRequest
):

    return answer_question(
        request.question
    )