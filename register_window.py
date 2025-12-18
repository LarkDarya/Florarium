from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                               QLabel, QLineEdit, QPushButton,
                               QDateEdit, QMessageBox)
from PySide6.QtCore import Qt, QDate

class RegisterDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Регистрация")
        self.setFixedSize(400, 750)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Заголовок
        title_label = QLabel("РЕГИСТРАЦИЯ")
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

        # Поле "Имя"
        name_layout = QVBoxLayout()
        name_label = QLabel("Имя:")
        name_label.setStyleSheet("font-weight: bold; color: #485935;")
        name_layout.addWidget(name_label)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Введите ваше имя")
        self.name_edit.setStyleSheet("""
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
        name_layout.addWidget(self.name_edit)
        main_layout.addLayout(name_layout)

        # Поле "Фамилия"
        surname_layout = QVBoxLayout()
        surname_label = QLabel("Фамилия:")
        surname_label.setStyleSheet("font-weight: bold; color: #485935;")
        surname_layout.addWidget(surname_label)

        self.surname_edit = QLineEdit()
        self.surname_edit.setPlaceholderText("Введите вашу фамилию")
        self.surname_edit.setStyleSheet("""
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
        surname_layout.addWidget(self.surname_edit)
        main_layout.addLayout(surname_layout)

        # Поле "Email"
        email_layout = QVBoxLayout()
        email_label = QLabel("Email:")
        email_label.setStyleSheet("font-weight: bold; color: #485935;")
        email_layout.addWidget(email_label)

        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("example@mail.com")
        self.email_edit.setStyleSheet("""
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
        email_layout.addWidget(self.email_edit)
        main_layout.addLayout(email_layout)

        # Поле "Логин"
        login_layout = QVBoxLayout()
        login_label = QLabel("Логин:")
        login_label.setStyleSheet("font-weight: bold; color: #485935;")
        login_layout.addWidget(login_label)

        self.login_edit = QLineEdit()
        self.login_edit.setPlaceholderText("Придумайте логин")
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
        self.password_edit.setPlaceholderText("Придумайте пароль")
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

        # Поле "Подтверждение пароля"
        confirm_password_layout = QVBoxLayout()
        confirm_password_label = QLabel("Подтвердите пароль:")
        confirm_password_label.setStyleSheet("font-weight: bold; color: #485935;")
        confirm_password_layout.addWidget(confirm_password_label)

        self.confirm_password_edit = QLineEdit()
        self.confirm_password_edit.setPlaceholderText("Повторите пароль")
        self.confirm_password_edit.setEchoMode(QLineEdit.Password)
        self.confirm_password_edit.setStyleSheet("""
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
        confirm_password_layout.addWidget(self.confirm_password_edit)
        main_layout.addLayout(confirm_password_layout)

        # Поле "Дата рождения"
        age_layout = QVBoxLayout()
        age_label = QLabel("Дата рождения:")
        age_label.setStyleSheet("font-weight: bold; color: #485935;")
        age_layout.addWidget(age_label)

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate().addYears(-18))
        self.date_edit.setMaximumDate(QDate.currentDate())
        self.date_edit.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                border: 2px solid #93a267;
                border-radius: 5px;
                font-size: 14px;
            }
            QDateEdit:focus {
                border: 2px solid #485935;
            }
        """)
        age_layout.addWidget(self.date_edit)
        main_layout.addLayout(age_layout)

        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        # Кнопка "Зарегистрироваться"
        register_button = QPushButton("Зарегистрироваться")
        register_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(147, 162, 103, 0.9);
                color: #f8efda;
                border: none;
                border-radius: 15px;
                padding: 10px 20px;
                font-weight: bold;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: rgba(113, 128, 78, 1);
            }
            QPushButton:pressed {
                background-color: rgba(94, 108, 65, 1);
            }
        """)
        register_button.clicked.connect(self.process_registration)
        buttons_layout.addWidget(register_button)

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

    def process_registration(self):
        """Обработка данных регистрации"""
        name = self.name_edit.text()
        surname = self.surname_edit.text()
        email = self.email_edit.text()
        login = self.login_edit.text()
        password = self.password_edit.text()
        confirm_password = self.confirm_password_edit.text()
        birth_date = self.date_edit.date()

        errors = []

        if not name.strip():
            errors.append("Введите имя")
        if not surname.strip():
            errors.append("Введите фамилию")
        if not email.strip():
            errors.append("Введите email")
        elif "@" not in email or "." not in email:
            errors.append("Введите корректный email")
        if not login.strip():
            errors.append("Введите логин")
        elif len(login) < 3:
            errors.append("Логин должен быть не менее 3 символов")
        if not password:
            errors.append("Введите пароль")
        elif len(password) < 6:
            errors.append("Пароль должен быть не менее 6 символов")
        if password != confirm_password:
            errors.append("Пароли не совпадают")

        # Проверка возраста
        age = birth_date.daysTo(QDate.currentDate()) // 365
        if age < 5:
            errors.append("Регистрация доступна с 5 лет")

        if errors:
            error_message = "Ошибки регистрации:\n• " + "\n• ".join(errors)
            self.parent.show_simple_message("Ошибка регистрации", error_message, "error")
            return

        try:
            user_id = self.parent.service.create_user(
                username=login,
                password=password,
                email=email,
                first_name=name,
                last_name=surname,
                birth_date=birth_date.toString("yyyy-MM-dd")
            )

            if user_id:
                self.parent.show_simple_message("Успешно",
                                       f"Регистрация прошла успешно!\nДобро пожаловать, {name} {surname}!",
                                       "info")
                self.accept()
            else:
                self.parent.show_simple_message("Ошибка",
                                       "Пользователь с таким логином или email уже существует",
                                       "error")

        except Exception as e:
            self.parent.show_simple_message("Ошибка",
                                   f"Произошла ошибка при сохранении данных: {str(e)}",
                                   "error")
