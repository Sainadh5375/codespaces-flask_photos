from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return "Welcome to the Photo Album! Visit /admin to upload and /user to view."

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if 'files' not in request.files:
            return "No file part in the request"
        files = request.files.getlist('files')  # Get the list of uploaded files
        for file in files:
            if file.filename == '':
                continue
            if file:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return redirect(url_for('admin'))
    return render_template('admin.html')


@app.route('/user')
def user():
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    image_paths = [os.path.join(app.config['UPLOAD_FOLDER'], img) for img in images]
    return render_template('user.html', images=image_paths)

if __name__ == '__main__':
    app.run(debug=True)
