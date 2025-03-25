import random
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define Models
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    source_url = db.Column(db.String(500), nullable=True)

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=False)
    like_count = db.Column(db.Integer, default=0)  # Store like count here

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=False)
    text = db.Column(db.String(500), nullable=False)

# Sample comments
comments = [
    "Amazing image!",
    "Great explanation of bacteria!",
    "Very informative!",
    "I love microbiology!",
    "Wow, I didn't know that about bacteria!"
]

# Populate Likes and Comments
with app.app_context():
    images = Image.query.all()
    
    for img in images:
        # Randomly add 0-10 likes per image
        like_entry = Like(image_id=img.id, like_count=random.randint(0, 10))
        db.session.add(like_entry)

        # Randomly add 0-3 comments per image
        for _ in range(random.randint(0, 3)):
            comment = Comment(image_id=img.id, text=random.choice(comments))
            db.session.add(comment)

    db.session.commit()
    print("✅ Likes & Comments added!")
