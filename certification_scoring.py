import requests
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the SentenceTransformer model
device = "cuda" if torch.cuda.is_available() else "cpu"
similarity_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device=device)

# Example Trusted Certification Issuers (Assign higher credibility)
TRUSTED_ISSUERS = {
    "Google": 5,
    "AWS": 5,
    "Microsoft": 5,
    "Coursera": 4,
    "Udemy": 3,
    "LinkedIn Learning": 3
}

def get_issuer_score(issuer):
    """Assign credibility score based on certification authority."""
    return TRUSTED_ISSUERS.get(issuer, 2)  # Default score is 2 for unknown issuers

def get_certification_level_score(cert_name):
    """Assign scores based on certification level (Beginner to Expert)."""
    cert_name = cert_name.lower()
    if "expert" in cert_name or "professional" in cert_name:
        return 5
    elif "associate" in cert_name or "specialist" in cert_name:
        return 4
    elif "fundamentals" in cert_name or "beginner" in cert_name:
        return 3
    return 2  # Default score for unknown level

def get_duration_score(duration_months):
    """Score based on course duration (longer = higher score)."""
    if duration_months >= 6:
        return 5
    elif duration_months >= 3:
        return 4
    elif duration_months >= 1:
        return 3
    return 2  # Short duration = lower score
    
def verify_certification(cert_url):
    """Check if certification URL is valid through verification API."""
    try:
        response = requests.head(cert_url, timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

POPULAR_CERTIFICATIONS = {
    "AWS Certified Solutions Architect": 5,
    "Google Professional Data Engineer": 5,
    "Microsoft Azure Solutions Architect": 4,
    "Certified Ethical Hacker (CEH)": 4,
    "Coursera Deep Learning Specialization": 3
}

def get_popularity_score(cert_name):
    """Assign a score based on certification popularity."""
    return POPULAR_CERTIFICATIONS.get(cert_name, 2)  # Default score if not found

def normalize_score(score, min_score=0, max_score=50):  # Adjust max_score based on realistic upper bound
    """Normalize a given score to a 1-10 scale."""
    if score < min_score:
        return 1
    if score > max_score:
        return 10
    return 1 + 9 * (score - min_score) / (max_score - min_score)

def extract_text_data(profile):
    """Extracts summary, headline, experience as a single text block."""
    professional_text = ""
    if "summary" in profile and profile["summary"]:
        professional_text += profile["summary"] + " "
    if "headline" in profile and profile["headline"]:
        professional_text += profile["headline"] + " "
    if "experience" in profile and isinstance(profile["experience"], list):
        for exp in profile["experience"]:
            professional_text += exp.get("company", "") + " " + exp.get("title", "") + " "

    return professional_text.strip()

def compute_similarity(text1, text2):
    """Computes similarity using SentenceTransformer embeddings."""
    if not text1 or not text2:
        return 0.0  # Return 0 if either text is empty
    
    # Generate embeddings
    embeddings = similarity_model.encode([text1, text2], convert_to_tensor=True)

    # Compute cosine similarity
    similarity_score = torch.nn.functional.cosine_similarity(embeddings[0], embeddings[1], dim=0).item()

    # Scale relevance weight between 0.5 and 1.5
    weight = 0.5 + similarity_score
    return min(weight, 1.5)  # Cap at 1.5

def compute_certification_credibility(cert):
    """Compute a robust credibility score for a certification."""
    credibility_score = 1  # Base score

    # License number check
    if cert.get("license_number"):
        credibility_score += 1

    # URL Verification
    if verify_certification(cert.get("url", "")):
        credibility_score += 2

    # Issuing Authority Score
    credibility_score += get_issuer_score(cert.get("authority", ""))

    # Certification Level Score
    credibility_score += get_certification_level_score(cert.get("name", ""))

    # Popularity Score
    credibility_score += get_popularity_score(cert.get("name", ""))

    # Duration Score (if available)
    if "duration_months" in cert:
        credibility_score += get_duration_score(cert["duration_months"])

    return min(credibility_score, 10)  # Cap at 10 for fairness

def compute_total_certification_score(profile):
    """Calculates the total certification score based on relevance and credibility."""
    professional_text = extract_text_data(profile)
    certifications = profile.get("certifications", [])
    total_score = 0.0

    for cert in certifications:
        cert_text = cert.get("name", "") + " " + cert.get("authority", "")
        relevance_weight = compute_similarity(professional_text, cert_text)
        credibility = compute_certification_credibility(cert)
        total_score += relevance_weight * credibility

    return normalize_score(total_score)
