import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
import pickle
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain.storage import InMemoryStore
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

if 'role_type' in st.session_state:
    role_type = st.session_state.role_type
    st.title(f"Ask questions about {role_type} role")
    if 'messages' not in st.session_state:
        st.session_state.messages=[]
    for message in st.session_state.messages:
        st.chat_message(message["role"]).markdown(message["content"])
    input = st.chat_input("Enter your question here")
    if input:
        st.chat_message("user").markdown(input)
        st.session_state.messages.append({"role":"user","content":input})
        # response=llm(prompt)
        vectorstore = FAISS.load_local(
        f"./data/{role_type}_faiss_index",
        OllamaEmbeddings(model="llama3.2:1b"),
        allow_dangerous_deserialization=True
        )

        with open(f"./data/{role_type}_docstore_data.pkl", "rb") as f:
            data = pickle.load(f)

        retriever = MultiVectorRetriever(
            vectorstore=vectorstore,
            docstore=InMemoryStore(),  # Or use persistent storage
            id_key="doc_id"
        )

        retriever.docstore.mset(list(zip(data["doc_ids"], data["chunks_splitted"])))

        results = retriever.get_relevant_documents(input)
        context = "\n\n".join([doc.page_content for doc in results])
        prompt_text="""
        Answer the following question based only on the provided context.
think step by step before providing a detailed answer.
provide a detailed answer.
Do not provide any extra message or comment except the reply.
Correctly interpret the text and tables in the markdown file.
Context: {context}
Question: {prompt}
        """
        prompt=ChatPromptTemplate.from_template(prompt_text)
        model=ChatGroq(temperature=0.5,
                    groq_api_key=os.getenv("GROQ_API_KEY"),
                    model="llama-3.1-8b-instant")
        chain=prompt|model|StrOutputParser()
        response=chain.invoke({"context":context,"prompt":input})
        st.chat_message('assistant').markdown(response)
        st.session_state.messages.append({"role":"assistant","content":response})