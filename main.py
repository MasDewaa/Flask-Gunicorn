from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image

# 1️⃣ Inisialisasi Flask
app = Flask(__name__)
CORS(app)  # Izinkan CORS untuk semua origin. Untuk lebih aman, sesuaikan origins.

# 2️⃣ Load model Keras
model = tf.keras.models.load_model("mymodel.keras")

# 3️⃣ Load labels dari file
with open("labels.txt") as f:
    labels = [line.strip() for line in f]

# 4️⃣ Ukuran input gambar
IMAGE_SIZE = (224, 224)  # Sesuaikan dengan model kamu

# 5️⃣ Endpoint root
@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "Flask Batik Classifier is running!"})

# 6️⃣ Endpoint prediksi
@app.route("/predict", methods=["POST"])
def predict():
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "error": "No selected file"}), 400

    try:
        # Baca dan preprocess gambar
        image = Image.open(file.stream).convert("RGB")
        image = image.resize(IMAGE_SIZE)
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)

        # Prediksi
        predictions = model.predict(image_array)[0]
        prediction_list = [
            {"label": labels[i], "confidence": float(pred)}
            for i, pred in enumerate(predictions)
        ]
        prediction_list.sort(key=lambda x: x["confidence"], reverse=True)
        top_predictions = prediction_list[:5]
        top_prediction = top_predictions[0]

        return jsonify({
            "success": True,
            "data": {
                "class_name": top_prediction["label"],
                "confidence": top_prediction["confidence"],
                "probabilities": {
                    p["label"]: p["confidence"] for p in top_predictions
                }
            }
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# 7️⃣ Run Flask (jika dijalankan langsung)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
