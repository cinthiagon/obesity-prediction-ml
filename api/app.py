from flask import Flask, request, jsonify
import joblib
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "obesity_model.pkl")

model = joblib.load(MODEL_PATH)

@app.route("/")
def home():
    return jsonify({"status": "API online"})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    prediction = model.predict([data])[0]
    return jsonify({"prediction": prediction})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
