from flask import Flask, jsonify, request
import requests
import torch
import math
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
from certification_scoring import compute_total_certification_score  # Import scoring function
from education_scoring import combined_education_score  # Import scoring function
from project_scoring import combine_project_scores  # Import scoring function

app = Flask(__name__)  # Initialize Flask app

API_KEY = "MmJFtKyE0dq4GYSvcHKXJA"  # Your API key
PROXYCURL_URL = "https://nubela.co/proxycurl/api/v2/linkedin"

# Check if CUDA is available
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load Models on CUDA
similarity_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device=device)
classifier = pipeline("text-classification", model="distilbert-base-uncased", device=0 if device == "cuda" else -1)

def scale_connection_count_exponential(connection_count, lambda_value=0.005, max_value=100):
    return round(1 + (max_value - 1) * (1 - math.exp(-lambda_value * connection_count)), 2)

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

    print(profile_data)
    
    # Compute certification score
    total_certification_score = compute_total_certification_score(profile_data)

    # Compute education score
    total_education_score = combined_education_score(profile_data.get("education"))

    # Compute project score
    total_project_score = combine_project_scores(profile_data.get("accomplishment_projects"), profile_data.get("skills"), classifier, similarity_model, device)

    # Compute social score
    total_social_score = (
        (50 if profile_data.get("country_full_name") not in [None, ""] else 25) +
        (50 if any(profile_data.get(key) not in [None, "", []] for key in ["personal_emails", "personal_numbers"]) else 25)
    )
 
    return jsonify({"certification_score": total_certification_score, "education_score": total_education_score, "project_score": total_project_score, "popularity": scale_connection_count_exponential(profile_data.get("connections", 0)), "social_score": total_social_score})

if __name__ == '__main__':
    app.run(debug=False)  # Start the Flask app
