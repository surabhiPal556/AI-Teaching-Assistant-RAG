# 🤖 RAG Based AI Teaching Assistant

An AI-powered Teaching Assistant built using Retrieval-Augmented Generation (RAG). The system extracts knowledge from educational video lectures, converts speech to text, creates semantic embeddings, retrieves the most relevant content, and generates accurate answers using Google's Gemini API.

## 🚀 Features

- Upload educational videos
- Extract audio from videos using FFmpeg
- Convert speech to text using Whisper Large-v2
- Generate embeddings using BGE-M3
- Store embeddings for faster retrieval
- Retrieve relevant lecture content using Cosine Similarity
- Generate intelligent answers using Google Gemini API
- Simple and responsive web interface built with HTML and CSS

---

## 🛠️ Frontend Technologies Used

- HTML5
- CSS3
- Flask (Frontend Integration)

---

## ⚙️ Backend Technologies Used

- Python
- Flask
- FFmpeg (Audio Extraction)
- Whisper Large-v2 (Speech-to-Text)
- BGE-M3 (Embedding Model)
- Cosine Similarity (Semantic Retrieval)
- Google Gemini API (Answer Generation)
- Joblib (Embedding Storage)

---

## 📂 Project Workflow

1. Upload a lecture video.
2. Extract audio using FFmpeg.
3. Convert speech into text using Whisper Large-v2.
4. Split the transcript into smaller chunks.
5. Generate embeddings using the BGE-M3 model.
6. Store embeddings using Joblib.
7. Retrieve the most relevant chunks using Cosine Similarity.
8. Send the retrieved context to Google Gemini API.
9. Display an accurate answer to the user.

---

## 📁 Project Structure

```
AI-Teaching-Assistant-RAG/
│
├── backend/
│   ├── app.py
│   ├── templates/
│   ├── static/
│   ├── uploads/
│   ├── transcripts/
│   ├── embeddings/
│   └── ...
│
├── README.md
└── requirements.txt
```

---

## ▶️ How to Run

1. Clone the repository

```bash
git clone https://github.com/your-username/AI-Teaching-Assistant-RAG.git
```

2. Navigate to the project directory

```bash
cd AI-Teaching-Assistant-RAG
```

3. Install the required dependencies

```bash
pip install -r requirements.txt
```

4. Add your Google Gemini API key.

5. Run the Flask application

```bash
python app.py
```

6. Open your browser and visit

```
http://127.0.0.1:5000
```

---

## 🎯 Future Enhancements

- PDF and document support
- Multi-language question answering
- Voice-based queries
- User authentication
- Chat history
- Cloud deployment

---

## 👩‍💻 Author

**Surabhi Pal**

---

## 📜 License

This project is developed for educational and learning purposes.
