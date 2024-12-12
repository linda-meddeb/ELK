from flask import Flask, render_template, request, jsonify
import os
from elasticsearch import Elasticsearch

app = Flask(__name__,template_folder='app/templates')
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configuration Elasticsearch
es = Elasticsearch("http://elasticsearch:9200")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'logfile' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['logfile']
    if file.filename == '':
        return "No selected file", 400
    
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    return jsonify({"message": "File uploaded successfully", "filename": file.filename})

@app.route('/search', methods=['GET'])
def search_logs():
    query = request.args.get('query', '')
    results = es.search(index="logs", query={"match": {"message": query}})
    return jsonify(results["hits"]["hits"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
