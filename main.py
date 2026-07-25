from fastapi import FastAPI
from rag_service import responder_pergunta
app=FastAPI()

@app.get("/")
def home():
    return {"mensagem":"A minha primeira API esta a funcioanr"}

@app.get("/pergunta")
def pergunta(pergunta:str):
    resposta=responder_pergunta(pergunta,r"C:\Dev\python-fundamentos\exercicos\Zoho_Caderno_Encargos_CRM_ServicosEnergias.pdf")# o r diz para ignorar os \ senao nao dava certo
    return resposta