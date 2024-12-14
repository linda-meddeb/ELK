import pdb
import re
from flask import Flask, render_template, request, jsonify
import os
from elasticsearch import Elasticsearch
from werkzeug.utils import secure_filename
import csv
import json
import os
app = Flask(__name__,template_folder='app/templates')
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
log_line_pattern = re.compile(r'(\w+): ([^,]+)')

# Add UPLOAD_FOLDER to app configuration
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Configuration Elasticsearch
ELASTICSEARCH_HOST = "http://localhost:9200"  
INDEX_NAME = "logs"
es = Elasticsearch(hosts=["http://elasticsearch:9200"],timeout=60,max_retries=10,retry_on_timeout=True)




################################################UTILS#####################################
def process_file(filepath,table_name):
    file_extension = os.path.splitext(filepath)[1].lower()

    if file_extension == '.csv':
        process_csv(filepath,table_name)
    elif file_extension == '.log':
        process_log(filepath,table_name)
    else:
        raise Exception(f"Type de fichier non supporté: {file_extension}")

def process_csv(filepath,table_name):
    try:
        with open(filepath, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for line_number, row in enumerate(reader, start=1):
                response = es.index(
                    index=table_name,
                    id=row.get("ID", line_number),  
                    body=row
                )
            return True
    except Exception as e:
       raise Exception(f"Erreur lors du traitement du fichier CSV: {e}")

def process_log(filepath,table_name):
    try:
        with open(filepath, 'r') as log_file:
            for line_number, line in enumerate(log_file, start=1):
                matches = log_line_pattern.findall(line)
                if matches:
                    log_entry = {key.strip(): value.strip() for key, value in matches}
                    response = es.index(index=table_name, id=log_entry.get("TransactionID", line_number), document=log_entry)

                else:
                   raise Exception(f"Ligne non valide au numéro {line_number}: {line.strip()}")
            return True
    except Exception as e:
       raise Exception(f"Erreur lors du traitement du fichier LOG: {e}")

#################################################API#################################################################""
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    
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
    
    try:
        result =process_file(filepath,filename)
        if not result:
            jsonify({"error":True,"message":"Erreur lors de l'indexation du file"}),406
    except Exception as e:
        return jsonify({"error":True,"message": str(e)}), 500

    return jsonify({"message": "File uploaded and indexed successfully", "filename": filename})

@app.route('/search', methods=['GET'])
def search_index():
    index_name = request.args.get('index')
    if not index_name:
        return jsonify({"error": "Index name is required"}), 400

    try:
        response = es.search(
            index=index_name,
            body={
                "query": {
                    "match_all": {}
                }
            },
            size=1000  
        )
        return jsonify(response['hits'])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/list_indices', methods=['GET'])
def list_indices():
    try:
        # Appeler l'API _cat/indices pour récupérer les index
        indices = es.cat.indices(format='json')
        
        # Extraire seulement les noms d'index
        index_names = [index['index'] for index in indices]
        
        return jsonify({"indices": index_names}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
