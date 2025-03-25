from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Retrieve keys from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

# Your Google Custom Search API URL
GOOGLE_SEARCH_URL = "https://www.googleapis.com/customsearch/v1"

@app.route('/search', methods=['GET'])
def search_images():
    query = request.args.get('query')
    
    if not query:
        return jsonify({"error": "Missing search query"}), 400

    params = {
        "q": query,
        "cx": SEARCH_ENGINE_ID,
        "key": GOOGLE_API_KEY,
        "searchType": "image",
        "num": 10  # Fetch 10 results
    }

    try:
        response = requests.get(GOOGLE_SEARCH_URL, params=params)
        data = response.json()
        
        results = []
        for item in data.get("items", []):
            results.append({
                "title": item["title"],
                "image_url": item["link"],
                "source_url": item["image"]["contextLink"]
            })

        return jsonify({"query": query, "images": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
