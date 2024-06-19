from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_experimental.chat_models import Llama2Chat
from langchain_community.llms import LlamaCpp
from langchain.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

CHROMA_PATH = "chroma"
load_dotenv()
USE_OPENAI = os.getenv("USE_OPENAI", "False") == "True"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def call_chatbot(query_text):
    if USE_OPENAI:
        model = ChatOpenAI(openai_api_key=OPENAI_API_KEY)
        embedding_function = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    else:
        model_path = "llama.cpp/models/llama-2-7b-chat.Q4_K_M.gguf"
        llm = LlamaCpp(model_path=model_path, streaming=False, n_ctx=4096)
        model = Llama2Chat(llm=llm)
        embedding_function = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    results = db.similarity_search_with_relevance_scores(query_text, k=7)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template("""
    Answer the question based only on the following context:

    {context}

    ---

    Answer the question based only on the above context and nothing else: {question}
    """)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)

    response_text = model.predict(prompt)
    print(response_text)
    return response_text
