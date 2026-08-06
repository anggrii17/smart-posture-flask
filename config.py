import os

DB_HOST = os.getenv("DB_HOST", "gondola.proxy.rlwy.net")
DB_PORT = int(os.getenv("DB_PORT", 13719))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "iFiXeifdjSNTvPzxCeGhPHjsexBqQwae")
DB_NAME = os.getenv("DB_NAME", "railway")