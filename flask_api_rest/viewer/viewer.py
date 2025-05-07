from flask import Flask, render_template, request
import os
import markdown

app = Flask(__name__)

# Lista di directory da esplorare
DIRECTORY_PATHS = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files'),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../NOPRO'),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../PRO')
]

@app.route('/')
def index():
    directories_content = {}

    for directory_path in DIRECTORY_PATHS:
        directory_name = os.path.basename(directory_path)
        files = []
        
        try:
            # Ottieni i file dalla directory
            if os.path.exists(directory_path):
                files = os.listdir(directory_path)
            else:
                files = []
        except FileNotFoundError:
            files = []
        
        directories_content[directory_name] = files

    return render_template('index.html', directories_content=directories_content)

@app.route('/view/<directory_name>/<filename>')
def view_file(directory_name, filename):
    # Trova il percorso completo della directory
    directory_path = None
    for path in DIRECTORY_PATHS:
        if os.path.basename(path) == directory_name:
            directory_path = path
            break

    if directory_path:
        file_path = os.path.join(directory_path, filename)
        
        # Se il file è un file Markdown (.md)
        if filename.endswith('.md') and os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                # Converte il contenuto Markdown in HTML
                content_html = markdown.markdown(content)
            return render_template('view_file.html', filename=filename, content=content_html)
        
        # Altrimenti, per file non Markdown, apri e leggi come testo
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return render_template('view_file.html', filename=filename, content=content)
    
    return f"Il file {filename} non esiste nella directory {directory_name}.", 404

if __name__ == '__main__':
    app.run(debug=True)
