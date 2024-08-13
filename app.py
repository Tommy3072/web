from flask import Flask, render_template, request
import os

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = 'uploads/'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No se ha seleccionado ningún archivo"
    
    file = request.files['file']

    if file.filename == '':
        return "No se ha seleccionado ningún archivo"

    if file and file.filename.endswith('.pdf'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return f"Archivo subido exitosamente: {file.filename}"

    return "El archivo no es un PDF válido"

@app.route('/files')
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('files.html', files=files)

if __name__ == '__main__':
    app.run(debug=True)

