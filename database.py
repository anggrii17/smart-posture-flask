# =====================================================
# KONEKSI DATABASE MYSQL
# =====================================================

import pymysql
from datetime import datetime, timedelta
from config import *


print("==========================")
print("DATABASE CONFIG")
print("HOST :", DB_HOST)
print("PORT :", DB_PORT)
print("USER :", DB_USER)
print("DB   :", DB_NAME)
print("==========================")


def get_connection():

    try:

        conn = pymysql.connect(
            host=DB_HOST,
            port=int(DB_PORT),
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

        print("✅ MYSQL CONNECTED")

        return conn


    except Exception as e:

        print("❌ MYSQL CONNECTION ERROR :", e)

        raise e



# =====================================================
# UPDATE REALTIME CURRENT POSTURE
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
        """, (
            pitch,
            status
        ))


        print("✅ CURRENT UPDATED")


    except Exception as e:

        print("❌ UPDATE CURRENT ERROR :", e)

        raise e


    finally:

        cursor.close()
        conn.close()



# =====================================================
# INSERT LOG
# Tidak Ergonomis = langsung simpan
# Ergonomis = interval 5 menit
# =====================================================

def insert_log(pitch, status):

    conn = get_connection()
    cursor = conn.cursor()


    try:

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
                    NOW()
                )

            """,(
                pitch,
                status
            ))


            print("✅ LOG INSERTED")

        else:

            print("ℹ️ LOG SKIPPED (interval 5 menit)")



    except Exception as e:

        print("❌ INSERT LOG ERROR :", e)

        raise e



    finally:

        cursor.close()
        conn.close()



# =====================================================
# FUNGSI UTAMA
# =====================================================

def save_prediction(pitch, status):


    print("SAVE PREDICTION START")


    update_current(
        pitch,
        status
    )


    insert_log(
        pitch,
        status
    )


    print("SAVE PREDICTION DONE")