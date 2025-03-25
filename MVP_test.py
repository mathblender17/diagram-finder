from flask import Flask, request, render_template_string, jsonify
import requests
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Old_images.db'  # Local database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the Image model (table)
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    source_url = db.Column(db.String(500), nullable=True)

# Function to save an image to the database
def save_image(title, image_url, source_url):
    """Saves an image record to the SQLite database."""
    new_image = Image(title=title, image_url=image_url, source_url=source_url)
    db.session.add(new_image)
    db.session.commit()

# Create the database and table (if not exists)
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    """Renders the search UI."""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Local Image Search</title>
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
            input[type="text"], button {
                padding: 10px;
                margin-bottom: 15px;
                font-size: 16px;
                width: 300px;
            }
            button {
                cursor: pointer;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
            }
        </style>
    </head>
    <body>
        <h1>Search Stored Images</h1>
        <input type="text" id="searchQuery" placeholder="Enter search term...">
        <button onclick="fetchStoredImages()">Search</button>
        <h2 id="resultTitle"></h2>
        <div class="grid" id="imageGrid"></div>

        <script>
            function fetchStoredImages() {
                let query = document.getElementById("searchQuery").value;
                if (!query) {
                    alert("Please enter a search term");
                    return;
                }

                document.getElementById("resultTitle").innerText = "Results for: " + query;

                fetch("/db_search?query=" + encodeURIComponent(query))
                .then(response => response.json())
                .then(data => {
                    let grid = document.getElementById("imageGrid");
                    grid.innerHTML = "";
                    if (data.images.length === 0) {
                        grid.innerHTML = "<p>No images found.</p>";
                    } else {
                        data.images.forEach(img => {
                            let imgElement = document.createElement("img");
                            imgElement.src = img.image_url;
                            imgElement.alt = img.title;
                            grid.appendChild(imgElement);
                        });
                    }
                })
                .catch(error => console.error("Error fetching stored images:", error));
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html_content)

@app.route('/db_search', methods=['GET'])
def db_search():
    """Searches images stored in the SQLite database."""
    query = request.args.get('query')

    if not query:
        return jsonify({"error": "Missing search query"}), 400

    # Search for images in database using case-insensitive matching
    images = Image.query.filter(Image.title.ilike(f"%{query}%")).all()

    # Convert results to JSON
    results = [{"title": img.title, "image_url": img.image_url, "source_url": img.source_url} for img in images]

    return jsonify({"query": query, "images": results})

if __name__ == '__main__':
    app.run(debug=True)
