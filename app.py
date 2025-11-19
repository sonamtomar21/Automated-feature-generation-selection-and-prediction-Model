# app.py
import os
import joblib
import numpy as np
from flask import Flask, request, jsonify, render_template

MODEL_PATH = os.environ.get("MODEL_PATH", "models/model.joblib")

app = Flask(__name__, template_folder="templates", static_folder="static")

bundle = None
if os.path.exists(MODEL_PATH):
    bundle = joblib.load(MODEL_PATH)
    model = bundle['model']
    encoders = bundle.get('encoders', {})
    feature_order = bundle.get('features', [])
else:
    model = None
    encoders = {}
    feature_order = []

@app.route("/")
def index():
    return render_template("index.html", features=feature_order)

@app.route("/health")
def health():
    return jsonify({"status":"ok", "model_loaded": model is not None})

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error":"Model not loaded"}), 500
    data = request.get_json(force=True)
    if not isinstance(data, dict):
        return jsonify({"error":"JSON object required"}), 400

    # Build feature vector in same order as training
    try:
        fv = []
        for f in feature_order:
            if f not in data:
                return jsonify({"error": f"Missing feature '{f}' in JSON body"}), 400
            val = data[f]
            # handle proto encoding
            if f == 'proto' and 'proto' in encoders:
                le = encoders['proto']
                val = str(val)
                if val not in le.classes_:
                    # unknown class — map to new index by adding to classes_
                    # fallback: transform by adding unseen as -1 -> safe numeric
                    try:
                        val_enc = int(le.transform([val])[0])
                    except Exception:
                        # fallback to a safe numeric: most common index 0
                        val_enc = 0
                    val = val_enc
                else:
                    val = int(le.transform([val])[0])
            fv.append(float(val))
        X = np.array([fv])
        pred = model.predict(X)[0]
        proba = None
        if hasattr(model, "predict_proba"):
            try:
                proba = float(model.predict_proba(X).max())
            except Exception:
                proba = None
        return jsonify({"prediction": int(pred), "probability": proba}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
