🛡️ Proactive Insurance Policy Guardian




Proactive Insurance Policy Guardian is an AI-powered web application that helps users analyze, understand, and query their insurance policy documents in natural language.

✅ Upload your insurance PDF
✅ Ask questions like "What is my deductible?"
✅ Get accurate, plain-English answers
✅ Receive answers via email
✅ View and clear your Q&A history
✅ Use voice input for convenience

📌 Table of Contents
Features

Tech Stack

Setup Guide

How It Works

Deployment

Screenshots

Disclaimer

License

Contact

✨ Features
✅ Upload and process PDF insurance policies
✅ Intelligent semantic search using FAISS embeddings
✅ Contextual answers from the Mistral-7B model
✅ Email delivery of AI responses
✅ Persistent chat history per session
✅ One-click history clearing
✅ Voice input (speech-to-text)
✅ Modern Tailwind CSS UI

⚙️ Tech Stack
Layer	Technology
Backend	Flask, Python
AI Models	SentenceTransformer (all-MiniLM-L6-v2), Mistral 7B Instruct
Vector Search	FAISS
PDF Parsing	PyPDF2
Frontend	HTML, Tailwind CSS, JavaScript
Email	smtplib with Gmail SMTP
Environment	Hugging Face API, dotenv

🛠️ Setup Guide
Follow these steps to get your project running locally.

📥 1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/YOUR_USERNAME/Proactive_Insurance.git
cd Proactive_Insurance
🧰 2. Create and Activate Virtual Environment
Windows:

powershell
Copy
Edit
python -m venv venv
venv\Scripts\activate
macOS/Linux:

bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate
📦 3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
🔑 4. Configure Environment Variables
Create a .env file in the project root:

ini
Copy
Edit
HF_TOKEN=your_huggingface_api_token
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
✅ Important:

Your Gmail must use an App Password.
How to create an app password.

Your Hugging Face token must have Inference API access.

▶️ 5. Run the Application
bash
Copy
Edit
python app.py
Visit:

cpp
Copy
Edit
http://127.0.0.1:3000
🧠 How It Works
Upload PDF: The app extracts all text.

Chunking: Policy text is split into 300-character chunks.

Embedding: Chunks are embedded with SentenceTransformer.

Semantic Search: FAISS finds the most relevant chunk for the question.

Answer Generation: Mistral-7B generates a clear answer.

Extras:

Answer is emailed if requested.

Chat history is saved to session.

Voice input populates the question box.

🌐 Deployment
You can deploy to:

Render.com

Add gunicorn to requirements.txt

Use gunicorn app:app as the start command

Vercel

With Flask serverless adapter

PythonAnywhere

WSGI-based hosting

📸 Screenshots
(Add screenshots of your app interface here)

⚠️ Disclaimer
This project is for educational purposes only.
It provides general information and is not a substitute for professional insurance advice.
Always consult your insurance advisor for specific guidance.



✉️ Contact
Shivam Sharma

LinkedIn:https://www.linkedin.com/in/shivam-sharma-ba2a4823a/ 

Email:shivam3782@gmail.com
