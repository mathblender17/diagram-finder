from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from fuzzywuzzy import fuzz, process

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    source_url = db.Column(db.String(500), nullable=True)

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=False)
    like_count = db.Column(db.Integer, default=0)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=False)
    text = db.Column(db.String(500), nullable=False)

# Create Tables
with app.app_context():
    db.create_all()

# Home Route
@app.route('/')
def home():
    return render_template("index.html")

# Like an Image
@app.route('/like/<int:image_id>', methods=['POST'])
def like_image(image_id):
    like_entry = Like.query.filter_by(image_id=image_id).first()
    
    if not like_entry:
        like_entry = Like(image_id=image_id, like_count=1)
        db.session.add(like_entry)
    else:
        like_entry.like_count += 1

    db.session.commit()
    return jsonify({"message": "Image liked!", "likes": like_entry.like_count})

# Add a Comment
@app.route('/comment/<int:image_id>', methods=['POST'])
def add_comment(image_id):
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "Comment cannot be empty"}), 400

    comment = Comment(image_id=image_id, text=text)
    db.session.add(comment)
    db.session.commit()
    return jsonify({"message": "Comment added!", "comment": text})

# Fetch Comments for an Image
@app.route('/comments/<int:image_id>', methods=['GET'])
def get_comments(image_id):
    comments = Comment.query.filter_by(image_id=image_id).all()
    return jsonify({"image_id": image_id, "comments": [c.text for c in comments]})

# Search for Images
@app.route('/search', methods=['GET'])
def search_images():
    query = request.args.get('query', '').strip().lower()

    if not query:
        return jsonify({"error": "Search query cannot be empty"}), 400

    all_images = Image.query.all()
    image_titles = [(img.id, img.title) for img in all_images]

    # Fuzzy matching
    matches = process.extract(query, [title for _, title in image_titles], scorer=fuzz.partial_ratio, limit=10)
    matched_images = [img_id for (img_id, title), score in zip(image_titles, matches) if score >= 60]

    # Retrieve matching image details
    results = Image.query.filter(Image.id.in_(matched_images)).all()

    return jsonify({
        "query": query,
        "results": [
            {
                "id": img.id,
                "title": img.title,
                "image_url": img.image_url,
                "likes": Like.query.filter_by(image_id=img.id).first().like_count if Like.query.filter_by(image_id=img.id).first() else 0,
                "comments": [c.text for c in Comment.query.filter_by(image_id=img.id).all()]
            } 
            for img in results
        ]
    })

if __name__ == '__main__':
    app.run(debug=True)
