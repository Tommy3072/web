from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = 'uploads/'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    message = ""
    if request.method == 'POST':
        if 'file' not in request.files:
            message = "No se ha seleccionado ningún archivo"
        else:
            file = request.files['file']

            if file.filename == '':
                message = "No se ha seleccionado ningún archivo"
            elif file and file.filename.endswith('.pdf'):
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)
                message = f"Archivo subido exitosamente: {file.filename}"
            else:
                message = "El archivo no es un PDF válido"
    
    return render_template('upload.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)


