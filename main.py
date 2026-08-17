# main.py

from typing import Annotated

from fastapi import FastAPI, HTTPException, Query

from rag_service import responder_pergunta


app = FastAPI()


CAMINHO_PDF = r"caminho_pdf"

@app.get("/")
def home():
    return {"mensagem": "A minha primeira API está a funcionar"}


@app.get("/question")
def question(
    pergunta: Annotated[
        str,
        Query(
            min_length=3,
            max_length=500,
            description="Pergunta sobre o conteúdo do PDF",
        ),
    ],
):
    try:
        answer = responder_pergunta(pergunta, CAMINHO_PDF)

        return {
            "question": pergunta,
            "answer": answer,
        }

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="O ficheiro PDF não foi encontrado.",
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
             detail=f"Ocorreu um erro ao processar a pergunta: {str(e)}",
        )
