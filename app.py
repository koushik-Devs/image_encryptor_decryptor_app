from flask import Flask, render_template, request, send_from_directory
from PIL import Image
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = "static/output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def process_image(image, key, mode='encrypt'):
    if mode == 'decrypt':
        key = -key

    img = image.convert("RGB")
    pixels = img.load()
    width, height = img.size

    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            r = (r + key) % 256
            g = (g + key) % 256
            b = (b + key) % 256
            pixels[x, y] = (r, g, b)
    
    return img

@app.route('/', methods=['GET', 'POST'])
def index():
    filename = None
    if request.method == 'POST':
        image_file = request.files['image']
        key = int(request.form['key'])
        mode = request.form['mode']

        if image_file:
            image = Image.open(image_file)
            processed_image = process_image(image, key, mode)

            filename = f"{uuid.uuid4().hex}.png"
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            processed_image.save(save_path)

    return render_template('index.html', filename=filename)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
