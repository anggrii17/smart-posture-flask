# =====================================================
# SMART POSTURE MONITORING SYSTEM
# Backend Flask + Random Forest
# =====================================================

from flask import Flask, request, jsonify
import joblib
import pandas as pd
from database import save_prediction

# =====================================================
# MEMBUAT APLIKASI FLASK
# =====================================================

app = Flask(__name__)

# =====================================================
# LOAD MODEL RANDOM FOREST
# =====================================================

try:
    model = joblib.load("random_forest_model.pkl")
    print("✅ Model Random Forest berhasil dimuat.")
except Exception as e:
    print("Gagal memuat model :", e)

# =====================================================
# HALAMAN HOME
# =====================================================

@app.route("/")
def home():
    return jsonify({
        "message": "Smart Posture Monitoring API",
        "status": "Running"
    })

# =====================================================
# TEST PREDIKSI
# Digunakan untuk pengujian melalui browser
#
# Contoh:
# http://127.0.0.1:5000/test?pitch=12.5
# =====================================================

@app.route("/test", methods=["GET"])
def test():

    try:

        # Ambil nilai pitch dari URL
        pitch = float(request.args.get("pitch"))

        # Bentuk data sesuai saat training
        input_data = pd.DataFrame({
            "pitch": [pitch]
        })

        # Prediksi menggunakan Random Forest
        pred = model.predict(input_data)[0]

        # Konversi hasil prediksi menjadi label
        status = "Ergonomis" if pred == 0 else "Tidak Ergonomis"

        return jsonify({
            "success": True,
            "pitch": pitch,
            "prediction": int(pred),
            "status": status
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

# =====================================================
# ENDPOINT PREDIKSI
# Endpoint ini akan dipanggil oleh ESP32
# =====================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # Ambil data JSON dari ESP32
        data = request.get_json()

        if data is None:
            return jsonify({
                "success": False,
                "error": "Body JSON tidak ditemukan."
            }), 400

        # Ambil nilai pitch
        pitch = float(data["pitch"])

        # Bentuk DataFrame
        input_data = pd.DataFrame({
            "pitch": [pitch]
        })

        # Prediksi menggunakan Random Forest
        pred = model.predict(input_data)[0]

        # Konversi hasil prediksi
        status = "Ergonomis" if pred == 0 else "Tidak Ergonomis"

        # ==========================================
        # SIMPAN KE DATABASE
        # ==========================================

        save_prediction(pitch, status)

        # Kirim hasil ke ESP32
        return jsonify({
            "success": True,
            "pitch": pitch,
            "prediction": int(pred),
            "status": status
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# =====================================================
# MENJALANKAN SERVER
# =====================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)