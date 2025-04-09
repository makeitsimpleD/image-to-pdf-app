from flask import Flask, request, send_file, render_template, jsonify
from PIL import Image
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_image_to_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "Keine Datei im Formular gefunden"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "Keine Datei ausgewählt"}), 400

    try:
        img = Image.open(file.stream).convert('RGB')
        output_path = 'converted.pdf'
        img.save(output_path)

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": f"Fehler beim Umwandeln: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)