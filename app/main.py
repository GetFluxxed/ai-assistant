from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from rag import answer_question

#Utilizing our API, users are able to write questions via the browser and recieve a response within window

app = FastAPI(
    title="Company Knowledge AI"
)


app.mount(
    "/static",
    StaticFiles(
        directory="static"
    ),
    name="static"
)


class QuestionRequest(BaseModel):

    question: str


@app.get("/")
def home():

    return FileResponse(
        "static/index.html"
    )


@app.post("/ask")
def ask_question(
    request: QuestionRequest
):

    return answer_question(
        request.question
    )