from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import LlamaCpp
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter

from langchain import hub
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
model_path = "llama.cpp/models/llama-2-7b-chat.Q2_K.gguf"
llm = LlamaCpp(model_path=model_path, streaming=False)

pdf_path = "Llama2.pdf"
loader = PyPDFLoader(pdf_path)
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
embeddings = HuggingFaceEmbeddings()

vector_store = FAISS.from_documents(docs, embeddings)
retriever = vector_store.as_retriever()
# qa_chain = create_retrieval_chain(llm=llm, retriever=vector_store.as_retriever())
# qa_chain = create_retrieval_chain(llm, vector_store)
combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful AI talking to human"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)


def get_response(query):
    return retrieval_chain.invoke(input=query)


print(get_response("What is the capital of France?"))
