import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_community.document_loaders import PyPDFLoader  # tool that reads files
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def _load_pdf(path):
    loader = PyPDFLoader(path)
    documents = loader.load()
    return documents


def _split_into_chunks(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=150)
    chunks = splitter.split_documents(documents)
    return chunks


def _create_vectorstore(chunks):
    vectorstore = Chroma.from_documents(chunks, embeddings)
    return vectorstore


def _search_chunk(question, vectorstore):
    results = vectorstore.similarity_search(question, k=3)
    return results


def _ask_llm(question, chunk):
    prompt = f"Context: {chunk}\n\nQuestion: {question}\n\nAnswer based only on the context."
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    return response.text


def answer_question(question, pdf_path):
    documents = _load_pdf(pdf_path)
    chunks = _split_into_chunks(documents)
    vectorstore = _create_vectorstore(chunks)
    results = _search_chunk(question, vectorstore)
    context = "\n\n".join([r.page_content for r in results])
    answer = _ask_llm(question, context)
    return answer
