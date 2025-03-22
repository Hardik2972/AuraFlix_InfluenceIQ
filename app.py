# from flask import Flask, jsonify, request
# import requests

# app = Flask(__name__)  # Initialize Flask app

# API_KEY = "Tpf2K8lfpgxMrJH2_hAHvg"  # Your API key
# PROXYCURL_URL = "https://nubela.co/proxycurl/api/v2/linkedin"

# @app.route('/get-profile', methods=['GET'])
# def get_profile():
#     linkedin_url = request.args.get("url")  # Get LinkedIn URL from query params
    
#     if not linkedin_url:
#         return jsonify({"error": "Missing LinkedIn profile URL"}), 400

#     headers = {
#         "Authorization": f"Bearer {API_KEY}"
#     }
#     params = {
#         "url": linkedin_url,
#         "fallback_to_cache": "on-error",
#         "use_cache": "if-present"
#     }

#     response = requests.get(PROXYCURL_URL, headers=headers, params=params)

#     if response.status_code == 200:
#         return jsonify(response.json())  # Return profile data as JSON
#     else:
#         return jsonify({"error": response.text, "status_code": response.status_code}), response.status_code

# if __name__ == '__main__':
#     app.run(debug=True)  # Start the Flask app


from flask import Flask, jsonify, request
import requests
from certification_scoring import compute_total_certification_score  # Import scoring function

app = Flask(__name__)  # Initialize Flask app

API_KEY = "qGBOlbHyuN1mrK8-lMfM8Q"  # Your API key
PROXYCURL_URL = "https://nubela.co/proxycurl/api/v2/linkedin"

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
    
    # Compute certification score
    total_certification_score = compute_total_certification_score(profile_data)

    return jsonify({"certification_score": total_certification_score})

if __name__ == '__main__':
    app.run(debug=True)  # Start the Flask app
