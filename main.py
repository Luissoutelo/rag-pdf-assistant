from fastapi import FastAPI
from rag_service import answer_question

app = FastAPI()


@app.get("/")
def home():
    return {"message": "My first API is working!"}


@app.get("/question")
def question(question: str):
    answer = answer_question(question, r"C:\Dev\python-fundamentos\exercicos\Zoho_Caderno_Encargos_CRM_ServicosEnergias.pdf")  # r tells Python to ignore \ as escape characters
    return answer
