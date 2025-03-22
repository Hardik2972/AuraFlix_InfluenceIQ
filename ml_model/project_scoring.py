import requests
import math
from sentence_transformers import SentenceTransformer, util
from datetime import datetime
import re

# Function to calculate semantic similarity
def calculate_similarity(text1, text2, similarity_model, device):
    if not text1 or not text2:
        return 0  # Handle empty text case
    embedding1 = similarity_model.encode(text1, convert_to_tensor=True).to(device)
    embedding2 = similarity_model.encode(text2, convert_to_tensor=True).to(device)
    return util.pytorch_cos_sim(embedding1, embedding2).item() + 0.1

# Function to classify project descriptions
def classify_description(text, classifier):
    if not text:
        return "neutral", 0  # Default label and score for empty input
    result = classifier(text)[0]
    return result['label'], result['score'] + 0.2

# Function to validate GitHub repository links and extract an activity score
def check_github_repo(repo_url):
    match = re.search(r"github\.com/([^/]+)/([^/]+)", repo_url or "")
    if not match:
        return 0  # Invalid or missing link
    
    owner, repo = match.groups()
    url = f"https://api.github.com/repos/{owner}/{repo}"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            activity_score = math.log(1 + sum(data.get(k, 0) for k in ['watchers_count', 'stargazers_count', 'forks_count']), 10)
            return round(activity_score, 2)
    except requests.exceptions.RequestException:
        pass  # Ignore network errors
    
    return 0  # Default score if API call fails

# Function to compute credibility score for a single project
def compute_project_score(project, user_skills, classifier, similarity_model, device):
    description = project.get('description', "").strip()
    # year = project.get('year', datetime.now().year)
    
    relevance = calculate_similarity(description, user_skills, similarity_model, device)
    _, technical_score = classify_description(description, classifier)
    # external_validation = check_github_repo(project.get('link'))
    # recency = max(1 - (datetime.now().year - year) * 0.1, 0)  # Decay over years
    
    # Weighted Score Calculation
    final_score = (
        0.5 * relevance +       # Increased importance of relevance
        0.5 * technical_score  # + Technical classification score
        # 0.15 * (external_validation / 2) +  # Normalized GitHub activity
        # 0.2 * recency          # Minimal decay effect
    ) * 100  # Scale to 0-100
    
    return round(final_score, 2)

# Function to combine multiple project scores
def combine_project_scores(projects, user_skills, classifier, similarity_model, device):
    total_weighted_score = 0
    total_weight = 0

    for project in projects:
        if not project.get('description'):
            continue

        score = compute_project_score(project, user_skills, classifier, similarity_model, device)
        
        # Weight based on GitHub activity and recency
        # github_weight = check_github_repo(project.get('link'))
        recency_weight = max(1 - (datetime.now().year - project.get('year', datetime.now().year)) * 0.1, 0)
        
        weight = recency_weight  # Total weight
        total_weighted_score += score * (weight if weight > 0 else 1)  # Prevent zero weight multiplication
        total_weight += (weight if weight > 0 else 1)

    # Avoid division by zero
    return min(round(total_weighted_score / total_weight, 2) if total_weight > 0 else 0, 100)