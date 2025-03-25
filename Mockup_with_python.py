from flask import Flask, request, render_template_string, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Retrieve API credentials
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

# Google Custom Search API URL
GOOGLE_SEARCH_URL = "https://www.googleapis.com/customsearch/v1"

# Home route - renders search form
@app.route('/')
def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Image Search</title>
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
            input[type="text"], select {
                padding: 10px;
                margin-bottom: 15px;
                font-size: 16px;
                width: 300px;
            }
            button {
                padding: 10px;
                font-size: 16px;
                cursor: pointer;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
            }
        </style>
    </head>
    <body>
        <h1>Search for Images</h1>
        <input type="text" id="searchQuery" placeholder="Enter search term...">
        <select id="imageType">
            <option value="">-- Select Image Type --</option>
            <option value="diagram">Diagram</option>
            <option value="flowchart">Flowchart</option>
            <option value="map">Map</option>
            <option value="graph">Graph</option>
            <option value="model">Model</option>
        </select>
        <button onclick="fetchImages()">Search</button>
        <h2 id="resultTitle"></h2>
        <div class="grid" id="imageGrid"></div>

        <script>
            function fetchImages() {
                let query = document.getElementById("searchQuery").value;
                let type = document.getElementById("imageType").value;

                if (!query) {
                    alert("Please enter a search term");
                    return;
                }

                let fullQuery = type ? query + " " + type : query;
                document.getElementById("resultTitle").innerText = "Results for: " + fullQuery;
                
                fetch("/search?query=" + encodeURIComponent(fullQuery))
                .then(response => response.json())
                .then(data => {
                    let grid = document.getElementById("imageGrid");
                    grid.innerHTML = "";
                    data.images.forEach(img => {
                        let imgElement = document.createElement("img");
                        imgElement.src = img.image_url;
                        imgElement.alt = "Image result";
                        grid.appendChild(imgElement);
                    });
                })
                .catch(error => console.error("Error fetching images:", error));
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html_content)

# Image search API
@app.route('/search', methods=['GET'])
def search_images():
    query = request.args.get('query')
    
    if not query:
        return jsonify({"error": "Missing search query"}), 400

    params = {
        "q": query,  # Now using only the selected image type
        "cx": SEARCH_ENGINE_ID,
        "key": GOOGLE_API_KEY,
        "searchType": "image",
        "num": 10  # Fetch 10 images
    }

    try:
        response = requests.get(GOOGLE_SEARCH_URL, params=params)
        data = response.json()
        
        # Fetch image URLs
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
