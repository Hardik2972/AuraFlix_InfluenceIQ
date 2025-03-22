from flask import Flask, jsonify, request
import requests
import torch
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
from certification_scoring import compute_total_certification_score  # Import scoring function

app = Flask(__name__)  # Initialize Flask app

API_KEY = "qGBOlbHyuN1mrK8-lMfM8Q"  # Your API key
PROXYCURL_URL = "https://nubela.co/proxycurl/api/v2/linkedin"

# Check if CUDA is available
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load Models on CUDA
similarity_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device=device)
classifier = pipeline("text-classification", model="distilbert-base-uncased", device=0 if device == "cuda" else -1)

@app.route('/get-score', methods=['GET'])
def get_certification_score():
    linkedin_url = request.args.get("url")  # Get LinkedIn URL from query params
    
    if not linkedin_url:
        return jsonify({"error": "Missing LinkedIn profile URL"}), 400

    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    params = {
        "url": linkedin_url,
        "fallback_to_cache": "on-error",
        "use_cache": "if-present"
    }

    response = requests.get(PROXYCURL_URL, headers=headers, params=params)

    if response.status_code != 200:
        return jsonify({"error": response.text, "status_code": response.status_code}), response.status_code
    
    profile_data = response.json()

    print(profile_data["education"])  # Debugging: Print education data
    print(profile_data["projects"])  # Debugging: Print project data
    
    # Compute certification score
    total_certification_score = compute_total_certification_score(profile_data)

    return jsonify({"certification_score": total_certification_score})

if __name__ == '__main__':
    app.run(debug=True)  # Start the Flask app
