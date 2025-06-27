from flask import Flask, render_template, request
import os
import PyPDF2
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from huggingface_hub import InferenceClient

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Load embedding model
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Load LLM
client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    token=os.getenv("HF_TOKEN")
)

# Helper to clean text
def clean_text(text):
    lines = text.splitlines()
    cleaned = []
    for line in lines:
        line = line.strip()
        if line and not line.lower().startswith("section"):
            cleaned.append(line)
    return " ".join(cleaned)

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    retrieved_context = ""
    filename = ""

    if request.method == "POST":
        pdf = request.files.get("pdf")
        question = request.form.get("question")
        filename = request.form.get("filename", "")

        # If uploading a new PDF
        if pdf:
            filename = pdf.filename
            pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            pdf.save(pdf_path)

            # Extract text
            text = ""
            reader = PyPDF2.PdfReader(pdf_path)
            for page in reader.pages:
                text += page.extract_text() or ""

            # Save extracted text
            text_path = os.path.join(app.config["UPLOAD_FOLDER"], f"{filename}.txt")
            with open(text_path, "w", encoding="utf-8") as f:
                f.write(text)

        # Only proceed if there's a question
        if filename and question:
            # Load saved text
            text_path = os.path.join(app.config["UPLOAD_FOLDER"], f"{filename}.txt")
            with open(text_path, "r", encoding="utf-8") as f:
                text = f.read()

            # Split into chunks
            chunk_size = 300
            chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

            # Embed chunks
            embeddings = embed_model.encode(chunks).astype("float32")
            index = faiss.IndexFlatL2(embeddings.shape[1])
            index.add(embeddings)

            # Embed question
            q_embedding = embed_model.encode([question]).astype("float32")
            _, I = index.search(q_embedding, k=1)
            retrieved_chunks = [chunks[i] for i in I[0]]

            retrieved_context = " ".join([clean_text(chunk) for chunk in retrieved_chunks])

            # Prompt for LLM
            prompt_content = (
                "Based only on the policy text below, answer the user's question. "
                "If the answer is not specified, reply exactly: 'Not specified in the policy.'\n\n"
                f"<<<POLICY>>>\n{retrieved_context}\n<<<END_POLICY>>>\n\n"
                f"Question: {question}\n\n"
                "Answer in clear, short plain English:"
            )

            messages = [
                {"role": "system", "content": "You are a helpful insurance policy expert."},
                {"role": "user", "content": prompt_content}
            ]

            # Get response
            response = client.chat_completion(
                messages,
                max_tokens=150,
                temperature=0.0
            )
            answer = response.choices[0].message.content.strip()

        elif not pdf and not question:
            answer = "Please upload a PDF and/or provide a question."

    return render_template(
        "index.html",
        answer=answer,
        retrieved_context=retrieved_context,
        filename=filename
    )

if __name__ == "__main__":
    app.run(debug=True, port=3000)
