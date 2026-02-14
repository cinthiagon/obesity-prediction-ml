from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os

app = Flask(__name__)

# =========================
# Carregar modelo (pipeline completo)
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "obesity_model.pkl")

model = joblib.load(MODEL_PATH)


# =========================
# Health check (produção)
# =========================
@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "API online"})


# =========================
# Endpoint de predição
# =========================
@app.route("/predict", methods=["POST"])
def predict():

    try:
        data = request.get_json()

        # Converter para DataFrame
        input_df = pd.DataFrame([data])

        # Predição
        prediction = model.predict(input_df)[0]

        return jsonify({
            "prediction": prediction
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
