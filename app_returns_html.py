from flask import Flask, request, jsonify, render_template_string
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Retrieve keys from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

# Google Search URL
GOOGLE_SEARCH_URL = "https://www.googleapis.com/customsearch/v1"

# Route to handle image search and display in grid
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
        
        # Fetching image URLs
        image_urls = []
        for item in data.get("items", []):
            image_urls.append(item["link"])

        # Rendering images in a grid format using HTML
        html_content = """
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Image Search Results</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    padding: 20px;
                }
                .grid {
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 15px;
                    width: 100%;
                    max-width: 1200px;
                }
                .grid img {
                    width: 100%;
                    height: auto;
                    border-radius: 8px;
                }
            </style>
        </head>
        <body>
            <h1>Search Results for: {{ query }}</h1>
            <div class="grid">
                {% for url in image_urls %}
                    <img src="{{ url }}" alt="Image" />
                {% endfor %}
            </div>
        </body>
        </html>
        """
        
        return render_template_string(html_content, query=query, image_urls=image_urls)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
