from flask import Flask, render_template, request, send_file
from PIL import Image
import numpy as np
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def encrypt_decrypt_image(image_path, key):
    img = Image.open(image_path).convert('RGB')
    data = np.array(img)
    transformed_data = data ^ key
    transformed_img = Image.fromarray(transformed_data.astype('uint8'))
    output_path = os.path.join(UPLOAD_FOLDER, f"result_{os.path.basename(image_path)}")
    transformed_img.save(output_path)
    return output_path

@app.route('/', methods=['GET', 'POST'])
def index():
    result_path = None
    if request.method == 'POST':
        if 'image' not in request.files or not request.form.get('key'):
            return render_template('index.html', error='Image and Key are required.')

        image = request.files['image']
        key = int(request.form['key'])
        mode = request.form['mode']
        image_path = os.path.join(UPLOAD_FOLDER, image.filename)
        image.save(image_path)
        result_path = encrypt_decrypt_image(image_path, key)

    return render_template('index.html', result_path=result_path)

@app.route('/download/<filename>')
def download(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
