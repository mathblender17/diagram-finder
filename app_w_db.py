from flask import Flask, request, render_template_string
from flask_sqlalchemy import SQLAlchemy
from rapidfuzz import process

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Old_images.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define Image model
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    source_url = db.Column(db.String(500), nullable=True)

# HTML Template for displaying search results
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Image Search</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin: 40px; }
        .container { width: 50%; margin: auto; }
        input { width: 80%; padding: 10px; font-size: 16px; }
        button { padding: 10px 15px; font-size: 16px; cursor: pointer; }
        .image-card { margin: 20px; padding: 10px; border: 1px solid #ddd; display: inline-block; }
        img { max-width: 200px; height: auto; }
    </style>
</head>
<body>
    <h1>Image Search</h1>
    <form method="GET" action="/db_search">
        <input type="text" name="query" placeholder="Search images..." required>
        <button type="submit">Search</button>
    </form>
    
    {% if query %}
        <h2>Results for: "{{ query }}"</h2>
        {% if images %}
            {% for img in images %}
                <div class="image-card">
                    <h3>{{ img.title }}</h3>
                    <a href="{{ img.source_url }}" target="_blank">
                        <img src="{{ img.image_url }}" alt="{{ img.title }}">
                    </a>
                </div>
            {% endfor %}
        {% else %}
            <p>No results found.</p>
        {% endif %}
    {% endif %}
</body>
</html>
"""

@app.route('/db_search', methods=['GET'])
def db_search():
    """Searches images using fuzzy matching and returns HTML page."""
    query = request.args.get('query')

    if not query:
        return render_template_string(HTML_TEMPLATE, query=None, images=[])

    # Fetch all stored image titles from the database
    images = Image.query.all()
    titles = [img.title for img in images]

    # Use fuzzy matching to find the best matches
    fuzzy_results = process.extract(query, titles, limit=10, score_cutoff=50)

    # Extract matching image objects
    matched_images = [
        img for img in images if img.title in [result[0] for result in fuzzy_results]
    ]

    # Render HTML template with search results
    return render_template_string(HTML_TEMPLATE, query=query, images=matched_images)

if __name__ == '__main__':
    app.run(debug=True)
