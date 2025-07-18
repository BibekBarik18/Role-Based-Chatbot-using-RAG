## 🧠 Role-Based Chatbot using RAG

This project implements a **role-aware, retrieval-augmented chatbot** that leverages multi-vector document retrieval and local LLM inference to provide **customized answers** based on a user’s role (e.g., Student, Admin, Faculty). It enables secure, scalable, and contextually precise interactions with large internal knowledge bases.

---

## 📂 How it Works

Users can upload **role-specific documentation** (in Markdown format), which is then:

1. 🔹 **Split into context-rich chunks** using a recursive character splitter
2. 🔹 **Summarized** using **Groq’s LLaMA-3.1 8B** model
3. 🔹 **Embedded** using **Ollama’s LLaMA-3.2 1B** model
4. 🔹 **Summaries Stored in a FAISS vector database** for fast and accurate semantic retrieval
5. 🔹 **Original documents Stored in pickel storage** along with the document ids for fast and accurate semantic retrieval

Each document is tagged with role metadata, enabling scoped retrieval based on the user’s current role.

---

## 🔍 What Sets This Chatbot Apart?

### 🎯 Role-Specific Knowledge Grounding

Each user role is associated with a unique subset of the documentation. Queries are dynamically filtered and contextualized, ensuring responses are generated only from relevant documents — simulating real-world access control.

### ⚡ Multi-Vector Retrieval

The chatbot stores **summarized chunks** in the vector database and the **original documents** in pickel storage. This **dual representation** enhances semantic matching by capturing multiple levels of abstraction — improving relevance, especially for nuanced or ambiguous queries.

### 💾 FAISS Vector Store

Utilizes **FAISS** for high-performance similarity search. Scales well with large corpora and ensures **low-latency** retrieval, making it suitable for real-time chat interfaces.

### 🔁 Reusability

Previously embedded role-based knowledge bases are cached and reusable. This drastically reduces compute cost and allows quick onboarding for new users or roles.

---

## 🛠️ Tech Stack

* **Python 3.10+**
* **LLM Inference**: Groq (LLaMA-3.1 8B) + Ollama (LLaMA-3.2 1B)
* **Embedding**: Sentence-Transformers / Ollama
* **Vector Store**: FAISS
* **UI**: Streamlit
* **Retrieval**: Chunked + Multi-vector with role metadata filtering
* **Langchain**: for implementing the rag pipeline
---

## 🚀 Key Features

* 🔐 **Access Control**: Scoped knowledge retrieval based on user role
* 🧩 **Modular Pipeline**: Ingestion, embedding, retrieval, and synthesis are independently configurable
* 📡 **Local & Offline Ready**: Supports fully local deployment with CPU/GPU inference

---

## ✅ Why This Matters

* 🏢 Perfect for **internal enterprise bots**, **technical onboarding assistants**, or **domain-specific support agents**
* 🧠 Enables **dynamic access** to knowledge traditionally locked in static documentation
* 🔄 Supports **low-cost, reusable, and private deployments** for secure organizations
* 📈 Bridges the gap between **search** and **conversation**

---

## 📎 Demo & Setup

```bash
# Step 1: Index your role-specific docs
python chatbot/memory_builder.py --chunk-size 1000 --chunk-overlap 50

# Step 2: Run the chatbot with your model of choice
streamlit run chatbot/rag_chatbot_app.py -- \
  --model llama-3.1 \
  --synthesis-strategy async-tree-summarization \
  --k 4
```

---

