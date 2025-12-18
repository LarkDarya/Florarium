from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                               QLabel, QLineEdit, QCheckBox,
                               QPushButton, QSpacerItem, QSizePolicy)
from PySide6.QtCore import Qt

class LoginDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.user = None
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Вход в систему")
        self.setFixedSize(350, 400)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Заголовок
        title_label = QLabel("АВТОРИЗАЦИЯ")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #485935;
                padding: 5px;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        main_layout.addSpacing(5)

        # Поле "Логин"
        login_layout = QVBoxLayout()
        login_label = QLabel("Логин:")
        login_label.setStyleSheet("font-weight: bold; color: #485935;")
        login_layout.addWidget(login_label)

        self.login_edit = QLineEdit()
        self.login_edit.setPlaceholderText("Введите ваш логин")
        self.login_edit.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #93a267;
                border-radius: 5px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #485935;
            }
        """)
        login_layout.addWidget(self.login_edit)
        main_layout.addLayout(login_layout)

        # Поле "Пароль"
        password_layout = QVBoxLayout()
        password_label = QLabel("Пароль:")
        password_label.setStyleSheet("font-weight: bold; color: #485935;")
        password_layout.addWidget(password_label)

        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Введите ваш пароль")
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #93a267;
                border-radius: 5px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #485935;
            }
        """)
        password_layout.addWidget(self.password_edit)
        main_layout.addLayout(password_layout)

        # Чекбокс "Показать пароль"
        self.show_password_check = QCheckBox("Показать пароль")
        self.show_password_check.setStyleSheet("""
            QCheckBox {
                color: #485935;
                font-size: 13px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #93a267;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                background-color: #93a267;
                border: 2px solid #485935;
            }
        """)
        self.show_password_check.stateChanged.connect(self.toggle_password_visibility)
        main_layout.addWidget(self.show_password_check)

        # Спейсер
        vertical_spacer = QSpacerItem(23, 40, QSizePolicy.Fixed, QSizePolicy.Fixed)
        main_layout.addItem(vertical_spacer)

        # Кнопки ОК и Отмена
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        # Кнопка "ОК"
        ok_button = QPushButton("ОК")
        ok_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(147, 162, 103, 0.9);
                color: #f8efda;
                border: none;
                border-radius: 15px;
                padding: 10px 20px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: rgba(113, 128, 78, 1);
            }
            QPushButton:pressed {
                background-color: rgba(94, 108, 65, 1);
            }
        """)
        ok_button.clicked.connect(self.process_login)
        buttons_layout.addWidget(ok_button)

        # Кнопка "Отмена"
        cancel_button = QPushButton("Отмена")
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(231, 76, 60, 0.8);
                color: white;
                border: none;
                border-radius: 15px;
                padding: 10px 20px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: rgba(192, 57, 43, 0.9);
            }
            QPushButton:pressed {
                background-color: rgba(169, 50, 38, 1);
            }
        """)
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_button)

        main_layout.addLayout(buttons_layout)
        self.setLayout(main_layout)

        # Центрируем окно
        self.move(
            self.parent.x() + (self.parent.width() - self.width()) // 2,
            self.parent.y() + (self.parent.height() - self.height()) // 2
        )

    def toggle_password_visibility(self, state):
        """Показать/скрыть пароль"""
        if state == 2:  # Qt.CheckState.Checked == 2
            self.password_edit.setEchoMode(QLineEdit.Normal)
        else:
            self.password_edit.setEchoMode(QLineEdit.Password)

    def process_login(self):
        """Обработка входа"""
        login = self.login_edit.text()
        password = self.password_edit.text()

        if not login or not password:
            self.parent.show_simple_message("Ошибка", "Пожалуйста, заполните все поля!", "error")
            return

        try:
            user = self.parent.service.authenticate_user(login, password)

            if user:
                self.user = user
                self.accept()
            else:
                self.parent.show_simple_message("Ошибка", "Неверный логин или пароль!", "error")

        except Exception as e:
            print(f"Ошибка при входе: {e}")
            import traceback
            traceback.print_exc()
            self.parent.show_simple_message("Ошибка", f"Ошибка при входе: {str(e)}", "error")

    def get_user(self):
        """Возвращает аутентифицированного пользователя"""
        return self.user
