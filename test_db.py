from database import get_connection

try:
    conn = get_connection()
    print("✅ Berhasil terhubung ke database!")
    conn.close()

except Exception as e:
    print("❌ Gagal koneksi:", e)