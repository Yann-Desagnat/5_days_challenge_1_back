import io
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS  # Permettre les requêtes depuis le front
from ultralytics import YOLO
from werkzeug.utils import secure_filename
from PIL import Image
import os
import cv2


app = Flask(__name__)
CORS(app)  # Activer CORS

# Define the path for saving temporary images
TEMP_DIR = 'temp_images'
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

# Load the model once
model = YOLO('best.pt')  # Remplace avec le chemin correct vers le fichier best.pt téléchargé depuis GitHub

@app.route('/detect', methods=['POST'])
def detect_logo():
    if 'image' not in request.files:
        return jsonify({"error": "Aucune image envoyée"}), 400

    image = request.files['image']
    
    # Read the image file into memory
    image_bytes = image.read()

    # Save the image in memory (without saving to disk)
    img = Image.open(io.BytesIO(image_bytes))

    # Perform inference on the image
    results = model.predict(img)

    # Get the processed image (this is a NumPy array)
    output_image = results[0].plot()  # This is a NumPy array with the results plotted

    # Convert the NumPy array to a PIL image

    output_image_rgb = cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)

    pil_image = Image.fromarray(output_image_rgb)

    # Save the processed image with predictions to a bytes buffer (in memory)
    img_byte_arr = io.BytesIO()
    pil_image.save(img_byte_arr, format='JPEG')  # Save the PIL image into the byte stream

    # Move the pointer to the beginning of the byte stream
    img_byte_arr.seek(0)

    # Return the image directly as a response
    return send_file(img_byte_arr, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
