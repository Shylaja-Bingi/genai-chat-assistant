GenAI Chat Assistant using RAG

Project Overview

This project is a **GenAI Chat Assistant** built using a **Retrieval Augmented Generation (RAG)** architecture.
It answers user questions using information retrieved from a set of documents.

The system uses embeddings and similarity search to retrieve the most relevant document context and then generates a response using a language model.

---

Architecture Diagram

User Question
↓
Frontend (HTML / JS Chat UI)
↓
Flask Backend API
↓
Embedding Model (Sentence Transformers)
↓
Vector Similarity Search
↓
Retrieve Relevant Context
↓
Prompt Construction
↓
Language Model generates Answer
↓
Response returned to User

RAG Workflow Explanation

1. User enters a query in the chatbot interface.
2. The query is sent to the Flask backend API.
3. The system converts the query into embeddings using a sentence transformer model.
4. The embeddings are compared with stored document embeddings.
5. The most relevant document context is retrieved using similarity search.
6. The retrieved context is combined with the user question to form a prompt.
7. The language model generates an answer based only on the provided context.
8. The response is returned to the chatbot interface.

---

Embedding Strategy

This project uses the model:

sentence-transformers/all-MiniLM-L6-v2

This model converts text into vector embeddings.
These embeddings allow semantic similarity comparison between the user query and stored documents.

---

Similarity Search

Cosine similarity is used to compare the query embedding with document embeddings.

The system retrieves the document chunk with the highest similarity score and uses it as context for the language model.

---

Prompt Design

The prompt is designed to ensure the model answers **only from the retrieved context**.

Example prompt format:

Context: <retrieved document text>

Question: <user question>

Instruction:
Answer the question based only on the context.
If the answer is not present, say: "I don't have enough information."

This helps prevent hallucinations.

---

Setup Instructions

1 Install dependencies

pip install -r requirements.txt

2 Run the application

python app.py

3 Open in browser

http://127.0.0.1:5000

---

Technologies Used

* Python
* Flask
* Sentence Transformers
* Transformers
* Scikit-learn
* HTML / CSS / JavaScript

---
