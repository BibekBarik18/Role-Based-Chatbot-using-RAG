from langchain_community.document_loaders import TextLoader
import faiss
from langchain_community.vectorstores import FAISS
from langchain.storage import InMemoryStore
from langchain.schema.document import Document
from langchain_ollama import OllamaEmbeddings
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
import uuid
import pickle
import tempfile

def embed_documents(file_path,role):
    with tempfile.NamedTemporaryFile(delete=False,suffix=".md") as temp_file:
        temp_file.write(file_path.read())
        temp_file_path=temp_file.name

    loader=TextLoader(temp_file_path)
    text_documents=loader.load()
    text_documents

    text_splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks=text_splitter.split_text(text_documents[0].page_content)

    print("text splitted")

    load_dotenv()

    prompt_text="""
    You are an assistant tasked with summarizing tables and text.
        Give a concise summary of the tables and text.
        Respond only with the summary, no additional comment.
        Do not start your message by saying "Here is a summary" or anything like that.
        Correctly interprete the text and tables in the markdown file.
        Chunk: {chunks}
    """
    prompt=ChatPromptTemplate.from_template(prompt_text)
    model=ChatGroq(temperature=0.5,
                groq_api_key=os.getenv("GROQ_API_KEY"),
                model="llama-3.1-8b-instant")
    summarize_chain=prompt|model|StrOutputParser()

    vectorstore=FAISS.from_documents(documents=[Document(page_content="dummy")],
                    embedding=OllamaEmbeddings(model="llama3.2:1b"),
    )

    store=InMemoryStore()
    id_key="doc_id"

    retriever=MultiVectorRetriever(
        vectorstore=vectorstore,
        docstore=store,
        id_key=id_key
    )

    chunks_splitted=[]
    doc_ids=[]
    for chunk in chunks:
        doc_ids.append(str(uuid.uuid4()))
        chunks_splitted.append(Document(page_content=chunk,metadata={id_key:doc_ids[-1],"source":"original"}))
    print("chunks splitted")

    summarized_texts=[]
    for i,chun in enumerate(chunks_splitted):
        summary=summarize_chain.invoke({"chunks": chun})
        summarized_texts.append(Document(page_content=summary,metadata={id_key:doc_ids[i],"source": "summary"}))

    print("chunks summarised")

    retriever.vectorstore.add_documents(summarized_texts)
    retriever.docstore.mset(list(zip(doc_ids,chunks_splitted)))

    vectorstore.save_local(f"data.\{role}_faiss_index")

    with open(f"data.\{role}_docstore_data.pkl", "wb") as f:
        pickle.dump({"doc_ids": doc_ids, "chunks_splitted": chunks_splitted}, f)

    os.remove(temp_file_path)
