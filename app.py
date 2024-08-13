from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['SECRET_KEY'] = 'your_secret_key'  # Necesario para Flask-Login

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# Dummy database
users = {'user1': User(1, 'user1', generate_password_hash('password'))}

@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if user.id == int(user_id):
            return user
    return None

@app.route('/')
@login_required
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            message = "Invalid username or password"
    return render_template('login.html', message=message)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/upload')
@login_required
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
@login_required
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
@login_required
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('files.html', files=files)

@app.route('/uploads/<filename>')
@login_required
def serve_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)

