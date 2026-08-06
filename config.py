import os

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

print("======================")
print("DB_HOST =", DB_HOST)
print("DB_PORT =", DB_PORT)
print("DB_USER =", DB_USER)
print("DB_NAME =", DB_NAME)
print("======================")