from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)

# Définir le répertoire pour stocker les fichiers de logs
UPLOAD_FOLDER = 'logs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Assurez-vous que le répertoire des logs existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Route principale pour afficher l'upload des fichiers et la liste des logs
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Récupérer le fichier téléchargé
        file = request.files['file']
        if file:
            # Sauvegarder le fichier dans le répertoire 'logs'
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            return redirect(url_for('index'))  # Rediriger vers la page principale après le téléchargement

    # Lister tous les fichiers dans le répertoire des logs
    log_files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', log_files=log_files)

# Route pour afficher le contenu d'un fichier log
@app.route('/view_log/<filename>')
def view_log(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            content = file.read()
        return render_template('view_log.html', filename=filename, content=content)
    return "Le fichier n'existe pas!", 404

# Route pour télécharger un fichier log
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
