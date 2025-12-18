from PySide6.QtWidgets import (QWidget, QLabel, QPushButton, QDialog,
                               QVBoxLayout, QHBoxLayout, QLineEdit,
                               QCheckBox, QMessageBox, QSpacerItem,
                               QSizePolicy, QDateEdit)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QPixmap
import sys

# Импортируем модули
from login_window import LoginDialog
from register_window import RegisterDialog
from service import FlorariumService

class WelcomeDialog(QDialog):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.user = user
        self.setup_ui()

    def setup_ui(self):
        # Определяем данные в зависимости от роли
        if self.user.role == 'admin':
            icon = "🌿"
            title = f"Добро пожаловать, {self.user.first_name or self.user.username}!"
            subtitle = "Панель администратора"
            message = "Управляйте растениями, фотографиями\nи другими данными системы Флорариум."
            button_text = "Начать работу"
        else:
            icon = "🌱"
            title = f"Рады видеть вас, {self.user.first_name or self.user.username}!"
            subtitle = "Ваш персональный флорариум"
            message = "Изучайте растения, создавайте коллекции\nи следите за своими зелеными питомцами."
            button_text = "Вперед!"

        self.setWindowTitle("Добро пожаловать")
        self.setFixedSize(400, 350)
        self.setStyleSheet("""
            QDialog {
                background-color: #FBFBFB;
                border: 2px solid rgba(147, 162, 103, 0.9);
                border-radius: 15px;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(25, 25, 25, 25)

        # Главная иконка
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("""
            QLabel {
                font-size: 48px;
                margin: 10px;
            }
        """)
        icon_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(icon_label)

        # Заголовок
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #485935;
                margin: 5px;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Подзаголовок
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #93a267;
                margin: 3px;
            }
        """)
        subtitle_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle_label)

        # Разделительная линия
        line = QWidget()
        line.setFixedHeight(1)
        line.setStyleSheet("background-color: rgba(147, 162, 103, 0.3); margin: 10px 0;")
        main_layout.addWidget(line)

        # Сообщение
        message_label = QLabel(message)
        message_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: #666;
                margin: 10px;
                line-height: 1.4;
            }
        """)
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setWordWrap(True)
        main_layout.addWidget(message_label)

        # Спейсер
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Кнопка
        buttons_layout = QHBoxLayout()
        ok_button = QPushButton(button_text)
        ok_button.setFixedWidth(150)
        ok_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(147, 162, 103, 0.9);
                color: #f8efda;
                border: none;
                border-radius: 15px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgba(113, 128, 78, 1);
            }
            QPushButton:pressed {
                background-color: rgba(94, 108, 65, 1);
            }
        """)
        ok_button.clicked.connect(self.accept)
        buttons_layout.addStretch()
        buttons_layout.addWidget(ok_button)
        buttons_layout.addStretch()

        main_layout.addLayout(buttons_layout)
        self.setLayout(main_layout)

        # Центрируем диалог
        parent = self.parent()
        if parent:
            self.move(
                parent.x() + (parent.width() - self.width()) // 2,
                parent.y() + (parent.height() - self.height()) // 2
            )


class SimpleMessageDialog(QDialog):
    def __init__(self, parent, title, message, msg_type="info"):
        super().__init__(parent)
        self.setup_ui(title, message, msg_type)

    def setup_ui(self, title, message, msg_type):
        self.setWindowTitle(title)
        self.setFixedSize(400, 250)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Сообщение
        message_label = QLabel(message)
        message_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #2c3e50;
                padding: 10px;
            }
        """)
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setWordWrap(True)
        main_layout.addWidget(message_label)

        # Иконка в зависимости от типа
        if msg_type == "error":
            icon_label = QLabel("✗")
            icon_label.setStyleSheet("""
                QLabel {
                    font-size: 32px;
                    color: #c0392b;
                    font-weight: bold;
                }
            """)
            button_type = "secondary"
        elif msg_type == "warning":
            icon_label = QLabel("!")
            icon_label.setStyleSheet("""
                QLabel {
                    font-size: 32px;
                    color: #f39c12;
                    font-weight: bold;
                }
            """)
            button_type = "warning"
        else:  # info
            icon_label = QLabel("✓")
            icon_label.setStyleSheet("""
                QLabel {
                    font-size: 32px;
                    color: #27ae60;
                    font-weight: bold;
                }
            """)
            button_type = "primary"

        icon_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(icon_label)

        # Спейсер
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Кнопка OK
        buttons_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        if button_type == "primary":
            ok_button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(147, 162, 103, 0.9);
                    color: #f8efda;
                    border: none;
                    border-radius: 15px;
                    padding: 10px 20px;
                    font-weight: bold;
                }
            """)
        elif button_type == "secondary":
            ok_button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(231, 76, 60, 0.8);
                    color: white;
                    border: none;
                    border-radius: 15px;
                    padding: 10px 20px;
                    font-weight: bold;
                }
            """)
        elif button_type == "warning":
            ok_button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(243, 156, 18, 0.8);
                    color: white;
                    border: none;
                    border-radius: 15px;
                    padding: 10px 20px;
                    font-weight: bold;
                }
            """)

        ok_button.clicked.connect(self.accept)
        buttons_layout.addWidget(ok_button)
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

