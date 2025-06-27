from flask import Flask, render_template, request
import os
import PyPDF2
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from huggingface_hub import InferenceClient

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load models
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
client = InferenceClient(
    model="HuggingFaceH4/zephyr-7b-beta",
    token=os.getenv("HF_TOKEN")
)

@app.route('/', methods=['GET', 'POST'])
def index():
    answer = ""

    if request.method == 'POST':
        pdf = request.files.get('pdf')
        question = request.form.get('question')

        if not pdf or not question:
            answer = "Please provide a PDF and a question."
            return render_template("index.html", answer=answer)

        # Save and extract PDF
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf.filename)
        pdf.save(pdf_path)

        text = ""
        reader = PyPDF2.PdfReader(pdf_path)
        for page in reader.pages:
            text += page.extract_text() or ""

        # Split into chunks
        chunk_size = 300
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

        # Embed and index chunks
        embeddings = embed_model.encode(chunks).astype("float32")
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)

        # Embed question and retrieve top 2 chunks
        q_embedding = embed_model.encode([question]).astype("float32")
        D, I = index.search(q_embedding, k=2)
        retrieved_chunks = [chunks[i] for i in I[0]]

        # Prepare prompt
        context = "\n\n".join(retrieved_chunks)
        messages = [
            {"role": "system", "content": "You are an insurance policy expert. Answer questions based only on the context below. If unsure, say 'Not specified in the policy.'"},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer in plain English:"}
        ]

        # Get response
        response = client.chat_completion(
            messages,
            max_tokens=300,
            temperature=0.3
        )
        answer = response.choices[0].message.content.strip()

    return render_template("index.html", answer=answer)

if __name__ == '__main__':
    app.run(debug=True, port=3000)
