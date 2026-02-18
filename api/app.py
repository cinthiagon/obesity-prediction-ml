from flask import Flask, request, jsonify
import joblib
import os
import pandas as pd

app = Flask(__name__)

# ======================================================
# CONFIGURAÇÃO DE CAMINHO DO MODELO
# ======================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "obesity_model.pkl")

# Carregar modelo
try:
    model = joblib.load(MODEL_PATH)
    print("Modelo carregado com sucesso.")
except Exception as e:
    print(f"Erro ao carregar modelo: {e}")
    model = None


# ======================================================
# ROTA RAIZ (HEALTH CHECK)
# ======================================================
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "API online",
        "service": "Obesity Prediction API",
        "version": "1.0"
    })


# ======================================================
# ROTA DE PREDIÇÃO
# ======================================================
@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Modelo não carregado."}), 500

    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "JSON vazio ou inválido."}), 400

        # Converter para DataFrame (modelo espera estrutura tabular)
        input_df = pd.DataFrame([data])

        prediction = model.predict(input_df)[0]

        return jsonify({
            "prediction": prediction
        })

    except Exception as e:
        return jsonify({
            "error": "Erro ao processar requisição.",
            "details": str(e)
        }), 500


# ======================================================
# EXECUÇÃO (IMPORTANTE PARA RENDER)
# ======================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
