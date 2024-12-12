from flask import Flask, render_template, request, jsonify
import os
from elasticsearch import Elasticsearch
from werkzeug.utils import secure_filename

app = Flask(__name__,template_folder='app/templates')
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# Add UPLOAD_FOLDER to app configuration
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Configuration Elasticsearch
ELASTICSEARCH_HOST = "http://localhost:9200"  
INDEX_NAME = "logs"
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    es = Elasticsearch(
    hosts=["http://localhost:9200"],
    timeout=60,
    max_retries=10,
    retry_on_timeout=True
)
    if 'logfile' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['logfile']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Sécuriser le nom de fichier
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Sauvegarder le fichier
    file.save(filepath)
    
    # Lire et indexer le contenu dans Elasticsearch
    try:
        # with open(filepath, 'r') as f:
            # for line_number, line in enumerate(f, start=1):
            #     response = es.index(index=INDEX_NAME, body={
            #     "line_number": line_number,
            #     "content": line.strip(),
            #     "filename": filename
            #     })
            #     if response.get('result') != 'created':
                response = es.index(
                index="Transaction",
                id=12345,
                body= {"time":"2024-12-12 18:56:52", "TransactionID": 12345, "Montant": "1131.49", "Devise": "TND", "Utilisateur": "user090", "Type": "Virement", "Statut": "Échoué"}

            )
                    # raise Exception(f"Failed to index line {line_number}")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "File uploaded and indexed successfully", "filename": filename})

@app.route('/search', methods=['GET'])
def search_logs():
    query = request.args.get('query', '')
    results = es.search(index="logs", query={"match": {"message": query}})
    return jsonify(results["hits"]["hits"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