class FlorariumWidget(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.service = FlorariumService()
        self.setup_ui()
        self.setup_connections()
        self.center_window()

    def center_window(self):
        """Центрировать окно на экране"""
        from PySide6.QtWidgets import QApplication
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())

    def setup_ui(self):
        # Настройка главного окна
        self.setGeometry(0, 0, 480, 730)
        self.setWindowTitle("Florarium")
        self.setStyleSheet("""
            QWidget {
                background: #FBFBFB;
                border-radius: 10px;
                font-family: 'Cambria Math';
                font-size: 14px;
            }
        """)

        # Метка "Добро пожаловать во"
        self.label_4 = QLabel("Добро пожаловать во", self)
        self.label_4.setGeometry(0, 0, 481, 91)
        self.label_4.setStyleSheet("""
            QLabel {
                background-color: transparent;
                color: #f8efda;
                font-size: 20px;
                font-weight: bold;
                font-family: "Times New Roman", serif;
                padding: 10px;
            }
        """)
        self.label_4.setAlignment(Qt.AlignCenter)

        # Метка "Флорариум"
        self.label_3 = QLabel("Флорариум", self)
        self.label_3.setGeometry(0, 50, 481, 91)
        self.label_3.setStyleSheet("""
            QLabel {
                background-color: transparent;
                color: #f8efda;
                font-size: 40px;
                font-weight: bold;
                font-family: "Times New Roman", serif;
                font-style: italic;
                padding: 10px;
                letter-spacing: 3px;
            }
        """)
        self.label_3.setAlignment(Qt.AlignCenter)

        # Метка с эмодзи
        self.label_5 = QLabel("🌱", self)
        self.label_5.setGeometry(0, 130, 481, 71)
        self.label_5.setStyleSheet("""
            QLabel {
                background-color: transparent;
                color: #f8efda;
                font-size: 40px;
                font-weight: bold;
                font-family: "Times New Roman", serif;
                padding: 10px;
            }
        """)
        self.label_5.setAlignment(Qt.AlignCenter)

        # Кнопка "Вход"
        self.pushButton = QPushButton("Вход", self)
        self.pushButton.setGeometry(20, 200, 200, 51)
        self.pushButton.setStyleSheet("""
            QPushButton {
                background-color: rgba(147, 162, 103, 1);
                color: #f8efda;
                border: none;
                border-radius: 25px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(113, 128, 78, 1);
                color: #f8efda;
                box-shadow: 0 4px 15px rgba(147, 162, 103, 0.4);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background-color: rgba(94, 108, 65, 1);
                color: #f8efda;
                transform: translateY(1px);
                box-shadow: 0 2px 8px rgba(147, 162, 103, 0.3);
                padding: 13px 23px 11px 25px;
            }
        """)

        # Кнопка "Выход"
        self.pushButton_3 = QPushButton("Выход", self)
        self.pushButton_3.setGeometry(260, 200, 200, 51)
        self.pushButton_3.setStyleSheet("""
            QPushButton {
                background-color: rgba(147, 162, 103, 1);
                color: #f8efda;
                border: none;
                border-radius: 25px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(113, 128, 78, 1);
                color: #f8efda;
                box-shadow: 0 4px 15px rgba(147, 162, 103, 0.4);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background-color: rgba(94, 108, 65, 1);
                color: #f8efda;
                transform: translateY(1px);
                box-shadow: 0 2px 8px rgba(147, 162, 103, 0.3);
                padding: 13px 23px 11px 25px;
            }
        """)

        # Кнопка "Регистрация"
        self.pushButton_2 = QPushButton("Регистрация", self)
        self.pushButton_2.setGeometry(140, 270, 200, 51)
        self.pushButton_2.setStyleSheet("""
            QPushButton {
                background-color: rgba(147, 162, 103, 1);
                color: #f8efda;
                border: none;
                border-radius: 25px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: bold;
                transition: background-color 0.3s ease,
                            transform 0.2s ease,
                            box-shadow 0.3s ease;
            }
            QPushButton:hover {
                background-color: rgba(113, 128, 78, 1);
                color: #f8efda;
                box-shadow: 0 4px 15px rgba(147, 162, 103, 0.4);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background-color: rgba(94, 108, 65, 1);
                color: #f8efda;
                transform: translateY(1px);
                box-shadow: 0 2px 8px rgba(147, 162, 103, 0.3);
                padding: 13px 23px 11px 25px;
            }
        """)

    def setup_connections(self):
        """Подключение обработчиков событий"""
        self.pushButton_3.clicked.connect(self.close)
        self.pushButton.clicked.connect(self.on_login_clicked)
        self.pushButton_2.clicked.connect(self.on_register_clicked)

    def on_login_clicked(self):
        """Обработчик нажатия кнопки 'Вход'"""
        self.open_login_window()

    def open_login_window(self):
        """Открывает окно входа"""
        login_dialog = LoginDialog(self)
        if login_dialog.exec():
            user = login_dialog.get_user()
            if user:
                self.open_user_window(user)

    def open_user_window(self, user):
        """Открытие окна в зависимости от роли пользователя"""
        try:
            # Показываем приветственное сообщение
            welcome_dialog = WelcomeDialog(self, user)
            welcome_dialog.exec()

            # Закрываем текущее окно (окно входа)
            self.hide()

            if user.role == 'admin':
                from admin_window import AdminWindow
                self.admin_window = AdminWindow(user.id)

                def custom_admin_close_event(event):
                    self.admin_window.closeEvent = lambda e: super(type(self.admin_window), self.admin_window).closeEvent(e)
                    event.accept()
                    self.show_main_window()

                self.admin_window.closeEvent = custom_admin_close_event
                self.admin_window.show()

            else:
                from user_window import UserWindow
                self.user_window = UserWindow(user.id)

                def custom_user_close_event(event):
                    from PySide6.QtWidgets import QWidget
                    QWidget.closeEvent(self.user_window, event)
                    self.show_main_window()

                self.user_window.closeEvent = custom_user_close_event
                self.user_window.show()

        except Exception as e:
            print(f"Ошибка при открытии окна: {e}")
            import traceback
            traceback.print_exc()
            self.show_simple_message("Ошибка",
                                   f"Не удалось открыть приложение: {str(e)}",
                                   "error")
            self.show()

    def show_main_window(self):
        """Показать главное окно"""
        self.show()
        self.raise_()
        self.activateWindow()

    def on_register_clicked(self):
        """Обработчик нажатия кнопки 'Регистрация'"""
        self.open_register_window()

    def open_register_window(self):
        """Открывает окно регистрации"""
        register_dialog = RegisterDialog(self)
        register_dialog.exec()

    def show_simple_message(self, title, message, msg_type="info"):
        """Показать стилизованное сообщение"""
        from app.welcome_dialog import SimpleMessageDialog
        dialog = SimpleMessageDialog(self, title, message, msg_type)
        dialog.exec()

    def set_background_image(self, image_path):
        """Добавляет фоновое изображение"""
        background_label = QLabel(self)
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            background_label.setPixmap(pixmap.scaled(
                self.size(),
                Qt.IgnoreAspectRatio,
                Qt.SmoothTransformation
            ))
            background_label.lower()
            background_label.setGeometry(0, 0, self.width(), self.height())
