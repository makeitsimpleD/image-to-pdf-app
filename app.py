from flask import Flask, request, send_file, render_template
from PIL import Image
import io
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_image():
    if 'file' not in request.files:
        return {"error": "No file uploaded"}, 400

    file = request.files['file']

    if file.filename == '':
        return {"error": "Empty filename"}, 400

    try:
        image = Image.open(file.stream).convert("RGB")
        pdf_bytes = io.BytesIO()
        image.save(pdf_bytes, format='PDF')
        pdf_bytes.seek(0)
        return send_file(pdf_bytes, mimetype='application/pdf', download_name='converted.pdf')
    except Exception as e:
        return {"error": str(e)}, 500

# 👇 Wichtig für Railway Deployment
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
