import os
import tempfile

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

from ai_feedback import generate_resume_feedback
from job_matching import compute_similarity, load_job_descriptions
from resume_parser import extract_text_from_pdf, extract_resume_profile

load_dotenv()
app = Flask(__name__)
CORS(app)

JOB_DESCRIPTIONS = load_job_descriptions()


@app.route("/api/jobs", methods=["GET"])
def get_jobs():
    return jsonify(JOB_DESCRIPTIONS)


@app.route("/api/analyze", methods=["POST"])
def analyze_resume():
    if "file" not in request.files:
        return jsonify({"error": "Resume file is required."}), 400

    resume_file = request.files["file"]
    if resume_file.filename == "":
        return jsonify({"error": "Upload a PDF resume file."}), 400

    _, temp_path = tempfile.mkstemp(suffix=".pdf")
    resume_file.save(temp_path)

    try:
        resume_text = extract_text_from_pdf(temp_path)
        profile = extract_resume_profile(resume_text)
        matches = compute_similarity(resume_text, JOB_DESCRIPTIONS)
        feedback = generate_resume_feedback(resume_text, matches[:2])

        return jsonify({
            "profile": profile,
            "matches": matches,
            "feedback": feedback,
        })
    finally:
        try:
            os.remove(temp_path)
        except OSError:
            pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
