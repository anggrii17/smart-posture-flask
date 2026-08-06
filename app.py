# =====================================================
# SMART POSTURE MONITORING SYSTEM
# Backend Flask + Random Forest
# =====================================================

from flask import Flask, request, jsonify
import joblib
import pandas as pd
# from database import save_prediction


# =====================================================
# FLASK APP
# =====================================================

app = Flask(__name__)


# =====================================================
# LOAD RANDOM FOREST MODEL
# =====================================================

try:

    model = joblib.load("random_forest_model.pkl")

    print("================================")
    print("MODEL RANDOM FOREST BERHASIL DIMUAT")
    print("FEATURE MODEL :", model.feature_names_in_)
    print("================================")


except Exception as e:

    print("GAGAL LOAD MODEL :", e)
    model = None



# =====================================================
# HOME
# =====================================================

@app.route("/")
def home():

    return jsonify({
        "message": "Smart Posture Monitoring API",
        "status": "Running"
    })



# =====================================================
# TEST PREDIKSI
# =====================================================

@app.route("/test", methods=["GET"])
def test():

    try:

        pitch = float(request.args.get("pitch"))


        input_data = pd.DataFrame({
            "pitch": [pitch]
        })


        pred = model.predict(input_data)[0]


        status = (
            "Ergonomis"
            if pred == 0
            else "Tidak Ergonomis"
        )


        return jsonify({

            "success": True,
            "pitch": pitch,
            "prediction": int(pred),
            "status": status

        })


    except Exception as e:

        print("ERROR TEST :", e)

        return jsonify({

            "success": False,
            "error": str(e)

        }),500




# =====================================================
# PREDICT DARI ESP32
# =====================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        print("==============================")
        print("REQUEST MASUK")


        data = request.get_json()


        print("DATA :", data)


        if data is None:

            return jsonify({

                "success": False,
                "error": "JSON tidak ditemukan"

            }),400



        pitch = float(data["pitch"])


        print("PITCH :", pitch)



        input_data = pd.DataFrame({

            "pitch": [pitch]

        })


        print("SEBELUM RANDOM FOREST")


        pred = model.predict(input_data)[0]


        print("HASIL RF :", pred)



        status = (

            "Ergonomis"
            if pred == 0
            else "Tidak Ergonomis"

        )


        print("STATUS :", status)
        
        save_prediction(
            pitch,
            status
        )

        print("DATABASE OK")


        return jsonify({

            "success": True,
            "pitch": pitch,
            "prediction": int(pred),
            "status": status

        })



    except Exception as e:


        print("==============================")
        print("ERROR PREDICT :", e)
        print("==============================")


        return jsonify({

            "success": False,
            "error": str(e)

        }),500




# =====================================================
# RUN
# =====================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )