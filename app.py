from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = 'uploads/'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload_and_list_files():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No se ha seleccionado ningún archivo"
        
        file = request.files['file']

        if file.filename == '':
            return "No se ha seleccionado ningún archivo"

        if file and file.filename.endswith('.pdf'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            return render_template('upload.html', files=os.listdir(app.config['UPLOAD_FOLDER']), message=f"Archivo subido exitosamente: {file.filename}")
        
        return render_template('upload.html', files=os.listdir(app.config['UPLOAD_FOLDER']), message="El archivo no es un PDF válido")
    
    return render_template('upload.html', files=os.listdir(app.config['UPLOAD_FOLDER']))

@app.route('/uploads/<filename>')
def serve_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)

