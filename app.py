from flask import Flask, request, render_template, send_file
from PIL import Image
import io
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return {'error': 'No file uploaded'}, 400

    file = request.files['file']
    if file.filename == '':
        return {'error': 'No selected file'}, 400

    try:
        image = Image.open(file.stream).convert("RGB")
        output = io.BytesIO()
        image.save(output, format='PDF')
        output.seek(0)
        return send_file(output, download_name=f"{os.path.splitext(file.filename)[0]}.pdf", as_attachment=True)
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)