# main.py
import sys
from PySide6.QtWidgets import QApplication, QMessageBox

from start_window import FlorariumWidget
from models import create_tables
from database import connect_db
from service import FlorariumService

class FlorariumApp:
    def __init__(self):
        # Инициализация базы данных
        try:
            connect_db()
            create_tables()
            print("База данных подключена успешно!")

            # Создание тестового администратора если его нет
            self.create_default_admin()

        except Exception as e:
            print(f"Ошибка подключения к БД: {e}")
            QMessageBox.critical(None, "Ошибка",
                               f"Не удалось подключиться к базе данных:\n{str(e)}")
            sys.exit(1)

    def create_default_admin(self):
        """Создает тестового администратора если его нет"""
        try:
            service = FlorariumService()

            # Проверяем, есть ли уже администраторы
            admin_exists = service.User.select().where(
                service.User.role == 'admin'
            ).exists()

            if not admin_exists:
                # Создаем тестового администратора
                service.create_user(
                    username="admin",
                    password="admin123",
                    email="admin@florarium.com",
                    first_name="Администратор",
                    last_name="Системы",
                    role="admin"
                )
                print("Создан тестовый администратор: admin / admin123")
        except Exception as e:
            print(f"Ошибка при создании администратора: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Инициализируем приложение
    florarium_app = FlorariumApp()

    # Создаем главное окно
    window = FlorariumWidget(app)

    # Добавляем фоновую картинку
    window.set_background_image("2.jpg")

    window.show()
    sys.exit(app.exec())
