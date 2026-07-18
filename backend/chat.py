import os
import joblib
import numpy as np

from dotenv import load_dotenv
from google import genai
from sklearn.metrics.pairwise import cosine_similarity

# =====================================================
# Paths & Environment Setup
# =====================================================
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY is None:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Local storage path tracking for VS Code
EMBEDDING_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "embeddings.joblib")

# =====================================================
# Gemini Client Initialization (No local models loaded!)
# =====================================================
client = genai.Client(api_key=GEMINI_API_KEY)
print("Gemini Client Initialized Successfully!")

# =====================================================
# Create Embedding Function Using Gemini Cloud API
# =====================================================
def create_embedding(text_list):
    # Calls Gemini's embedding model over the air (0 MB local RAM used)
    response = client.models.embed_content(
        model="text-embedding-004",
        contents=text_list
    )
    # Extract the vector arrays
    embeddings = [e.values for e in response.embeddings]
    return np.array(embeddings)

# =====================================================
# Ask Question
# =====================================================
def ask_question(question):    
    print("\nUser Question :", question)

    if not os.path.exists(EMBEDDING_FILE):
        return {
            "question": question,
            "answer": "No lectures have been processed yet. Please upload a video first.",
            "error": "Database file not found.",
            "lecture": "N/A", "start": 0, "end": 0, "text": ""
        }

    df = joblib.load(EMBEDDING_FILE)

    if df.empty:
        return {
            "question": question,
            "answer": "The database is currently empty. Please upload a video.",
            "error": "Empty dataframe.",
            "lecture": "N/A", "start": 0, "end": 0, "text": ""
        }

    # Create Query Embedding via Gemini
    question_embedding = create_embedding([question])[0]

    # Compute Cosine Similarity
    all_embeddings = np.vstack(df["embedding"].values)
    similarities = cosine_similarity(
        all_embeddings,
        question_embedding.reshape(1, -1)
    ).flatten()

    # Retrieve Top 5 Chunks
    top_results = min(5, len(df))
    max_index = similarities.argsort()[::-1][:top_results]
    new_df = df.iloc[max_index]

    top_match = new_df.iloc[0]

    # Build Context Prompt
    context = ""
    for _, item in new_df.iterrows():
        context += (
            f"Lecture Number : {item['number']}\n"
            f"Lecture Title : {item['title']}\n"
            f"Start Time : {item['start']}\n"
            f"End Time : {item['end']}\n"
            f"Transcript : {item['text']}\n\n"
        )

    prompt = f"""
You are an AI Teaching Assistant.
Use ONLY the lecture context below to answer the user's question.

Lecture Context:
{context}

Student Question:
{question}
""".strip()

    error = None
    answer = None

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        answer = response.text if response.text else "Gemini returned an empty response."
    except Exception as e:
        print("\nGemini Error:", e)
        error = "Sorry, I am temporarily unavailable."

    return {
        "question": question,
        "answer": answer,
        "error": error,
        "lecture": f"Lecture {top_match['number']}: {top_match['title']}",
        "start": top_match["start"],
        "end": top_match["end"],
        "text": top_match["text"]
    }