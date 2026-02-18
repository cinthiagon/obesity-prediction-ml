from flask import Flask, request, jsonify
import joblib
import os
import pandas as pd

app = Flask(__name__)

# =====================================================
# PATHS
# =====================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "obesity_model.pkl")
DATA_PATH = os.path.join(BASE_DIR, "obesity.csv")

# =====================================================
# LOAD MODEL
# =====================================================
model = joblib.load(MODEL_PATH)

# =====================================================
# LOAD DATA
# =====================================================
df = pd.read_csv(DATA_PATH)

# =====================================================
# ROOT
# =====================================================
@app.route("/")
def home():
    return jsonify({
        "service": "Obesity Prediction API",
        "status": "API online",
        "version": "2.0"
    })

# =====================================================
# PREDICTION ENDPOINT
# =====================================================
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        input_df = pd.DataFrame([data])
        prediction = model.predict(input_df)[0]

        return jsonify({
            "prediction": prediction
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400

# =====================================================
# DATA ENDPOINT (NOVO)
# =====================================================
@app.route("/data", methods=["GET"])
def get_data():
    try:
        return df.to_json(orient="records")
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
