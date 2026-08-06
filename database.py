# =====================================================
# KONEKSI DATABASE MYSQL
# =====================================================

import pymysql
from datetime import datetime, timedelta
from config import *


def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )


# =====================================================
# UPDATE DATA REALTIME CURRENT POSTURE
# =====================================================

def update_current(pitch, status):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            UPDATE current_posture
            SET pitch=%s,
                status=%s,
                timestamp=NOW()
            WHERE id=1
        """, (pitch, status))

    finally:
        cursor.close()
        conn.close()



# =====================================================
# SIMPAN LOG DENGAN ATURAN
# Tidak Ergonomis  -> langsung simpan
# Ergonomis        -> simpan setiap 5 menit
# =====================================================

def insert_log(pitch, status):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        save_log = False


        # Jika tidak ergonomis langsung masuk log
        if status == "Tidak Ergonomis":

            save_log = True


        # Jika ergonomis cek interval 5 menit
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
                (pitch,status,timestamp)
                VALUES(%s,%s,NOW())
            """, (pitch, status))


    finally:
        cursor.close()
        conn.close()



# =====================================================
# FUNGSI UTAMA (PENGGANTI save_prediction)
# =====================================================

def save_prediction(pitch, status):

    # selalu update realtime
    update_current(
        pitch,
        status
    )


    # simpan log sesuai aturan
    insert_log(
        pitch,
        status
    )