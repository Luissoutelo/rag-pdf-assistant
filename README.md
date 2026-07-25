# RAG PDF Assistant

Sistema de perguntas e respostas sobre documentos PDF, usando RAG (Retrieval-Augmented Generation). Permite fazer perguntas em linguagem natural sobre o conteúdo de um PDF e receber respostas geradas por um LLM, com base apenas no contexto relevante encontrado no documento.

## Como funciona

1. **Leitura do PDF** — o documento é lido e convertido em texto
2. **Chunking** — o texto é dividido em pedaços menores, com sobreposição entre eles para preservar contexto
3. **Embeddings** — cada pedaço é transformado em um vetor numérico que representa o seu significado, usando o modelo `all-MiniLM-L6-v2`
4. **Vector Store** — os vetores são armazenados numa base de dados vetorial (Chroma) para pesquisa rápida
5. **Similarity Search** — quando uma pergunta é feita, o sistema encontra os pedaços do documento mais relevantes por similaridade semântica
6. **Geração de resposta** — o contexto encontrado é enviado, junto com a pergunta, ao modelo Gemini, que gera a resposta final

## Stack

- **Python**
- **LangChain** — orquestração do pipeline de RAG
- **FastAPI** — API para servir o sistema via HTTP
- **ChromaDB** — base de dados vetorial
- **Sentence Transformers** — geração de embeddings
- **Google Gemini API** — geração de respostas em linguagem natural

## Como correr

1. Clona o repositório
2. Instala as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Cria um ficheiro `.env` na raiz do projeto com a tua chave da API Gemini:
   ```
   GEMINI_API_KEY=a_tua_chave_aqui
   ```
4. Coloca o teu PDF na pasta do projeto e ajusta o caminho no código
5. Corre o servidor:
   ```bash
   uvicorn main:app --reload
   ```
6. Acede a `http://127.0.0.1:8000/docs` para testar a API interativamente

## Exemplo de uso

```
GET /pergunta?pergunta=quais as fases do pipeline de deals?
```

```json
{
  "resposta": "As fases do pipeline de deals são: Qualificação, Análise de necessidades, Proposta apresentada, Negociação, Fechado Ganho, Fechado Perdido"
}
```

## Notas

Este projeto foi construído em duas etapas: primeiro implementado manualmente (chunking, embeddings e similarity search escritos do zero, sem frameworks), para compreender os fundamentos de um sistema RAG, e depois recriado com LangChain para comparação e produção.