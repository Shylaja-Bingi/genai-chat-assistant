from sentence_transformers import SentenceTransformer
from flask import Flask, request, jsonify, render_template
import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from transformers import pipeline

model = SentenceTransformer("all-MiniLM-L6-v2")

llm = pipeline("text-generation", model="gpt2")
def chunk_document(text, chunk_size=200):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)

    return chunks

chunk_embeddings = []

def find_similar_chunks(user_query):

    query_embedding = generate_embedding(user_query)

    embeddings = [chunk["embedding"] for chunk in chunk_embeddings]

    similarities = cosine_similarity([query_embedding], embeddings)[0]

    top_indices = np.argsort(similarities)[-3:][::-1]

    results = []

    for i in top_indices:
        # Only keep chunks with reasonable similarity
        if similarities[i] > 0.4:
            results.append(chunk_embeddings[i])

    return results

def get_llm_response(context, user_message):

    # Just return the most relevant context
    sentences = context.split(".")
    answer = ".".join(sentences[:2]).strip()

    return answer + "."
    
def generate_embedding(text):
    embedding = model.encode(text)
    return embedding


app = Flask(__name__)

# Load documents
with open("docs.json", "r") as f:
    documents = json.load(f)

    all_chunks = []

# First create chunks
for doc in documents:
    chunks = chunk_document(doc["content"])

    for chunk in chunks:
        all_chunks.append({
            "title": doc["title"],
            "content": chunk
        })

# Then generate embeddings
for chunk in all_chunks:
    embedding = generate_embedding(chunk["content"])

    chunk_embeddings.append({
        "title": chunk["title"],
        "content": chunk["content"],
        "embedding": embedding
    })

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():

    data = request.json
    user_message = data.get("message")

    # Step 1: Find relevant chunks
    relevant_chunks = find_similar_chunks(user_message)

    # If nothing relevant found
    if not relevant_chunks:
        return jsonify({
            "reply": "I don't have enough information from the documents.",
            "retrievedChunks": 0
        })

    # Step 2: Build context
    context = "\n".join([chunk["content"] for chunk in relevant_chunks])

    # Step 3: Generate response
    reply = get_llm_response(context, user_message)

    return jsonify({
        "reply": reply,
        "retrievedChunks": len(relevant_chunks)
    })


if __name__ == "__main__":
    app.run(debug=True)