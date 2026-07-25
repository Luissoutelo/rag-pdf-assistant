import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_community.document_loaders import PyPDFLoader #ferramenta que le ficheiros
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def _carregar_pdf(caminho):
   loader = PyPDFLoader(caminho)
   documentos=loader.load()
   return documentos

def _dividir_em_chunks(documentos):   
    splitter= RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=150) 
    chunks=splitter.split_documents(documentos)
    return chunks
def _criar_vetoresstore(chunks):
    vectorstore = Chroma.from_documents(chunks, embeddings)
    return vectorstore
    
def _procurar_chunk(pergunta, vectorstore):
    resultados = vectorstore.similarity_search(pergunta, k=3)
    return resultados
    
    
    
def _perguntar_llm(pergunta,chunk):
    prompt = f"Contexto: {chunk}\n\nPergunta: {pergunta}\n\nResponde com base apenas no contexto."
    modelo_ia = genai.GenerativeModel('gemini-2.5-flash')
    resposta = modelo_ia.generate_content(prompt)
    return resposta.text
def responder_pergunta(pergunta,caminho_pdf):
    documentos = _carregar_pdf(caminho_pdf)
    chunks = _dividir_em_chunks(documentos)
    vectorstore = _criar_vetoresstore(chunks)
    resultados = _procurar_chunk(pergunta, vectorstore)
    contexto="\n\n".join([r.page_content for r in resultados])
    resposta = _perguntar_llm(pergunta, contexto)
    return resposta