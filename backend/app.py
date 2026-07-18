from flask import Flask, render_template, request, jsonify
from backend.audio import extract_audio, PROCESSING_STATUS
from backend.chat import ask_question
import os

app = Flask(__name__)

# ==========================================
# Persistent Cloud Storage Paths
# ==========================================
UPLOAD_FOLDER = "/data/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        files = request.files.getlist("videos")
        for file in files:
            if file.filename != "":
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                file.save(filepath)
                
                # Triggers background threading workflow instantly
                extract_audio(filepath)

        return render_template("chat.html", status_message="Your video is being processed using Whisper large-v2 in the background. It will be searchable in a few minutes!")

    return render_template("upload.html")

@app.route("/status")
def status():
    return jsonify(PROCESSING_STATUS)

@app.route("/chat", methods=["POST"])
def chat():
    question = request.form["question"]
    result = ask_question(question)
    return render_template(
        "chat.html",
        question=result["question"],
        answer=result["answer"],
        error=result["error"],
        lecture=result["lecture"],
        start=result["start"],
        end=result["end"],
        text=result["text"]
    )

if __name__ == "__main__":
    # Standard fallback configuration block for fallback debugging execution 
    app.run(debug=False)