from flask import Flask, request, jsonify
from flask_cors import CORS  # Permettre les requêtes depuis le front

app = Flask(__name__)
CORS(app)  # Activer CORS

@app.route('/detect', methods=['POST'])
def detect_logo():
    if 'image' not in request.files:
        return jsonify({"error": "Aucune image envoyée"}), 400

    image = request.files['image']

    # 🚀 Ici, ajoute ton traitement YOLO pour détecter les logos
    # Exemple simplifié :
    detected_logos = ["Nike", "Adidas"]  # Simule une détection de logo

    return jsonify({
        "message": "Détection terminée",
        "filename": image.filename,
        "detected_logos": detected_logos
    })

if __name__ == '__main__':
    app.run(debug=True)
