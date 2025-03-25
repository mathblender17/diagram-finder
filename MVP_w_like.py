from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Define Image model
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    source_url = db.Column(db.String(500), nullable=True)

# Define Like model (with like_count column)
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=False, unique=True)
    like_count = db.Column(db.Integer, default=0)

# Define Comment model
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=False)
    text = db.Column(db.String(500), nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# Home Route
@app.route('/')
def home():
    return "Database with Search, Likes & Comments is ready!"

# Route to like an image (increments like_count)
@app.route('/like/<int:image_id>', methods=['POST'])
def like_image(image_id):
    image = Image.query.get(image_id)
    if image:
        like_entry = Like.query.filter_by(image_id=image_id).first()

        if like_entry:
            like_entry.like_count += 1  # Increment like count
        else:
            like_entry = Like(image_id=image_id, like_count=1)  # Create new entry
        
        db.session.add(like_entry)
        db.session.commit()

        return jsonify({"message": "Image liked!", "likes": like_entry.like_count})
    
    return jsonify({"error": "Image not found"}), 404

# Route to add a comment to an image
@app.route('/comment/<int:image_id>', methods=['POST'])
def add_comment(image_id):
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "Comment cannot be empty"}), 400

    image = Image.query.get(image_id)
    if image:
        comment = Comment(image_id=image.id, text=text)
        db.session.add(comment)
        db.session.commit()
        return jsonify({"message": "Comment added!", "comment": text})
    
    return jsonify({"error": "Image not found"}), 404

# Route to fetch comments for an image
@app.route('/comments/<int:image_id>', methods=['GET'])
def get_comments(image_id):
    comments = Comment.query.filter_by(image_id=image_id).all()
    return jsonify({"image_id": image_id, "comments": [c.text for c in comments]})

# Route to search for images with fuzzy matching
@app.route('/search', methods=['GET'])
def search_images():
    query = request.args.get('query', '').strip().lower()

    if not query:
        return jsonify({"error": "Search query cannot be empty"}), 400

    all_images = Image.query.all()
    image_titles = [(img.id, img.title) for img in all_images]
    
    # Extract titles for fuzzy matching
    titles_only = [title for _, title in image_titles]

    # Get the best matches (returns tuples of (title, score))
    matches = process.extract(query, titles_only, scorer=fuzz.partial_ratio, limit=10)

    # Extract matched image IDs based on the titles found
    matched_images = [img_id for (img_id, title), (matched_title, score) in zip(image_titles, matches) if score >= 60]

    # Retrieve matching image details
    results = Image.query.filter(Image.id.in_(matched_images)).all()

    return jsonify({
        "query": query,
        "results": [
            {
                "id": img.id,
                "title": img.title,
                "image_url": img.image_url,
                "likes": Like.query.filter_by(image_id=img.id).first().like_count if Like.query.filter_by(image_id=img.id).first() else 0
            } 
            for img in results
        ]
    })

if __name__ == '__main__':
    app.run(debug=True)
