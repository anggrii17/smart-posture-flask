# =====================================================
# SMART POSTURE MONITORING SYSTEM
# Backend Flask + Random Forest + Flutter API
# =====================================================

from flask import Flask, request, jsonify
from datetime import timezone
import joblib
import pandas as pd
import pymysql

from database import save_prediction
from config import *


# =====================================================
# FLASK APP
# =====================================================

app = Flask(__name__)



# =====================================================
# CONNECTION DATABASE
# Digunakan untuk Flutter
# =====================================================

def get_connection():

    return pymysql.connect(
        host=DB_HOST,
        port=int(DB_PORT),
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )



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
# TEST RANDOM FOREST
# =====================================================

@app.route("/test", methods=["GET"])
def test():

    try:

        pitch = float(request.args.get("pitch"))


        input_data = pd.DataFrame({

            "pitch":[pitch]

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

                "success":False,
                "error":"JSON tidak ditemukan"

            }),400




        pitch = float(data["pitch"])



        print("PITCH :", pitch)



        input_data = pd.DataFrame({

            "pitch":[pitch]

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





        # SIMPAN DATABASE

        try:

            save_prediction(
                pitch,
                status
            )


            print("DATABASE BERHASIL")



        except Exception as e:

            print("DATABASE GAGAL :", e)




        return jsonify({

            "success":True,
            "pitch":pitch,
            "prediction":int(pred),
            "status":status

        })




    except Exception as e:


        print("==============================")
        print("ERROR PREDICT :", e)
        print("==============================")


        return jsonify({

            "success":False,
            "error":str(e)

        }),500





# =====================================================
# API UNTUK FLUTTER
# CURRENT POSTURE
# =====================================================

@app.route("/current", methods=["GET"])
def current():

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM current_posture
            WHERE id = 1
        """)

        data = cursor.fetchone()

        cursor.close()
        conn.close()

        if data:

            dt = data["timestamp"]

            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)

            data["timestamp"] = dt.isoformat()
            data["timestamp_unix"] = int(dt.timestamp())

        return jsonify({
            "success": True,
            "data": data
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500





# =====================================================
# API UNTUK FLUTTER
# POSTURE LOGS
# =====================================================

@app.route("/logs", methods=["GET"])
def logs():

    try:


        conn = get_connection()
        cursor = conn.cursor()



        cursor.execute("""
            SELECT *
            FROM posture_logs
            ORDER BY id DESC
            LIMIT 50
        """)



        data = cursor.fetchall()



        cursor.close()
        conn.close()



        return jsonify({

            "success":True,
            "data":data

        })



    except Exception as e:


        return jsonify({

            "success":False,
            "error":str(e)

        }),500





# =====================================================
# RUN SERVER
# =====================================================

if __name__ == "__main__":


    app.run(

        host="0.0.0.0",
        port=5000

    )