import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import re
from fuzzywuzzy import process

file_path = "qs-excel.xlsx"  # Replace with your actual file path
df = pd.read_excel(file_path, header=None, usecols=[0, 3, 28])

df[28] = df[28].apply(lambda x: 20 if str(x).strip().upper() == '-' else x)

df[3] = df[3].astype(str).str.lower().apply(lambda x: re.sub(r'[^a-z0-9]', '', x))

institute_scores = dict(zip(df[3], df[28]))

# 📌 Degree Score Mapping (Predefined)
degree_scores = {
    "phd": 40, "doctorate": 40, "doctorofphilosophy": 40,
    "master": 30, "masters": 30, "mtech": 30, "msc": 30, "ms": 30, "mba": 30,  
    "ma": 30, "mcom": 30, "mca": 30, "mphil": 30, "med": 30, "meng": 30, "mcs": 30,
    "bachelor": 20, "bachelors": 20, "btech": 20, "bacheloroftechnology": 20,  
    "bsc": 20, "bachelorofscience": 20, "be": 20, "bachelorofengineering": 20,  
    "ba": 20, "bachelorofarts": 20, "bcom": 20, "bachelorofcommerce": 20,  
    "bba": 20, "bachelorofbusinessadministration": 20, "bbs": 20, "bhm": 20,
    "diploma": 10, "associatedegree": 10, "pgd": 10, "postgraduatediploma": 10,
    "hnd": 10, "highernationaldiploma": 10
}

# 🔹 Helper function to clean text (remove spaces & special characters)
def clean_text(text):
    return re.sub(r'[^a-z0-9]', '', text.lower().strip()) if text else ""

# 🔹 Get Degree Score using Exact, Token & Fuzzy Matching
def get_degree_score(degree_name):
    cleaned_degree = clean_text(degree_name)

    # ✅ 1. Exact Matching
    if cleaned_degree in degree_scores:
        return degree_scores[cleaned_degree]

    # ✅ 2. Token-Based Matching (for different word orders)
    tokens = set(cleaned_degree.split())
    for key in degree_scores.keys():
        if set(key.split()).intersection(tokens):
            return degree_scores[key]

    # ✅ 3. Fuzzy Matching (handling typos & variations)
    best_match, score = process.extractOne(cleaned_degree, degree_scores.keys())
    return degree_scores[best_match] if score > 80 else 0  # 80% similarity threshold

# 📌 Education Score Calculation Function
def calculate_education_score(education_data):
    # 🔹 Extract & clean institute name
    institute_name = clean_text(education_data.get("school", ""))
   
    # 🔹 Get Institute Score (Default = 10, then scale to 40)
    institute_score = institute_scores.get(institute_name, 20)
    institute_score = (institute_score / 100) * 40  # Scale from 100 to 40

    # 🔹 Get Degree Score
    degree_name = education_data.get("degree_name", "")
    degree_score = get_degree_score(degree_name)

    # 🔹 GPA Score (assuming a 10-point scale, scale to 20 points)
    gpa = education_data.get("grade")
    gpa_score = (gpa / 10) * 20 if isinstance(gpa, (int, float)) and 0 <= gpa <= 10 else 0

    # 🔹 Final Score Calculation
    final_score = institute_score + degree_score + gpa_score
    return min(final_score, 100)  # Ensure score does not exceed 100

def combined_education_score(education_data):
    best_score = 0
    for edu in education_data:
        best_score = max(best_score, calculate_education_score(edu))

    return round(best_score, 2)