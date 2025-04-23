from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

from nlp import analyze_text
from gpt_integration import generate_text

app = Flask(__name__)

# Configure SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define a simple model to store NLP analysis results
class AnalysisResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    entities = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

@app.route('/')
def index():
    return "Flask NLP app is running."

@app.route('/analyze-text', methods=['POST'])
def analyze_text_route():
    data = request.get_json()
    text = data.get('text', '')
    if not text:
        return jsonify({"error": "No text provided"}), 400
    result = analyze_text(text)
    return jsonify(result)

@app.route('/generate-text', methods=['POST'])
def generate_text_route():
    data = request.get_json()
    prompt = data.get('prompt', '')
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    generated = generate_text(prompt)
    return jsonify({"generated_text": generated})

@app.route('/store-analysis', methods=['POST'])
def store_analysis():
    data = request.get_json()
    text = data.get('text', '')
    entities = data.get('entities', '')
    if not text:
        return jsonify({"error": "No text provided"}), 400
    analysis = AnalysisResult(text=text, entities=str(entities))
    db.session.add(analysis)
    db.session.commit()
    return jsonify({"message": "Analysis stored", "id": analysis.id})

if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    app.run(debug=True)
