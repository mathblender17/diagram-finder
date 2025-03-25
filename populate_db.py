from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define Image Model (must match MV_w_like.py)
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    source_url = db.Column(db.String(500), nullable=True)
    

# List of 50 images (You can replace URLs with actual images)
image_data = [
    {"title": "Bacteria Cell Structure", "image_url": "https://example.com/bacteria1.jpg", "source_url": "https://example.com"},
    {"title": "Bacterial Flagella", "image_url": "https://example.com/bacteria2.jpg", "source_url": "https://example.com"},
    {"title": "Binary Fission in Bacteria", "image_url": "https://example.com/bacteria3.jpg", "source_url": "https://example.com"},
    {"title": "Bacterial Growth Curve", "image_url": "https://example.com/bacteria4.jpg", "source_url": "https://example.com"},
    {"title": "Prokaryotic Bacteria Cell", "image_url": "https://example.com/bacteria5.jpg", "source_url": "https://example.com"},
    {"title": "Gram-Positive vs Gram-Negative Bacteria", "image_url": "https://example.com/bacteria6.jpg", "source_url": "https://example.com"},
    {"title": "E. coli Structure", "image_url": "https://example.com/bacteria7.jpg", "source_url": "https://example.com"},
    {"title": "Bacterial Conjugation", "image_url": "https://example.com/bacteria8.jpg", "source_url": "https://example.com"},
    {"title": "Bacterial Plasmids", "image_url": "https://example.com/bacteria9.jpg", "source_url": "https://example.com"},
    {"title": "Bacterial Capsule", "image_url": "https://example.com/bacteria10.jpg", "source_url": "https://example.com"},
    {"title": "Bacterial Pili", "image_url": "https://example.com/bacteria11.jpg", "source_url": "https://example.com"},
    {"title": "Salmonella Bacteria", "image_url": "https://example.com/bacteria12.jpg", "source_url": "https://example.com"},
    {"title": "Staphylococcus aureus", "image_url": "https://example.com/bacteria13.jpg", "source_url": "https://example.com"},
    {"title": "Streptococcus Bacteria", "image_url": "https://example.com/bacteria14.jpg", "source_url": "https://example.com"},
    {"title": "Bacterial Cell Wall", "image_url": "https://example.com/bacteria15.jpg", "source_url": "https://example.com"},
    {"title": "Bacterial Transformation", "image_url": "https://example.com/bacteria16.jpg", "source_url": "https://example.com"},
    {"title": "Bacterial Transduction", "image_url": "https://example.com/bacteria17.jpg", "source_url": "https://example.com"},
    {"title": "Bacterial Endospore", "image_url": "https://example.com/bacteria18.jpg", "source_url": "https://example.com"},
    {"title": "Bacillus Bacteria", "image_url": "https://example.com/bacteria19.jpg", "source_url": "https://example.com"},
    {"title": "Coccus Bacteria", "image_url": "https://example.com/bacteria20.jpg", "source_url": "https://example.com"},
    {"title": "Spirilla Bacteria", "image_url": "https://example.com/bacteria21.jpg", "source_url": "https://example.com"},
    {"title": "Vibrio cholerae", "image_url": "https://example.com/bacteria22.jpg", "source_url": "https://example.com"},
    {"title": "Neisseria gonorrhoeae", "image_url": "https://example.com/bacteria23.jpg", "source_url": "https://example.com"},
    {"title": "Clostridium tetani", "image_url": "https://example.com/bacteria24.jpg", "source_url": "https://example.com"},
    {"title": "Mycobacterium tuberculosis", "image_url": "https://example.com/bacteria25.jpg", "source_url": "https://example.com"},
    {"title": "Bacterial Ribosomes", "image_url": "https://example.com/bacteria26.jpg", "source_url": "https://example.com"},
    {"title": "Bacterial DNA", "image_url": "https://example.com/bacteria27.jpg", "source_url": "https://example.com"},
    {"title": "Bacterial Cytoplasm", "image_url": "https://example.com/bacteria28.jpg", "source_url": "https://example.com"},
    {"title": "Bacterial Mesosome", "image_url": "https://example.com/bacteria29.jpg", "source_url": "https://example.com"},
    {"title": "Bacterial Nucleoid", "image_url": "https://example.com/bacteria30.jpg", "source_url": "https://example.com"},
    {"title": "Bacterial Membrane", "image_url": "https://example.com/bacteria31.jpg", "source_url": "https://example.com"},
    {"title": "Helicobacter pylori", "image_url": "https://example.com/bacteria32.jpg", "source_url": "https://example.com"},
    {"title": "Pseudomonas aeruginosa", "image_url": "https://example.com/bacteria33.jpg", "source_url": "https://example.com"},
    {"title": "Bacillus anthracis", "image_url": "https://example.com/bacteria34.jpg", "source_url": "https://example.com"},
    {"title": "Yersinia pestis", "image_url": "https://example.com/bacteria35.jpg", "source_url": "https://example.com"},
    {"title": "Borrelia burgdorferi", "image_url": "https://example.com/bacteria36.jpg", "source_url": "https://example.com"},
    {"title": "Chlamydia trachomatis", "image_url": "https://example.com/bacteria37.jpg", "source_url": "https://example.com"},
    {"title": "Bacterial LPS Structure", "image_url": "https://example.com/bacteria38.jpg", "source_url": "https://example.com"},
    {"title": "Bacterial Biofilm", "image_url": "https://example.com/bacteria39.jpg", "source_url": "https://example.com"},
    {"title": "Bacterial Colony Morphology", "image_url": "https://example.com/bacteria40.jpg", "source_url": "https://example.com"},
    {"title": "Bacterial Autotrophs", "image_url": "https://example.com/bacteria41.jpg", "source_url": "https://example.com"},
    {"title": "Bacterial Heterotrophs", "image_url": "https://example.com/bacteria42.jpg", "source_url": "https://example.com"},
    {"title": "Aerobic vs Anaerobic Bacteria", "image_url": "https://example.com/bacteria43.jpg", "source_url": "https://example.com"},
    {"title": "Bacterial Quorum Sensing", "image_url": "https://example.com/bacteria44.jpg", "source_url": "https://example.com"},
    {"title": "Bacterial Toxins", "image_url": "https://example.com/bacteria45.jpg", "source_url": "https://example.com"},
    {"title": "Bacterial Exoenzymes", "image_url": "https://example.com/bacteria46.jpg", "source_url": "https://example.com"},
    {"title": "Nitrogen-Fixing Bacteria", "image_url": "https://example.com/bacteria47.jpg", "source_url": "https://example.com"},
    {"title": "Bacterial Photosynthesis", "image_url": "https://example.com/bacteria48.jpg", "source_url": "https://example.com"},
    {"title": "Bacterial Chemosynthesis", "image_url": "https://example.com/bacteria49.jpg", "source_url": "https://example.com"},
    {"title": "Extremophile Bacteria", "image_url": "https://example.com/bacteria50.jpg", "source_url": "https://example.com"}
]

# Populate Database
with app.app_context():
    db.session.bulk_insert_mappings(Image, image_data)
    db.session.commit()
    print("✅ Database populated with 50 images!")
