from flask import Flask, request, render_template, send_file, jsonify
import os
import random
import string

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure uploads folder exists
files_db = {}  # Temporary in-memory storage for file info & codes

# Generate a random 6-digit verification code
def generate_code():
    return ''.join(random.choices(string.digits, k=6))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        code = generate_code()
        files_db[code] = file.filename
        return jsonify({"message": "File uploaded successfully!", "code": code})
    return jsonify({"error": "No file uploaded"}), 400

@app.route('/download', methods=['POST'])
def download_file():
    data = request.json
    code = data.get('code')
    filename = files_db.get(code)
    if filename:
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({"error": "File not found"}), 404
    return jsonify({"error": "Invalid code"}), 400

if __name__ == '__main__':
    app.run(debug=True)