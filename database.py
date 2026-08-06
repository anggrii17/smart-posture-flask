# =====================================================
# KONEKSI DATABASE MYSQL
# =====================================================

import pymysql
from datetime import datetime, timedelta
from config import *


print("==========================")
print("DATABASE.PY TERBACA")
print("DATABASE CONFIG")
print("HOST :", DB_HOST)
print("PORT :", DB_PORT)
print("USER :", DB_USER)
print("DB   :", DB_NAME)
print("==========================")


# =====================================================
# CONNECTION
# =====================================================

def get_connection():

    try:

        conn = pymysql.connect(
            host=DB_HOST,
            port=int(DB_PORT),
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
            connect_timeout=5,
            read_timeout=5,
            write_timeout=5
        )

        print("✅ MYSQL CONNECTED")

        return conn


    except Exception as e:

        print("❌ MYSQL CONNECTION ERROR :", e)

        raise e



# =====================================================
# UPDATE DATA REALTIME CURRENT POSTURE
# =====================================================

def update_current(pitch, status):

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()


        cursor.execute("""
            UPDATE current_posture
            SET pitch=%s,
                status=%s,
                timestamp=CONVERT_TZ(NOW(), '+00:00', '+07:00')
            WHERE id=1
        """, (
            pitch,
            status
        ))


        print("✅ CURRENT UPDATED")


    except Exception as e:

        print("❌ UPDATE CURRENT ERROR :", e)

        raise e


    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()



# =====================================================
# SIMPAN LOG
# Tidak Ergonomis  = langsung simpan
# Ergonomis        = setiap 5 menit
# =====================================================

def insert_log(pitch, status):

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()


        save_log = False



        if status == "Tidak Ergonomis":

            save_log = True



        elif status == "Ergonomis":


            cursor.execute("""
                SELECT timestamp
                FROM posture_logs
                ORDER BY id DESC
                LIMIT 1
            """)


            last_log = cursor.fetchone()



            if last_log is None:

                save_log = True


            else:

                last_time = last_log["timestamp"]


                if datetime.now() - last_time >= timedelta(minutes=5):

                    save_log = True




        if save_log:


            cursor.execute("""
                INSERT INTO posture_logs
                (
                    pitch,
                    status,
                    timestamp
                )

                VALUES
                (
                    %s,
                    %s,
                    '+00:00', '+07:00'
                )

            """, (
                pitch,
                status
            ))


            print("✅ LOG INSERTED")


        else:

            print("ℹ️ LOG SKIPPED")



    except Exception as e:

        print("❌ INSERT LOG ERROR :", e)

        raise e



    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()



# =====================================================
# FUNGSI UTAMA
# =====================================================

def save_prediction(pitch, status):

    print("SAVE PREDICTION START")


    try:

        update_current(
            pitch,
            status
        )


        insert_log(
            pitch,
            status
        )


        print("SAVE PREDICTION DONE")


    except Exception as e:

        print("❌ SAVE PREDICTION ERROR :", e)

        raise e