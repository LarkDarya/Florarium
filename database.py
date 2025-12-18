from peewee import PostgresqlDatabase
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.getenv('DB_NAME', 'florarium_db')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', 5432))

# Создание объекта базы данных
db = PostgresqlDatabase(
    DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    encoding='utf8'  # Явное указание кодировки
)

def connect_db():
    """Подключение к базе данных"""
    if db.is_closed():
        try:
            db.connect()
            print("[OK] Подключение к базе данных установлено")
            return True
        except Exception as e:
            print(f"[ERROR] Ошибка подключения к БД: {e}")
            return False
    else:
        print("[INFO] Соединение с БД уже установлено")
        return True

def close_db():
    """Закрытие соединения с базой данных"""
    if not db.is_closed():
        db.close()
        print("[OK] Соединение с БД закрыто")
