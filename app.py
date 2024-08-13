from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Crear el directorio para subir archivos si no existe
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

@app.route('/uploads/<filename>')
def serve_file(filename):
    # Sirve el archivo para su descarga
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)

