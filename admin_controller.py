# windows/admin_controller.py
from PySide6.QtWidgets import (QMessageBox, QTableWidgetItem, QDialog,
                               QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                               QTextEdit, QSpinBox, QPushButton, QFormLayout,
                               QComboBox, QFileDialog, QCheckBox, QSpacerItem,
                               QSizePolicy, QWidget, QHeaderView)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QBrush, QColor
from datetime import datetime
import os
import sys

class AdminController:
    def __init__(self, service, window):
        self.service = service
        self.window = window
        self.setup_connections()

    def setup_connections(self):
        # Подключение сигналов для пользователей
        self.window.btn_add_user.clicked.connect(self.add_user)
        self.window.btn_edit_user.clicked.connect(self.edit_user)
        self.window.btn_delete_user.clicked.connect(self.delete_user)

        # Кнопки семейств растений
        self.window.btn_add_family.clicked.connect(self.add_family)
        self.window.btn_edit_family.clicked.connect(self.edit_family)
        self.window.btn_delete_family.clicked.connect(self.delete_family)

        # Кнопки руководств по уходу
        self.window.btn_add_care_guide.clicked.connect(self.add_care_guide)
        self.window.btn_edit_care_guide.clicked.connect(self.edit_care_guide)
        self.window.btn_delete_care_guide.clicked.connect(self.delete_care_guide)

        # Кнопки местоположений
        self.window.btn_add_location.clicked.connect(self.add_location)
        self.window.btn_edit_location.clicked.connect(self.edit_location)
        self.window.btn_delete_location.clicked.connect(self.delete_location)

        # Кнопки фотографий
        self.window.btn_add_photo.clicked.connect(self.add_photo)
        self.window.btn_edit_photo.clicked.connect(self.edit_photo)
        self.window.btn_delete_photo.clicked.connect(self.delete_photo)

        # Кнопки растений
        self.window.btn_add_plant.clicked.connect(self.add_plant)
        self.window.btn_edit_plant.clicked.connect(self.edit_plant)
        self.window.btn_delete_plant.clicked.connect(self.delete_plant)

        # Кнопки вредителей
        self.window.btn_add_pest.clicked.connect(self.add_pest)
        self.window.btn_edit_pest.clicked.connect(self.edit_pest)
        self.window.btn_delete_pest.clicked.connect(self.delete_pest)

        # Кнопки болезней
        self.window.btn_add_disease.clicked.connect(self.add_disease)
        self.window.btn_edit_disease.clicked.connect(self.edit_disease)
        self.window.btn_delete_disease.clicked.connect(self.delete_disease)

        # Кнопки связей
        self.window.btn_add_plant_family.clicked.connect(self.add_plant_family_relation)
        self.window.btn_delete_plant_family.clicked.connect(self.delete_plant_family_relation)
        self.window.btn_add_plant_pest.clicked.connect(self.add_plant_pest_relation)
        self.window.btn_delete_plant_pest.clicked.connect(self.delete_plant_pest_relation)
        self.window.btn_add_plant_disease.clicked.connect(self.add_plant_disease_relation)
        self.window.btn_delete_plant_disease.clicked.connect(self.delete_plant_disease_relation)

        # Кнопки экспорта
        self.window.btn_export_users.clicked.connect(self.export_users)
        self.window.btn_export_families.clicked.connect(self.export_families)
        self.window.btn_export_care_guides.clicked.connect(self.export_care_guides)
        self.window.btn_export_locations.clicked.connect(self.export_locations)
        self.window.btn_export_photos.clicked.connect(self.export_photos)
        self.window.btn_export_plants.clicked.connect(self.export_plants)
        self.window.btn_export_pests.clicked.connect(self.export_pests)
        self.window.btn_export_diseases.clicked.connect(self.export_diseases)

        self.load_all_data()

    def load_all_data(self):
        """Загрузка всех данных"""
        self.load_families()
        self.load_users()
        self.load_care_guides()
        self.load_locations()
        self.load_photos()
        self.load_plants()
        self.load_pests()
        self.load_diseases()
        self.load_plant_family_relations()
        self.load_plant_pest_relations()
        self.load_plant_disease_relations()

    def reset_sequence(self, model_class):
        """
        Сброс последовательности автоинкремента для указанной модели
        """
        try:
            # Получаем текущий максимальный ID через ORM
            max_record = model_class.select().order_by(model_class.id.desc()).first()

            if max_record:
                print(f"Максимальный ID для {model_class.__name__}: {max_record.id}")
                return max_record.id + 1
            else:
                print(f"Таблица {model_class.__name__} пуста, начинаем с 1")
                return 1

        except Exception as e:
            print(f"Ошибка при получении максимального ID: {str(e)}")
            return 1

    def create_styled_button(self, text, style="primary"):
        """Создание стилизованной кнопки"""
        button = QPushButton(text)
        if style == "primary":
            button.setStyleSheet("""
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
        elif style == "secondary":
            button.setStyleSheet("""
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
        elif style == "warning":
            button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(243, 156, 18, 0.8);
                    color: white;
                    border: none;
                    border-radius: 15px;
                    padding: 10px 20px;
                    font-weight: bold;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: rgba(230, 126, 34, 0.9);
                }
                QPushButton:pressed {
                    background-color: rgba(211, 84, 0, 1);
                }
            """)
        return button

    def create_styled_line_edit(self, placeholder=""):
        """Создание стилизованного поля ввода"""
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        line_edit.setStyleSheet("""
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
        return line_edit

    def create_styled_text_edit(self):
        """Создание стилизованного текстового поля"""
        text_edit = QTextEdit()
        text_edit.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                border: 2px solid #93a267;
                border-radius: 5px;
                font-size: 14px;
                min-height: 80px;
            }
            QTextEdit:focus {
                border: 2px solid #485935;
            }
        """)
        return text_edit

    def create_styled_spinbox(self):
        """Создание стилизованного спинбокса"""
        spinbox = QSpinBox()
        spinbox.setStyleSheet("""
            QSpinBox {
                padding: 8px;
                border: 2px solid #93a267;
                border-radius: 5px;
                font-size: 14px;
            }
            QSpinBox:focus {
                border: 2px solid #485935;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 20px;
                border: none;
                background-color: #93a267;
                border-radius: 2px;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #485935;
            }
        """)
        return spinbox

    def create_styled_combobox(self):
        """Создание стилизованного комбобокса"""
        combo = QComboBox()
        combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #93a267;
                border-radius: 5px;
                font-size: 14px;
                background-color: white;
            }
            QComboBox:focus {
                border: 2px solid #485935;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border: none;
            }
        """)
        return combo

    def create_styled_dialog(self, title, width=400, height=400):
        """Создание стилизованного диалогового окна"""
        dialog = QDialog(self.window)
        dialog.setWindowTitle(title)
        dialog.setFixedSize(width, height)

        # Основной layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Заголовок
        title_label = QLabel(title.upper())
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
        main_layout.addSpacing(10)

        return dialog, main_layout

    def show_info_message(self, title, message):
        """Показать информационное сообщение"""
        dialog, main_layout = self.create_styled_dialog(title, 400, 250)

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

        # Иконка
        icon_label = QLabel("✓")
        icon_label.setStyleSheet("""
            QLabel {
                font-size: 32px;
                color: #27ae60;
                font-weight: bold;
            }
        """)
        icon_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(icon_label)

        # Спейсер
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Кнопка OK
        buttons_layout = QHBoxLayout()
        ok_button = self.create_styled_button("OK", "primary")
        buttons_layout.addWidget(ok_button)
        main_layout.addLayout(buttons_layout)

        ok_button.clicked.connect(dialog.accept)

        dialog.setLayout(main_layout)
        dialog.exec()

    def show_error_message(self, title, message):
        """Показать сообщение об ошибке"""
        dialog, main_layout = self.create_styled_dialog(title, 400, 250)

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

        # Иконка
        icon_label = QLabel("✗")
        icon_label.setStyleSheet("""
            QLabel {
                font-size: 32px;
                color: #c0392b;
                font-weight: bold;
            }
        """)
        icon_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(icon_label)

        # Спейсер
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Кнопка OK
        buttons_layout = QHBoxLayout()
        ok_button = self.create_styled_button("OK", "secondary")
        buttons_layout.addWidget(ok_button)
        main_layout.addLayout(buttons_layout)

        ok_button.clicked.connect(dialog.accept)

        dialog.setLayout(main_layout)
        dialog.exec()

    def show_warning_message(self, title, message):
        """Показать предупреждение"""
        dialog, main_layout = self.create_styled_dialog(title, 400, 250)

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

        # Иконка
        icon_label = QLabel("!")
        icon_label.setStyleSheet("""
            QLabel {
                font-size: 32px;
                color: #f39c12;
                font-weight: bold;
            }
        """)
        icon_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(icon_label)

        # Спейсер
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Кнопка OK
        buttons_layout = QHBoxLayout()
        ok_button = self.create_styled_button("OK", "warning")
        buttons_layout.addWidget(ok_button)
        main_layout.addLayout(buttons_layout)

        ok_button.clicked.connect(dialog.accept)

        dialog.setLayout(main_layout)
        dialog.exec()

    def show_confirmation_dialog(self, title, message):
        """Показать диалог подтверждения"""
        dialog, main_layout = self.create_styled_dialog(title, 400, 250)
        dialog.result = False

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

        # Иконка
        icon_label = QLabel("?")
        icon_label.setStyleSheet("""
            QLabel {
                font-size: 32px;
                color: #3498db;
                font-weight: bold;
            }
        """)
        icon_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(icon_label)

        # Спейсер
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        yes_button = self.create_styled_button("Да", "primary")
        no_button = self.create_styled_button("Нет", "secondary")

        def on_yes():
            dialog.result = True
            dialog.accept()

        def on_no():
            dialog.result = False
            dialog.accept()

        yes_button.clicked.connect(on_yes)
        no_button.clicked.connect(on_no)

        buttons_layout.addWidget(yes_button)
        buttons_layout.addWidget(no_button)
        main_layout.addLayout(buttons_layout)

        dialog.setLayout(main_layout)
        dialog.exec()

        return dialog.result

    def add_user(self):
        """Добавление нового пользователя"""
        try:
            # Создаем диалоговое окно для добавления пользователя
            dialog, main_layout = self.create_styled_dialog("Добавить пользователя", 450, 600)

            # Форма
            form_layout = QFormLayout()
            form_layout.setSpacing(10)

            # Логин
            username_input = self.create_styled_line_edit("Введите логин")
            username_label = QLabel("Логин*:")
            username_label.setStyleSheet("font-weight: bold; color: #485935;")
            form_layout.addRow(username_label, username_input)

            # Email
            email_input = self.create_styled_line_edit("Введите email")
            email_label = QLabel("Email*:")
            email_label.setStyleSheet("font-weight: bold; color: #485935;")
            form_layout.addRow(email_label, email_input)

            # Пароль
            password_input = self.create_styled_line_edit("Введите пароль")
            password_input.setEchoMode(QLineEdit.Password)
            password_label = QLabel("Пароль*:")
            password_label.setStyleSheet("font-weight: bold; color: #485935;")
            form_layout.addRow(password_label, password_input)

            # Имя
            first_name_input = self.create_styled_line_edit("Введите имя")
            first_name_label = QLabel("Имя:")
            first_name_label.setStyleSheet("font-weight: bold; color: #485935;")
            form_layout.addRow(first_name_label, first_name_input)

            # Фамилия
            last_name_input = self.create_styled_line_edit("Введите фамилию")
            last_name_label = QLabel("Фамилия:")
            last_name_label.setStyleSheet("font-weight: bold; color: #485935;")
            form_layout.addRow(last_name_label, last_name_input)

            # Дата рождения
            birth_date_input = self.create_styled_line_edit("дд.мм.гггг")
            birth_date_input.setPlaceholderText("Например: 15.05.1990")
            birth_date_label = QLabel("Дата рождения:")
            birth_date_label.setStyleSheet("font-weight: bold; color: #485935;")
            form_layout.addRow(birth_date_label, birth_date_input)

            # Роль
            role_combo = self.create_styled_combobox()
            role_combo.addItems(["user", "admin"])
            role_label = QLabel("Роль:")
            role_label.setStyleSheet("font-weight: bold; color: #485935;")
            form_layout.addRow(role_label, role_combo)

            main_layout.addLayout(form_layout)

            # Примечания
            notes_widget = QWidget()
            notes_layout = QVBoxLayout(notes_widget)
            notes_layout.setSpacing(5)
            notes_layout.setContentsMargins(10, 5, 10, 5)

            # Примечание об обязательных полях
            note_label = QLabel("* - обязательные поля")
            note_label.setStyleSheet("font-size: 11px; color: #7f8c8d; font-style: italic;")
            note_label.setAlignment(Qt.AlignLeft)
            notes_layout.addWidget(note_label)

            # Примечание о дате рождения
            birth_note = QLabel("Формат даты рождения: дд.мм.гггг (например: 15.05.1990)")
            birth_note.setStyleSheet("font-size: 11px; color: #7f8c8d; font-style: italic;")
            birth_note.setAlignment(Qt.AlignLeft)
            notes_layout.addWidget(birth_note)

            # Примечание о том, что дата рождения не обязательна
            birth_optional_note = QLabel("Дата рождения - необязательное поле")
            birth_optional_note.setStyleSheet("font-size: 11px; color: #7f8c8d; font-style: italic;")
            birth_optional_note.setAlignment(Qt.AlignLeft)
            notes_layout.addWidget(birth_optional_note)

            main_layout.addWidget(notes_widget)

            # Спейсер
            main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

            # Кнопки
            buttons_layout = QHBoxLayout()
            buttons_layout.setSpacing(15)

            save_button = self.create_styled_button("Сохранить", "primary")
            cancel_button = self.create_styled_button("Отмена", "secondary")

            def save():
                username = username_input.text().strip()
                email = email_input.text().strip()
                password = password_input.text().strip()
                first_name = first_name_input.text().strip()
                last_name = last_name_input.text().strip()
                birth_date = birth_date_input.text().strip()
                role = role_combo.currentText()

                if not username or not email or not password:
                    self.show_warning_message("Внимание", "Заполните обязательные поля: Логин, Email и Пароль")
                    return

                # Проверка уникальности
                existing_user = self.service.User.get_or_none(self.service.User.username == username)
                if existing_user:
                    self.show_warning_message("Ошибка", "Пользователь с таким логином уже существует")
                    return

                existing_email = self.service.User.get_or_none(self.service.User.email == email)
                if existing_email:
                    self.show_warning_message("Ошибка", "Пользователь с таким email уже существует")
                    return

                # Обработка даты рождения
                processed_birth_date = None
                if birth_date:
                    try:
                        birth_date_formats = ['%d.%m.%Y', '%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']

                        for fmt in birth_date_formats:
                            try:
                                processed_birth_date = datetime.strptime(birth_date, fmt)
                                break
                            except ValueError:
                                continue

                        if not processed_birth_date:
                            self.show_warning_message("Ошибка",
                                "Некорректный формат даты рождения. Используйте дд.мм.гггг (например: 15.05.1990)")
                            return

                        if processed_birth_date > datetime.now():
                            self.show_warning_message("Ошибка", "Дата рождения не может быть в будущем")
                            return

                        min_birth_date = datetime.now().replace(year=datetime.now().year - 150)
                        if processed_birth_date < min_birth_date:
                            self.show_warning_message("Ошибка",
                                f"Дата рождения не может быть раньше {min_birth_date.strftime('%d.%m.%Y')}")
                            return

                    except Exception as e:
                        self.show_warning_message("Ошибка", f"Ошибка обработки даты рождения: {str(e)}")
                        return

                try:
                    user_data = {
                        'username': username,
                        'email': email,
                        'password': password,
                        'first_name': first_name or None,
                        'last_name': last_name or None,
                        'role': role,
                        'birth_date': processed_birth_date  # Может быть None
                    }

                    self.service.User.create(**user_data)
                    if hasattr(self.window, 'load_users'):
                        self.window.load_users()
                    self.show_info_message("Успех", "Пользователь успешно добавлен")
                    dialog.accept()

                except Exception as e:
                    self.show_error_message("Ошибка", f"Не удалось сохранить пользователя:\n{str(e)}")

            save_button.clicked.connect(save)
            cancel_button.clicked.connect(dialog.reject)

            buttons_layout.addWidget(save_button)
            buttons_layout.addWidget(cancel_button)
            main_layout.addLayout(buttons_layout)

            dialog.setLayout(main_layout)
            dialog.exec()

        except Exception as e:
            self.show_error_message("Ошибка", f"Не удалось открыть диалог добавления пользователя:\n{str(e)}")

    def edit_user(self):
            """Редактирование выбранного пользователя"""
            try:
                current_row = self.window.users_table.currentRow()
                if current_row < 0:
                    self.show_warning_message("Внимание", "Выберите пользователя для редактирования")
                    return

                user_id = int(self.window.users_table.item(current_row, 0).text())

                try:
                    user = self.service.User.get_by_id(user_id)
                except self.service.User.DoesNotExist:
                    self.show_warning_message("Ошибка", "Пользователь не найден")
                    return

                is_current_user = (user_id == self.window.user_id)

                # Создаем диалоговое окно для редактирования пользователя
                dialog, main_layout = self.create_styled_dialog(
                    f"Редактировать пользователя",
                    450, 650 if is_current_user else 600
                )

                # Форма
                form_layout = QFormLayout()
                form_layout.setSpacing(10)

                # Поле "Логин"
                username_input = self.create_styled_line_edit()
                username_input.setText(user.username)
                username_label = QLabel("Логин*:")
                username_label.setStyleSheet("font-weight: bold; color: #485935;")
                form_layout.addRow(username_label, username_input)

                # Поле "Email"
                email_input = self.create_styled_line_edit()
                email_input.setText(user.email)
                email_label = QLabel("Email*:")
                email_label.setStyleSheet("font-weight: bold; color: #485935;")
                form_layout.addRow(email_label, email_input)

                # Если это текущий пользователь - поле для смены пароля
                if is_current_user:
                    password_input = self.create_styled_line_edit()
                    password_input.setPlaceholderText("Введите новый пароль")
                    password_input.setEchoMode(QLineEdit.Password)
                    password_label = QLabel("Новый пароль:")
                    password_label.setStyleSheet("font-weight: bold; color: #485935;")
                    form_layout.addRow(password_label, password_input)

                # Поле "Имя"
                first_name_input = self.create_styled_line_edit()
                first_name_input.setText(user.first_name or '')
                first_name_label = QLabel("Имя:")
                first_name_label.setStyleSheet("font-weight: bold; color: #485935;")
                form_layout.addRow(first_name_label, first_name_input)

                # Поле "Фамилия"
                last_name_input = self.create_styled_line_edit()
                last_name_input.setText(user.last_name or '')
                last_name_label = QLabel("Фамилия:")
                last_name_label.setStyleSheet("font-weight: bold; color: #485935;")
                form_layout.addRow(last_name_label, last_name_input)

                # Дата рождения
                birth_date_input = self.create_styled_line_edit("дд.мм.гггг")
                if user.birth_date:
                    # Форматируем дату рождения для отображения
                    birth_date_str = self.format_date_for_display(user.birth_date, include_time=False)
                    birth_date_input.setText(birth_date_str)
                birth_date_input.setPlaceholderText("Например: 15.05.1990")
                birth_date_label = QLabel("Дата рождения:")
                birth_date_label.setStyleSheet("font-weight: bold; color: #485935;")
                form_layout.addRow(birth_date_label, birth_date_input)

                # Роль
                role_combo = self.create_styled_combobox()
                role_combo.addItems(["user", "admin"])
                role_combo.setCurrentText(user.role)

                # Роль
                if is_current_user:
                    # Для текущего пользователя роль не меняется - используем QLineEdit с readOnly
                    role_label = QLabel("Роль:")
                    role_label.setStyleSheet("font-weight: bold; color: #485935;")

                    role_display = QLineEdit(user.role)
                    role_display.setReadOnly(True)
                    role_display.setStyleSheet("""
                        QLineEdit {
                            padding: 8px;
                            border: 2px solid #93a267;
                            border-radius: 5px;
                            font-size: 14px;
                            background-color: #f5f5f5;
                            color: #666;
                        }
                    """)
                    form_layout.addRow(role_label, role_display)
                else:
                    # Для других пользователей - комбобокс
                    role_combo = self.create_styled_combobox()
                    role_combo.addItems(["user", "admin"])
                    role_combo.setCurrentText(user.role)

                    role_label = QLabel("Роль:")
                    role_label.setStyleSheet("font-weight: bold; color: #485935;")
                    form_layout.addRow(role_label, role_combo)
                main_layout.addLayout(form_layout)

                # Примечания
                notes_widget = QWidget()
                notes_layout = QVBoxLayout(notes_widget)
                notes_layout.setSpacing(5)
                notes_layout.setContentsMargins(10, 5, 10, 5)

                # Примечание об обязательных полях
                note_label = QLabel("* - обязательные поля")
                note_label.setStyleSheet("font-size: 11px; color: #7f8c8d; font-style: italic;")
                note_label.setAlignment(Qt.AlignLeft)
                notes_layout.addWidget(note_label)

                # Примечание о дате рождения
                birth_note = QLabel("Формат даты рождения: дд.мм.гггг (например: 15.05.1990)")
                birth_note.setStyleSheet("font-size: 11px; color: #7f8c8d; font-style: italic;")
                birth_note.setAlignment(Qt.AlignLeft)
                notes_layout.addWidget(birth_note)

                # Примечание о том, что дата рождения не обязательна
                birth_optional_note = QLabel("Оставьте поле пустым, чтобы удалить дату рождения")
                birth_optional_note.setStyleSheet("font-size: 11px; color: #7f8c8d; font-style: italic;")
                birth_optional_note.setAlignment(Qt.AlignLeft)
                notes_layout.addWidget(birth_optional_note)

                if is_current_user:
                    # Примечание о пароле
                    password_note = QLabel("Оставьте поле пароля пустым, если не хотите менять пароль")
                    password_note.setStyleSheet("font-size: 11px; color: #e74c3c; font-style: italic;")
                    password_note.setAlignment(Qt.AlignLeft)
                    notes_layout.addWidget(password_note)

                    # Примечание о роли
                    role_note = QLabel("Роль текущего пользователя нельзя изменить")
                    role_note.setStyleSheet("font-size: 11px; color: #f39c12; font-style: italic;")
                    role_note.setAlignment(Qt.AlignLeft)
                    notes_layout.addWidget(role_note)

                main_layout.addWidget(notes_widget)

                # Спейсер
                main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

                # Кнопки
                buttons_layout = QHBoxLayout()
                buttons_layout.setSpacing(15)

                save_button = self.create_styled_button("Сохранить", "primary")
                cancel_button = self.create_styled_button("Отмена", "secondary")

                def save():
                    username = username_input.text().strip()
                    email = email_input.text().strip()
                    first_name = first_name_input.text().strip()
                    last_name = last_name_input.text().strip()
                    birth_date = birth_date_input.text().strip()

                    if not username or not email:
                        self.show_warning_message("Внимание", "Заполните обязательные поля: Логин и Email")
                        return

                    # Проверка уникальности (кроме текущего пользователя)
                    existing_user = self.service.User.get_or_none(
                        (self.service.User.username == username) &
                        (self.service.User.id != user_id)
                    )
                    if existing_user:
                        self.show_warning_message("Ошибка", "Пользователь с таким логином уже существует")
                        return

                    existing_email = self.service.User.get_or_none(
                        (self.service.User.email == email) &
                        (self.service.User.id != user_id)
                    )
                    if existing_email:
                        self.show_warning_message("Ошибка", "Пользователь с таким email уже существует")
                        return

                    # Обработка даты рождения
                    processed_birth_date = None
                    if birth_date:
                        try:
                            birth_date_formats = ['%d.%m.%Y', '%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']

                            for fmt in birth_date_formats:
                                try:
                                    processed_birth_date = datetime.strptime(birth_date, fmt)
                                    break
                                except ValueError:
                                    continue

                            if not processed_birth_date:
                                self.show_warning_message("Ошибка",
                                    "Некорректный формат даты рождения. Используйте дд.мм.гггг (например: 15.05.1990)")
                                return

                            if processed_birth_date > datetime.now():
                                self.show_warning_message("Ошибка", "Дата рождения не может быть в будущем")
                                return

                            min_birth_date = datetime.now().replace(year=datetime.now().year - 150)
                            if processed_birth_date < min_birth_date:
                                self.show_warning_message("Ошибка",
                                    f"Дата рождения не может быть раньше {min_birth_date.strftime('%d.%m.%Y')}")
                                return

                        except Exception as e:
                            self.show_warning_message("Ошибка", f"Ошибка обработки даты рождения: {str(e)}")
                            return
                    else:
                        processed_birth_date = None

                    try:
                        update_data = {
                            'username': username,
                            'email': email,
                            'first_name': first_name or None,
                            'last_name': last_name or None,
                            'birth_date': processed_birth_date  # Может быть None для удаления
                        }

                        # Меняем роль только если это не текущий пользователь
                        if not is_current_user:
                            update_data['role'] = role_combo.currentText()

                        # Меняем пароль только если это текущий пользователь И пароль указан
                        if is_current_user:
                            password = password_input.text().strip()
                            if password:
                                update_data['password'] = password

                        self.service.User.update(**update_data).where(
                            self.service.User.id == user_id
                        ).execute()

                        self.load_users()
                        self.show_info_message("Успех", "Пользователь успешно обновлен")
                        dialog.accept()

                    except Exception as e:
                        self.show_error_message("Ошибка", f"Не удалось обновить пользователя:\n{str(e)}")

                save_button.clicked.connect(save)
                cancel_button.clicked.connect(dialog.reject)

                buttons_layout.addWidget(save_button)
                buttons_layout.addWidget(cancel_button)
                main_layout.addLayout(buttons_layout)

                dialog.setLayout(main_layout)
                dialog.exec()

            except Exception as e:
                self.show_error_message("Ошибка", f"Не удалось редактировать пользователя:\n{str(e)}")

    def format_date_for_display(self, date_value, include_time=True):
        """Форматирование даты для отображения"""
        if not date_value:
            return ""

        try:
            if isinstance(date_value, datetime):
                date_obj = date_value
            elif isinstance(date_value, str):
                for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%Y-%m-%dT%H:%M:%S']:
                    try:
                        date_obj = datetime.strptime(date_value, fmt)
                        break
                    except ValueError:
                        continue
                else:
                    return str(date_value)[:10]
            else:
                return str(date_value)

            if include_time:
                return date_obj.strftime('%d.%m.%Y %H:%M')
            else:
                return date_obj.strftime('%d.%m.%Y')

        except Exception:
            return str(date_value)[:10]

    def update_user_dialog(self, dialog, user_id, is_current_user, username, email, password, first_name, last_name, role):
        """Обновление пользователя из диалога"""
        try:
            if not username or not email:
                self.show_warning_message("Внимание", "Заполните обязательные поля: Логин и Email")
                return

            # Проверка уникальности логина и email
            existing_user = self.service.User.get_or_none(
                (self.service.User.username == username) &
                (self.service.User.id != user_id)
            )
            if existing_user:
                self.show_warning_message("Ошибка", "Пользователь с таким логином уже существует")
                return

            existing_email = self.service.User.get_or_none(
                (self.service.User.email == email) &
                (self.service.User.id != user_id)
            )
            if existing_email:
                self.show_warning_message("Ошибка", "Пользователь с таким email уже существует")
                return

            # Обновление пользователя
            update_data = {
                'username': username,
                'email': email,
                'first_name': first_name or None,
                'last_name': last_name or None
            }

            # Меняем роль только если это не текущий пользователь
            if not is_current_user:
                update_data['role'] = role

            # Меняем пароль только если это текущий пользователь И пароль указан
            if is_current_user and password:
                update_data['password'] = password

            self.service.User.update(**update_data).where(self.service.User.id == user_id).execute()

            if hasattr(self.window, 'load_users'):
                self.window.load_users()

            self.show_info_message("Успех", "Пользователь успешно обновлен")
            dialog.accept()

        except Exception as e:
            self.show_error_message("Ошибка", f"Не удалось обновить пользователя:\n{str(e)}")

    def delete_user(self):
        """Удаление выбранного пользователя"""
        try:
            current_row = self.window.users_table.currentRow()
            if current_row < 0:
                self.show_warning_message("Внимание", "Выберите пользователя для удаления")
                return

            user_id = int(self.window.users_table.item(current_row, 0).text())
            username = self.window.users_table.item(current_row, 1).text()

            # Проверка, не пытается ли админ удалить самого себя
            if user_id == self.window.user_id:
                self.show_warning_message("Внимание", "Вы не можете удалить самого себя")
                return

            # Подтверждение удаления с использованием стилизованного диалога
            if self.show_confirmation_dialog("Подтверждение удаления",
                                            f"Вы уверены, что хотите удалить пользователя '{username}'?"):
                try:
                    user = self.service.User.get_by_id(user_id)
                    if user:
                        user.delete_instance()
                        if hasattr(self.window, 'load_users'):
                            self.window.load_users()
                        self.show_info_message("Успех", "Пользователь успешно удален")
                    else:
                        self.show_warning_message("Ошибка", "Пользователь не найден")

                except Exception as e:
                    self.show_error_message("Ошибка", f"Не удалось удалить пользователя:\n{str(e)}")

        except Exception as e:
            self.show_error_message("Ошибка", f"Не удалось выполнить операцию удаления:\n{str(e)}")

    def load_users(self):
        """Загрузка пользователей с сортировкой по ID"""
        try:
            users = list(self.service.User.select().order_by(self.service.User.id).dicts())

            # Проверяем, есть ли у таблицы достаточно столбцов
            if self.window.users_table.columnCount() < 8:
                self.window.users_table.setColumnCount(8)

            # Устанавливаем заголовки столбцов
            headers = [
                "ID", "Логин", "Email", "Имя", "Фамилия",
                "Роль", "Дата регистрации", "Дата рождения"
            ]
            self.window.users_table.setHorizontalHeaderLabels(headers)

            self.window.users_table.setRowCount(len(users))

            for i, user in enumerate(users):
                # ID
                self.window.users_table.setItem(i, 0, QTableWidgetItem(str(user['id'])))

                # Логин
                self.window.users_table.setItem(i, 1, QTableWidgetItem(user['username']))

                # Email
                self.window.users_table.setItem(i, 2, QTableWidgetItem(user.get('email', '')))

                # Имя
                self.window.users_table.setItem(i, 3, QTableWidgetItem(user.get('first_name', '')))

                # Фамилия
                self.window.users_table.setItem(i, 4, QTableWidgetItem(user.get('last_name', '')))

                # Роль с цветовым оформлением
                role = user.get('role', 'user')
                role_item = QTableWidgetItem(role)

                # Разные цвета для ролей
                if role == 'admin':
                    role_item.setForeground(QBrush(QColor("#FF5722")))  # Оранжево-красный для админа
                    role_item.setBackground(QBrush(QColor("#FFEBEE")))  # Светлый фон
                else:
                    role_item.setForeground(QBrush(QColor("#2196F3")))  # Синий для пользователя
                    role_item.setBackground(QBrush(QColor("#E3F2FD")))  # Светло-синий фон

                self.window.users_table.setItem(i, 5, role_item)

                # Дата регистрации
                created_at = user.get('created_at')
                created_item = self.create_date_table_item(created_at, "регистрации")
                created_item.setTextAlignment(Qt.AlignCenter)
                self.window.users_table.setItem(i, 6, created_item)

                # Дата рождения
                birth_date = user.get('birth_date')
                birth_item = self.create_date_table_item(birth_date, "рождения", is_birth_date=True)
                birth_item.setTextAlignment(Qt.AlignCenter)
                self.window.users_table.setItem(i, 7, birth_item)

        except Exception as e:
            self.show_error_message("Ошибка", f"Не удалось загрузить пользователей: {str(e)}")

    def create_date_table_item(self, date_value, context="", is_birth_date=False):
        """
        Создает элемент таблицы для отображения даты
        """
        item = QTableWidgetItem()

        if not date_value:
            item.setText("Не указана" if is_birth_date else "N/A")
            return item

        try:
            date_str = ""
            date_obj = None

            # Преобразуем в datetime объект
            if isinstance(date_value, datetime):
                date_obj = date_value
            elif isinstance(date_value, str):
                formats_to_try = [
                    '%Y-%m-%d %H:%M:%S',
                    '%Y-%m-%dT%H:%M:%S',  # ISO формат
                    '%Y-%m-%dT%H:%M:%S.%f',
                    '%Y-%m-%dT%H:%M:%SZ',
                    '%Y-%m-%d',
                    '%d.%m.%Y',
                    '%d/%m/%Y',
                    '%Y/%m/%d'
                ]

                for fmt in formats_to_try:
                    try:
                        date_obj = datetime.strptime(date_value, fmt)
                        break
                    except ValueError:
                        continue

            if date_obj:
                if is_birth_date:
                    date_str = date_obj.strftime('%d.%m.%Y')

                    # Проверяем корректность даты рождения
                    if date_obj > datetime.now():
                        item.setText(f"{date_str} ⚠")
                else:
                    # Дата регистрации
                    date_str = date_obj.strftime('%d.%m.%Y %H:%M')
                    item.setText(date_str)
            else:
                item.setText(str(date_value)[:20])

        except Exception as e:
            item.setText(f"Ошибка: {str(date_value)[:10]}")

        # Добавляем всплывающую подсказку
        tooltip = f"Дата {context}: {item.text()}"
        item.setToolTip(tooltip)

        return item



    # Методы для семейств растений
    def add_family(self):
        """Добавление семейства растений"""
        dialog, main_layout = self.create_styled_dialog("Добавить семейство растений", 400, 450)

        # Форма
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        # Поле "Название"
        name_input = self.create_styled_line_edit("Введите название семейства")
        name_label = QLabel("Название:")
        name_label.setStyleSheet("font-weight: bold; color: #485935;")
        form_layout.addRow(name_label, name_input)

        # Поле "Описание"
        description_input = self.create_styled_text_edit()
        description_label = QLabel("Описание:")
        description_label.setStyleSheet("font-weight: bold; color: #485935;")
        form_layout.addRow(description_label, description_input)

        main_layout.addLayout(form_layout)

        # Спейсер
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        ok_button = self.create_styled_button("Сохранить", "primary")
        cancel_button = self.create_styled_button("Отмена", "secondary")

        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)
        main_layout.addLayout(buttons_layout)

        def save():
            name = name_input.text().strip()
            description = description_input.toPlainText().strip()

            if not name:
                self.show_warning_message("Ошибка", "Введите название семейства")
                return

            try:
                self.service.PlantFamily.create(
                    name=name,
                    description=description if description else None
                )
                self.load_families()
                self.show_info_message("Успех", "Семейство добавлено")
                dialog.accept()
            except Exception as e:
                self.show_error_message("Ошибка", f"Ошибка: {str(e)}")

        ok_button.clicked.connect(save)
        cancel_button.clicked.connect(dialog.reject)

        dialog.setLayout(main_layout)
        dialog.exec()

    def edit_family(self):
        """Редактирование семейства растений"""
        selected = self.window.families_table.currentRow()
        if selected >= 0:
            family_id = int(self.window.families_table.item(selected, 0).text())
            family_name = self.window.families_table.item(selected, 1).text()
            family_description = self.window.families_table.item(selected, 2).text()

            dialog, main_layout = self.create_styled_dialog(f"Редактировать семейство: {family_name}", 400, 450)

            # Форма
            form_layout = QFormLayout()
            form_layout.setSpacing(10)

            # Поле "Название"
            name_input = self.create_styled_line_edit()
            name_input.setText(family_name)
            name_label = QLabel("Название:")
            name_label.setStyleSheet("font-weight: bold; color: #485935;")
            form_layout.addRow(name_label, name_input)

            # Поле "Описание"
            description_input = self.create_styled_text_edit()
            description_input.setPlainText(family_description)
            description_label = QLabel("Описание:")
            description_label.setStyleSheet("font-weight: bold; color: #485935;")
            form_layout.addRow(description_label, description_input)

            main_layout.addLayout(form_layout)

            # Спейсер
            main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

            # Кнопки
            buttons_layout = QHBoxLayout()
            buttons_layout.setSpacing(15)

            ok_button = self.create_styled_button("Сохранить", "primary")
            cancel_button = self.create_styled_button("Отмена", "secondary")

            buttons_layout.addWidget(ok_button)
            buttons_layout.addWidget(cancel_button)
            main_layout.addLayout(buttons_layout)

            def save():
                name = name_input.text().strip()
                description = description_input.toPlainText().strip()

                if not name:
                    self.show_warning_message("Ошибка", "Введите название семейства")
                    return

                try:
                    self.service.PlantFamily.update(
                        name=name,
                        description=description if description else None
                    ).where(self.service.PlantFamily.id == family_id).execute()
                    self.load_families()
                    self.show_info_message("Успех", "Семейство обновлено")
                    dialog.accept()
                except Exception as e:
                    self.show_error_message("Ошибка", f"Ошибка: {str(e)}")

            ok_button.clicked.connect(save)
            cancel_button.clicked.connect(dialog.reject)

            dialog.setLayout(main_layout)
            dialog.exec()
        else:
            self.show_warning_message("Внимание", "Выберите семейство")

    def delete_family(self):
        """Удаление семейства растений"""
        selected = self.window.families_table.currentRow()
        if selected >= 0:
            family_name = self.window.families_table.item(selected, 1).text()

            if self.show_confirmation_dialog("Подтверждение", f"Удалить семейство '{family_name}'?"):
                try:
                    family_id = int(self.window.families_table.item(selected, 0).text())
                    family = self.service.PlantFamily.get_by_id(family_id)
                    family.delete_instance()
                    self.reset_sequence(self.service.PlantFamily)
                    self.load_families()
                    self.show_info_message("Успех", "Семейство удалено")
                except self.service.PlantFamily.DoesNotExist:
                    self.show_error_message("Ошибка", "Семейство не найдено")
                except Exception as e:
                    self.show_error_message("Ошибка", f"Ошибка: {str(e)}")
        else:
            self.show_warning_message("Внимание", "Выберите семейство")

    def load_families(self):
        """Загрузка семейств растений с сортировкой по ID"""
        try:
            families = list(self.service.PlantFamily.select().order_by(self.service.PlantFamily.id).dicts())
            self.window.families_table.setRowCount(len(families))
            for i, family in enumerate(families):
                self.window.families_table.setItem(i, 0, QTableWidgetItem(str(family['id'])))
                self.window.families_table.setItem(i, 1, QTableWidgetItem(family['name']))
                self.window.families_table.setItem(i, 2, QTableWidgetItem(family.get('description', '')))
        except Exception as e:
            self.show_error_message("Ошибка", f"Не удалось загрузить семейства: {str(e)}")




    # Методы для руководств по уходу
    def add_care_guide(self):
        """Добавление руководства по уходу"""
        dialog, main_layout = self.create_styled_dialog("Добавить руководство по уходу", 450, 500)

        # Форма
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        # Поле "Полив"
        watering_input = self.create_styled_line_edit("Введите режим полива")
        watering_label = QLabel("Полив:")
        watering_label.setStyleSheet("font-weight: bold; color: #485935;")
        form_layout.addRow(watering_label, watering_input)

        # Поле "Свет"
        light_input = self.create_styled_spinbox()
        light_input.setRange(0, 100000)
        light_input.setSuffix(" лк")
        light_label = QLabel("Свет:")
        light_label.setStyleSheet("font-weight: bold; color: #485935;")
        form_layout.addRow(light_label, light_input)

        # Поле "Темп. мин"
        temp_min_input = self.create_styled_spinbox()
        temp_min_input.setRange(-50, 50)
        temp_min_input.setSuffix(" °C")
        temp_min_label = QLabel("Темп. мин:")
        temp_min_label.setStyleSheet("font-weight: bold; color: #485935;")
        form_layout.addRow(temp_min_label, temp_min_input)

        # Поле "Темп. макс"
        temp_max_input = self.create_styled_spinbox()
        temp_max_input.setRange(-50, 50)
        temp_max_input.setSuffix(" °C")
        temp_max_label = QLabel("Темп. макс:")
        temp_max_label.setStyleSheet("font-weight: bold; color: #485935;")
        form_layout.addRow(temp_max_label, temp_max_input)

        # Поле "Почва"
        soil_input = self.create_styled_line_edit("Введите тип почвы")
        soil_label = QLabel("Почва:")
        soil_label.setStyleSheet("font-weight: bold; color: #485935;")
        form_layout.addRow(soil_label, soil_input)

        # Поле "Удобрения"
        fertilizers_input = self.create_styled_line_edit("Введите удобрения")
        fertilizers_label = QLabel("Удобрения:")
        fertilizers_label.setStyleSheet("font-weight: bold; color: #485935;")
        form_layout.addRow(fertilizers_label, fertilizers_input)

        # Поле "Влажность"
        humidity_input = self.create_styled_spinbox()
        humidity_input.setRange(0, 100)
        humidity_input.setSuffix(" %")
        humidity_label = QLabel("Влажность:")
        humidity_label.setStyleSheet("font-weight: bold; color: #485935;")
        form_layout.addRow(humidity_label, humidity_input)

        main_layout.addLayout(form_layout)

        # Спейсер
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        ok_button = self.create_styled_button("Сохранить", "primary")
        cancel_button = self.create_styled_button("Отмена", "secondary")

        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)
        main_layout.addLayout(buttons_layout)

        def save():
            try:
                watering = watering_input.text().strip()
                watering = watering if watering != "" else None

                soil = soil_input.text().strip()
                soil = soil if soil != "" else None

                fertilizers = fertilizers_input.text().strip()
                fertilizers = fertilizers if fertilizers != "" else None

                self.service.CareGuide.create(
                    watering=watering,
                    light=light_input.value(),
                    temperature_min=temp_min_input.value(),
                    temperature_max=temp_max_input.value(),
                    soil=soil,
                    fertilizers=fertilizers,
                    humidity=humidity_input.value()
                )
                self.load_care_guides()
                self.show_info_message("Успех", "Руководство добавлено")
                dialog.accept()
            except Exception as e:
                self.show_error_message("Ошибка", f"Ошибка: {str(e)}")

        ok_button.clicked.connect(save)
        cancel_button.clicked.connect(dialog.reject)

        dialog.setLayout(main_layout)
        dialog.exec()

    def edit_care_guide(self):
        """Редактирование руководства по уходу"""
        selected = self.window.care_guides_table.currentRow()
        if selected >= 0:
            guide_id = int(self.window.care_guides_table.item(selected, 0).text())

            dialog, main_layout = self.create_styled_dialog("Редактировать руководство по уходу", 450, 500)

            # Форма
            form_layout = QFormLayout()
            form_layout.setSpacing(10)

            # Безопасное получение значений из таблицы
            def get_table_value(row, col, default=""):
                item = self.window.care_guides_table.item(row, col)
                if item is None:
                    return default
                text = item.text()
                return text if text != "" else default

            # Поле "Полив"
            watering_input = self.create_styled_line_edit()
            watering_input.setText(get_table_value(selected, 1))
            watering_label = QLabel("Полив:")
            watering_label.setStyleSheet("font-weight: bold; color: #485935;")
            form_layout.addRow(watering_label, watering_input)

            # Поле "Свет"
            light_input = self.create_styled_spinbox()
            light_input.setRange(0, 100000)
            light_input.setSuffix(" лк")
            light_value = get_table_value(selected, 2, "0")
            try:
                light_input.setValue(int(light_value))
            except ValueError:
                light_input.setValue(0)
            light_label = QLabel("Свет:")
            light_label.setStyleSheet("font-weight: bold; color: #485935;")
            form_layout.addRow(light_label, light_input)

            # Поле "Темп. мин"
            temp_min_input = self.create_styled_spinbox()
            temp_min_input.setRange(-50, 50)
            temp_min_input.setSuffix(" °C")
            temp_min_value = get_table_value(selected, 3, "0")
            try:
                temp_min_input.setValue(int(temp_min_value))
            except ValueError:
                temp_min_input.setValue(0)
            temp_min_label = QLabel("Темп. мин:")
            temp_min_label.setStyleSheet("font-weight: bold; color: #485935;")
            form_layout.addRow(temp_min_label, temp_min_input)

            # Поле "Темп. макс"
            temp_max_input = self.create_styled_spinbox()
            temp_max_input.setRange(-50, 50)
            temp_max_input.setSuffix(" °C")
            temp_max_value = get_table_value(selected, 4, "0")
            try:
                temp_max_input.setValue(int(temp_max_value))
            except ValueError:
                temp_max_input.setValue(0)
            temp_max_label = QLabel("Темп. макс:")
            temp_max_label.setStyleSheet("font-weight: bold; color: #485935;")
            form_layout.addRow(temp_max_label, temp_max_input)

            # Поле "Почва"
            soil_input = self.create_styled_line_edit()
            soil_input.setText(get_table_value(selected, 5))
            soil_label = QLabel("Почва:")
            soil_label.setStyleSheet("font-weight: bold; color: #485935;")
            form_layout.addRow(soil_label, soil_input)

            # Поле "Удобрения"
            fertilizers_input = self.create_styled_line_edit()
            fertilizers_input.setText(get_table_value(selected, 6))
            fertilizers_label = QLabel("Удобрения:")
            fertilizers_label.setStyleSheet("font-weight: bold; color: #485935;")
            form_layout.addRow(fertilizers_label, fertilizers_input)

            # Поле "Влажность"
            humidity_input = self.create_styled_spinbox()
            humidity_input.setRange(0, 100)
            humidity_input.setSuffix(" %")
            humidity_value = get_table_value(selected, 7, "0")
            try:
                humidity_input.setValue(int(humidity_value))
            except ValueError:
                humidity_input.setValue(0)
            humidity_label = QLabel("Влажность:")
            humidity_label.setStyleSheet("font-weight: bold; color: #485935;")
            form_layout.addRow(humidity_label, humidity_input)

            main_layout.addLayout(form_layout)

            # Спейсер
            main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

            # Кнопки
            buttons_layout = QHBoxLayout()
            buttons_layout.setSpacing(15)

            ok_button = self.create_styled_button("Сохранить", "primary")
            cancel_button = self.create_styled_button("Отмена", "secondary")

            buttons_layout.addWidget(ok_button)
            buttons_layout.addWidget(cancel_button)
            main_layout.addLayout(buttons_layout)

            def save():
                try:
                    watering = watering_input.text().strip()
                    watering = watering if watering != "" else None

                    soil = soil_input.text().strip()
                    soil = soil if soil != "" else None

                    fertilizers = fertilizers_input.text().strip()
                    fertilizers = fertilizers if fertilizers != "" else None

                    update_data = {
                        'watering': watering,
                        'light': light_input.value(),
                        'temperature_min': temp_min_input.value(),
                        'temperature_max': temp_max_input.value(),
                        'soil': soil,
                        'fertilizers': fertilizers,
                        'humidity': humidity_input.value()
                    }

                    self.service.CareGuide.update(**update_data).where(
                        self.service.CareGuide.id == guide_id
                    ).execute()

                    self.load_care_guides()
                    self.show_info_message("Успех", "Руководство обновлено")
                    dialog.accept()
                except Exception as e:
                    self.show_error_message("Ошибка", f"Ошибка: {str(e)}")

            ok_button.clicked.connect(save)
            cancel_button.clicked.connect(dialog.reject)

            dialog.setLayout(main_layout)
            dialog.exec()
        else:
            self.show_warning_message("Внимание", "Выберите руководство")

    def delete_care_guide(self):
        """Удаление руководства по уходу"""
        selected = self.window.care_guides_table.currentRow()
        if selected >= 0:
            if self.show_confirmation_dialog("Подтверждение", "Удалить руководство по уходу?"):
                try:
                    guide_id = int(self.window.care_guides_table.item(selected, 0).text())
                    guide = self.service.CareGuide.get_by_id(guide_id)
                    guide.delete_instance()
                    self.reset_sequence(self.service.CareGuide)
                    self.load_care_guides()
                    self.show_info_message("Успех", "Руководство удалено")
                except self.service.CareGuide.DoesNotExist:
                    self.show_error_message("Ошибка", "Руководство не найдено")
                except Exception as e:
                    self.show_error_message("Ошибка", f"Ошибка: {str(e)}")
        else:
            self.show_warning_message("Внимание", "Выберите руководство")

    def load_care_guides(self):
        """Загрузка руководств по уходу с сортировкой по ID"""
        try:
            guides = list(self.service.CareGuide.select().order_by(self.service.CareGuide.id).dicts())
            self.window.care_guides_table.setRowCount(len(guides))
            for i, guide in enumerate(guides):
                self.window.care_guides_table.setItem(i, 0, QTableWidgetItem(str(guide['id'])))
                self.window.care_guides_table.setItem(i, 1, QTableWidgetItem(guide.get('watering') or ''))

                light_val = guide.get('light')
                self.window.care_guides_table.setItem(i, 2, QTableWidgetItem(str(light_val) if light_val is not None else ''))

                temp_min = guide.get('temperature_min')
                self.window.care_guides_table.setItem(i, 3, QTableWidgetItem(str(temp_min) if temp_min is not None else ''))

                temp_max = guide.get('temperature_max')
                self.window.care_guides_table.setItem(i, 4, QTableWidgetItem(str(temp_max) if temp_max is not None else ''))

                self.window.care_guides_table.setItem(i, 5, QTableWidgetItem(guide.get('soil') or ''))
                self.window.care_guides_table.setItem(i, 6, QTableWidgetItem(guide.get('fertilizers') or ''))

                humidity_val = guide.get('humidity')
                self.window.care_guides_table.setItem(i, 7, QTableWidgetItem(str(humidity_val) if humidity_val is not None else ''))
        except Exception as e:
            self.show_error_message("Ошибка", f"Не удалось загрузить руководства: {str(e)}")



    # Методы для местоположений
    def add_location(self):
        """Добавление местоположения"""
        dialog, main_layout = self.create_styled_dialog("Добавить местоположение", 400, 450)

        # Форма
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        # Поле "Название местности"
        name_input = self.create_styled_line_edit("Введите название местности")
        name_label = QLabel("Название местности:")
        name_label.setStyleSheet("font-weight: bold; color: #485935;")
        form_layout.addRow(name_label, name_input)

        # Поле "Описание"
        description_input = self.create_styled_text_edit()
        description_label = QLabel("Описание:")
        description_label.setStyleSheet("font-weight: bold; color: #485935;")
        form_layout.addRow(description_label, description_input)

        main_layout.addLayout(form_layout)

        # Спейсер
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        ok_button = self.create_styled_button("Сохранить", "primary")
        cancel_button = self.create_styled_button("Отмена", "secondary")

        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)
        main_layout.addLayout(buttons_layout)

        def save():
            name = name_input.text().strip()
            description = description_input.toPlainText().strip()

            if not name:
                self.show_warning_message("Ошибка", "Введите название местности")
                return

            try:
                self.service.PlantLocation.create(
                    location_name=name,
                    description=description if description else None
                )
                self.load_locations()
                self.show_info_message("Успех", "Местоположение добавлено")
                dialog.accept()
            except Exception as e:
                self.show_error_message("Ошибка", f"Ошибка: {str(e)}")

        ok_button.clicked.connect(save)
        cancel_button.clicked.connect(dialog.reject)

        dialog.setLayout(main_layout)
        dialog.exec()

    def edit_location(self):
        """Редактирование местоположения"""
        selected = self.window.locations_table.currentRow()
        if selected >= 0:
            location_id = int(self.window.locations_table.item(selected, 0).text())
            location_name = self.window.locations_table.item(selected, 1).text()
            location_description = self.window.locations_table.item(selected, 2).text()

            dialog, main_layout = self.create_styled_dialog(f"Редактировать местоположение: {location_name}", 400, 450)

            # Форма
            form_layout = QFormLayout()
            form_layout.setSpacing(10)

            # Поле "Название местности"
            name_input = self.create_styled_line_edit()
            name_input.setText(location_name)
            name_label = QLabel("Название местности:")
            name_label.setStyleSheet("font-weight: bold; color: #485935;")
            form_layout.addRow(name_label, name_input)

            # Поле "Описание"
            description_input = self.create_styled_text_edit()
            description_input.setPlainText(location_description)
            description_label = QLabel("Описание:")
            description_label.setStyleSheet("font-weight: bold; color: #485935;")
            form_layout.addRow(description_label, description_input)

            main_layout.addLayout(form_layout)

            # Спейсер
            main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

            # Кнопки
            buttons_layout = QHBoxLayout()
            buttons_layout.setSpacing(15)

            ok_button = self.create_styled_button("Сохранить", "primary")
            cancel_button = self.create_styled_button("Отмена", "secondary")

            buttons_layout.addWidget(ok_button)
            buttons_layout.addWidget(cancel_button)
            main_layout.addLayout(buttons_layout)

            def save():
                name = name_input.text().strip()
                description = description_input.toPlainText().strip()

                if not name:
                    self.show_warning_message("Ошибка", "Введите название местности")
                    return

                try:
                    self.service.PlantLocation.update(
                        location_name=name,
                        description=description if description else None
                    ).where(self.service.PlantLocation.id == location_id).execute()
                    self.load_locations()
                    self.show_info_message("Успех", "Местоположение обновлено")
                    dialog.accept()
                except Exception as e:
                    self.show_error_message("Ошибка", f"Ошибка: {str(e)}")

            ok_button.clicked.connect(save)
            cancel_button.clicked.connect(dialog.reject)

            dialog.setLayout(main_layout)
            dialog.exec()
        else:
            self.show_warning_message("Внимание", "Выберите местоположение")

    def delete_location(self):
        """Удаление местоположения"""
        selected = self.window.locations_table.currentRow()
        if selected >= 0:
            location_name = self.window.locations_table.item(selected, 1).text()

            if self.show_confirmation_dialog("Подтверждение", f"Удалить местоположение '{location_name}'?"):
                try:
                    location_id = int(self.window.locations_table.item(selected, 0).text())
                    location = self.service.PlantLocation.get_by_id(location_id)
                    location.delete_instance()
                    self.reset_sequence(self.service.PlantLocation)
                    self.load_locations()
                    self.show_info_message("Успех", "Местоположение удалено")
                except self.service.PlantLocation.DoesNotExist:
                    self.show_error_message("Ошибка", "Местоположение не найдено")
                except Exception as e:
                    self.show_error_message("Ошибка", f"Ошибка: {str(e)}")
        else:
            self.show_warning_message("Внимание", "Выберите местоположение")

    def load_locations(self):
        """Загрузка местоположений с сортировкой по ID"""
        try:
            locations = list(self.service.PlantLocation.select().order_by(self.service.PlantLocation.id).dicts())
            self.window.locations_table.setRowCount(len(locations))
            for i, location in enumerate(locations):
                self.window.locations_table.setItem(i, 0, QTableWidgetItem(str(location['id'])))
                self.window.locations_table.setItem(i, 1, QTableWidgetItem(location['location_name']))
                self.window.locations_table.setItem(i, 2, QTableWidgetItem(location.get('description', '')))
        except Exception as e:
            self.show_error_message("Ошибка", f"Не удалось загрузить местоположения: {str(e)}")


    # Методы для фото
    def add_photo(self):
        """Добавление фотографии"""
        dialog, main_layout = self.create_styled_dialog("Добавить фотографию", 500, 350)

        # Форма
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        # Поле для выбора файла
        file_input = self.create_styled_line_edit("Нажмите кнопку справа для выбора файла")
        file_input.setReadOnly(True)

        file_button = self.create_styled_button("Выбрать...", "primary")
        file_button.setFixedWidth(100)

        file_layout = QHBoxLayout()
        file_layout.addWidget(file_input)
        file_layout.addWidget(file_button)

        file_label = QLabel("Фотография:")
        file_label.setStyleSheet("font-weight: bold; color: #485935;")
        form_layout.addRow(file_label, file_layout)

        main_layout.addLayout(form_layout)

        def browse_file():
            filename, _ = QFileDialog.getOpenFileName(
                dialog,
                "Выберите фотографию",
                "",
                "Images (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*.*)"
            )
            if filename:
                file_input.setText(filename)

        file_button.clicked.connect(browse_file)

        # Спейсер
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        ok_button = self.create_styled_button("Сохранить", "primary")
        cancel_button = self.create_styled_button("Отмена", "secondary")

        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)
        main_layout.addLayout(buttons_layout)

        def save():
            path = file_input.text().strip()

            if not path:
                self.show_warning_message("Ошибка", "Выберите фотографию")
                return

            if not os.path.exists(path):
                self.show_error_message("Ошибка", f"Файл не найден: {path}")
                return

            try:
                photos_dir = r"F:\Даша\Репозиторий\Florarium\data\photos"
                os.makedirs(photos_dir, exist_ok=True)

                import shutil
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                file_extension = os.path.splitext(path)[1]
                new_filename = f"photo_{timestamp}{file_extension}"
                destination = os.path.join(photos_dir, new_filename)

                # Копируем файл
                shutil.copy2(path, destination)

                # Сохраняем относительный путь для базы данных
                relative_path = os.path.join("data", "photos", new_filename)

                print(f"Фото сохранено в: {destination}")
                print(f"Относительный путь: {relative_path}")

                # Создаем запись в базе данных
                self.service.PlantPhoto.create(photo_url=relative_path)
                self.load_photos()
                self.show_info_message("Успех", "Фотография добавлена")
                dialog.accept()
            except Exception as e:
                self.show_error_message("Ошибка", f"Ошибка при сохранении фото: {str(e)}")
                import traceback
                traceback.print_exc()

        ok_button.clicked.connect(save)
        cancel_button.clicked.connect(dialog.reject)

        dialog.setLayout(main_layout)
        dialog.exec()

    def edit_photo(self):
        """Редактирование фотографии"""
        selected = self.window.photos_table.currentRow()
        if selected >= 0:
            photo_id = int(self.window.photos_table.item(selected, 0).text())
            current_photo_url = self.window.photos_table.item(selected, 1).text()

            dialog, main_layout = self.create_styled_dialog("Редактировать фотографию", 500, 350)

            # Форма
            form_layout = QFormLayout()
            form_layout.setSpacing(10)

            # Текущий файл
            current_file_layout = QHBoxLayout()
            current_file_label = QLabel("Текущий файл:")
            current_file_label.setStyleSheet("font-weight: bold; color: #485935;")

            # Отображаем только имя файла из URL
            if current_photo_url:
                if "data/photos/" in current_photo_url:
                    filename = current_photo_url.split("data/photos/")[-1]
                elif "data\\photos\\" in current_photo_url:
                    filename = current_photo_url.split("data\\photos\\")[-1]
                else:
                    filename = os.path.basename(current_photo_url)
                current_file_value = QLabel(filename)
            else:
                current_file_value = QLabel("Не указан")

            current_file_value.setStyleSheet("color: #666; font-style: italic;")
            current_file_layout.addWidget(current_file_label)
            current_file_layout.addWidget(current_file_value)
            form_layout.addRow("", current_file_layout)

            # Поле для выбора файла
            file_input = self.create_styled_line_edit("Выберите новый файл...")
            file_input.setReadOnly(True)

            file_button = self.create_styled_button("Выбрать...", "primary")
            file_button.setFixedWidth(100)

            file_layout = QHBoxLayout()
            file_layout.addWidget(file_input)
            file_layout.addWidget(file_button)

            file_label = QLabel("Новый файл:")
            file_label.setStyleSheet("font-weight: bold; color: #485935;")
            form_layout.addRow(file_label, file_layout)

            # Поле для ввода URL вручную
            manual_url_input = self.create_styled_line_edit("Или введите URL вручную...")
            manual_url_label = QLabel("URL вручную:")
            manual_url_label.setStyleSheet("font-weight: bold; color: #485935;")
            form_layout.addRow(manual_url_label, manual_url_input)

            main_layout.addLayout(form_layout)

            def browse_file():
                filename, _ = QFileDialog.getOpenFileName(
                    dialog,
                    "Выберите фотографию",
                    "",
                    "Images (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*.*)"
                )
                if filename:
                    file_input.setText(filename)

            file_button.clicked.connect(browse_file)

            # Спейсер
            main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

            # Кнопки
            buttons_layout = QHBoxLayout()
            buttons_layout.setSpacing(15)

            ok_button = self.create_styled_button("Сохранить", "primary")
            cancel_button = self.create_styled_button("Отмена", "secondary")

            buttons_layout.addWidget(ok_button)
            buttons_layout.addWidget(cancel_button)
            main_layout.addLayout(buttons_layout)

            def save():
                file_path = file_input.text().strip()
                manual_url = manual_url_input.text().strip()

                final_url = current_photo_url  # По умолчанию оставляем старый URL

                if file_path:
                    if not os.path.exists(file_path):
                        self.show_error_message("Ошибка", f"Файл не найден: {file_path}")
                        return

                    try:
                        photos_dir = r"F:\Даша\Репозиторий\Florarium\data\photos"
                        os.makedirs(photos_dir, exist_ok=True)

                        import shutil
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        file_extension = os.path.splitext(file_path)[1]
                        new_filename = f"photo_{timestamp}{file_extension}"
                        destination = os.path.join(photos_dir, new_filename)

                        # Копируем файл
                        shutil.copy2(file_path, destination)

                        # Сохраняем относительный путь
                        final_url = os.path.join("data", "photos", new_filename)

                        print(f"Новое фото сохранено в: {destination}")
                        print(f"Относительный путь: {final_url}")

                    except Exception as e:
                        self.show_error_message("Ошибка", f"Ошибка при копировании файла: {str(e)}")
                        import traceback
                        traceback.print_exc()
                        return

                elif manual_url:
                    if manual_url and (manual_url.startswith("http://") or manual_url.startswith("https://")):
                        final_url = manual_url
                    elif manual_url and os.path.exists(manual_url):
                        try:
                            photos_dir = r"F:\Даша\Репозиторий\Florarium\data\photos"
                            os.makedirs(photos_dir, exist_ok=True)

                            import shutil
                            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                            file_extension = os.path.splitext(manual_url)[1]
                            new_filename = f"photo_{timestamp}{file_extension}"
                            destination = os.path.join(photos_dir, new_filename)

                            shutil.copy2(manual_url, destination)
                            final_url = os.path.join("data", "photos", new_filename)

                            print(f"Фото из ручного ввода сохранено в: {destination}")
                        except Exception as e:
                            self.show_error_message("Ошибка", f"Ошибка при обработке ручного URL: {str(e)}")
                            return
                    elif manual_url:
                        # Просто сохраняем как есть (может быть относительный путь)
                        final_url = manual_url

                try:
                    # Обновляем запись в базе данных
                    self.service.PlantPhoto.update(photo_url=final_url).where(
                        self.service.PlantPhoto.id == photo_id
                    ).execute()

                    self.load_photos()
                    self.show_info_message("Успех", "Фотография обновлена")
                    dialog.accept()

                except Exception as e:
                    self.show_error_message("Ошибка", f"Ошибка при обновлении записи: {str(e)}")

            ok_button.clicked.connect(save)
            cancel_button.clicked.connect(dialog.reject)

            dialog.setLayout(main_layout)
            dialog.exec()
        else:
            self.show_warning_message("Внимание", "Выберите фотографию")

    def delete_photo(self):
        """Удаление фотографии"""
        selected = self.window.photos_table.currentRow()
        if selected >= 0:
            if self.show_confirmation_dialog("Подтверждение", "Удалить фотографию?"):
                try:
                    photo_id = int(self.window.photos_table.item(selected, 0).text())
                    photo = self.service.PlantPhoto.get_by_id(photo_id)
                    photo.delete_instance()
                    self.reset_sequence(self.service.PlantPhoto)
                    self.load_photos()
                    self.show_info_message("Успех", "Фотография удалена")
                except self.service.PlantPhoto.DoesNotExist:
                    self.show_error_message("Ошибка", "Фотография не найдена")
                except Exception as e:
                    self.show_error_message("Ошибка", f"Ошибка: {str(e)}")
        else:
            self.show_warning_message("Внимание", "Выберите фотографию")

    def load_photos(self):
        """Загрузка фотографий с сортировкой по ID"""
        try:
            photos = list(self.service.PlantPhoto.select().order_by(self.service.PlantPhoto.id).dicts())
            self.window.photos_table.setRowCount(len(photos))
            for i, photo in enumerate(photos):
                self.window.photos_table.setItem(i, 0, QTableWidgetItem(str(photo['id'])))
                self.window.photos_table.setItem(i, 1, QTableWidgetItem(photo['photo_url']))
        except Exception as e:
            self.show_error_message("Ошибка", f"Не удалось загрузить фотографии: {str(e)}")



    # Методы для растений
    def add_plant(self):
        """Добавление растения"""
        dialog, main_layout = self.create_styled_dialog("Добавить растение", 500, 550)  # Увеличил высоту

        # Форма
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        # Поле "Научное название"
        scientific_name_input = self.create_styled_line_edit("Введите научное название")
        scientific_name_label = QLabel("Научное название:")
        scientific_name_label.setStyleSheet("font-weight: bold; color: #485935;")
        form_layout.addRow(scientific_name_label, scientific_name_input)

        # Поле "Описание"
        description_input = self.create_styled_text_edit()
        description_label = QLabel("Описание:")
        description_label.setStyleSheet("font-weight: bold; color: #485935;")
        form_layout.addRow(description_label, description_input)

        # Комбобокс "Руководство по уходу"
        care_guide_combo = self.create_styled_combobox()
        care_guides = list(self.service.CareGuide.select())
        care_guide_combo.addItem("Не выбрано", None)
        for guide in care_guides:
            display_text = f"ID {guide.id}"
            if guide.watering:
                display_text += f" - {guide.watering[:30]}"
            care_guide_combo.addItem(display_text, guide.id)
        care_guide_label = QLabel("Руководство по уходу:")
        care_guide_label.setStyleSheet("font-weight: bold; color: #485935;")
        form_layout.addRow(care_guide_label, care_guide_combo)

        # Комбобокс "Основное местоположение"
        location_combo = self.create_styled_combobox()
        locations = list(self.service.PlantLocation.select())
        location_combo.addItem("Не выбрано", None)
        for location in locations:
            location_combo.addItem(f"ID {location.id} - {location.location_name}", location.id)
        location_label = QLabel("Основное местоположение:")
        location_label.setStyleSheet("font-weight: bold; color: #485935;")
        form_layout.addRow(location_label, location_combo)

        # Комбобокс "Основное фото"
        photo_combo = self.create_styled_combobox()
        photos = list(self.service.PlantPhoto.select())
        photo_combo.addItem("Не выбрано", None)
        for photo in photos:
            # Отображаем только имя файла или последнюю часть URL
            if photo.photo_url:
                filename = os.path.basename(photo.photo_url)
                display_text = f"ID {photo.id} - {filename[:30]}"
            else:
                display_text = f"ID {photo.id} - без файла"
            photo_combo.addItem(display_text, photo.id)
        photo_label = QLabel("Основное фото:")
        photo_label.setStyleSheet("font-weight: bold; color: #485935;")
        form_layout.addRow(photo_label, photo_combo)

        main_layout.addLayout(form_layout)

        # Спейсер
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        ok_button = self.create_styled_button("Сохранить", "primary")
        cancel_button = self.create_styled_button("Отмена", "secondary")

        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)
        main_layout.addLayout(buttons_layout)

        def save():
            scientific_name = scientific_name_input.text().strip()

            if not scientific_name:
                self.show_warning_message("Ошибка", "Введите научное название")
                return

            try:
                self.service.Plant.create(
                    scientific_name=scientific_name,
                    description=description_input.toPlainText().strip() or None,
                    care_guide=care_guide_combo.currentData(),
                    main_location=location_combo.currentData(),
                    main_photo=photo_combo.currentData()
                )
                self.load_plants()
                self.show_info_message("Успех", "Растение добавлено")
                dialog.accept()
            except Exception as e:
                self.show_error_message("Ошибка", f"Ошибка: {str(e)}")

        ok_button.clicked.connect(save)
        cancel_button.clicked.connect(dialog.reject)

        dialog.setLayout(main_layout)
        dialog.exec()

    def edit_plant(self):
        """Редактирование растения"""
        selected = self.window.plants_table.currentRow()
        if selected >= 0:
            plant_id = int(self.window.plants_table.item(selected, 0).text())
            plant_name = self.window.plants_table.item(selected, 1).text()

            dialog, main_layout = self.create_styled_dialog(f"Редактировать растение: {plant_name}", 500, 550)  # Увеличил высоту

            # Форма
            form_layout = QFormLayout()
            form_layout.setSpacing(10)

            # Поле "Научное название"
            scientific_name_input = self.create_styled_line_edit()
            scientific_name_input.setText(plant_name)
            scientific_name_label = QLabel("Научное название:")
            scientific_name_label.setStyleSheet("font-weight: bold; color: #485935;")
            form_layout.addRow(scientific_name_label, scientific_name_input)

            # Поле "Описание"
            description_input = self.create_styled_text_edit()
            description_item = self.window.plants_table.item(selected, 2)
            description_input.setPlainText(description_item.text() if description_item else "")
            description_label = QLabel("Описание:")
            description_label.setStyleSheet("font-weight: bold; color: #485935;")
            form_layout.addRow(description_label, description_input)

            # Комбобокс "Руководство по уходу"
            care_guide_combo = self.create_styled_combobox()
            care_guides = list(self.service.CareGuide.select())
            care_guide_combo.addItem("Не выбрано", None)

            current_guide_id = None
            try:
                plant = self.service.Plant.get_by_id(plant_id)
                if plant.care_guide:
                    current_guide_id = plant.care_guide.id
            except:
                pass

            for guide in care_guides:
                display_text = f"ID {guide.id}"
                if guide.watering:
                    display_text += f" - {guide.watering[:30]}"
                care_guide_combo.addItem(display_text, guide.id)
                if guide.id == current_guide_id:
                    care_guide_combo.setCurrentIndex(care_guide_combo.count() - 1)

            care_guide_label = QLabel("Руководство по уходу:")
            care_guide_label.setStyleSheet("font-weight: bold; color: #485935;")
            form_layout.addRow(care_guide_label, care_guide_combo)

            # Комбобокс "Основное местоположение"
            location_combo = self.create_styled_combobox()
            locations = list(self.service.PlantLocation.select())
            location_combo.addItem("Не выбрано", None)

            current_location_id = None
            try:
                if plant and plant.main_location:
                    current_location_id = plant.main_location.id
            except:
                pass

            for location in locations:
                location_combo.addItem(f"ID {location.id} - {location.location_name}", location.id)
                if location.id == current_location_id:
                    location_combo.setCurrentIndex(location_combo.count() - 1)

            location_label = QLabel("Основное местоположение:")
            location_label.setStyleSheet("font-weight: bold; color: #485935;")
            form_layout.addRow(location_label, location_combo)

            # Комбокс "Основное фото"
            photo_combo = self.create_styled_combobox()
            photos = list(self.service.PlantPhoto.select())
            photo_combo.addItem("Не выбрано", None)

            current_photo_id = None
            try:
                if plant and plant.main_photo:
                    current_photo_id = plant.main_photo.id
            except:
                pass

            for photo in photos:
                if photo.photo_url:
                    filename = os.path.basename(photo.photo_url)
                    display_text = f"ID {photo.id} - {filename[:30]}"
                else:
                    display_text = f"ID {photo.id} - без файла"
                photo_combo.addItem(display_text, photo.id)
                if photo.id == current_photo_id:
                    photo_combo.setCurrentIndex(photo_combo.count() - 1)

            photo_label = QLabel("Основное фото:")
            photo_label.setStyleSheet("font-weight: bold; color: #485935;")
            form_layout.addRow(photo_label, photo_combo)

            main_layout.addLayout(form_layout)

            # Спейсер
            main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

            # Кнопки
            buttons_layout = QHBoxLayout()
            buttons_layout.setSpacing(15)

            ok_button = self.create_styled_button("Сохранить", "primary")
            cancel_button = self.create_styled_button("Отмена", "secondary")

            buttons_layout.addWidget(ok_button)
            buttons_layout.addWidget(cancel_button)
            main_layout.addLayout(buttons_layout)

            def save():
                scientific_name = scientific_name_input.text().strip()

                if not scientific_name:
                    self.show_warning_message("Ошибка", "Введите научное название")
                    return

                try:
                    update_data = {
                        'scientific_name': scientific_name,
                        'description': description_input.toPlainText().strip() or None,
                        'care_guide': care_guide_combo.currentData(),
                        'main_location': location_combo.currentData(),
                        'main_photo': photo_combo.currentData()  # ДОБАВЛЕНО
                    }

                    if update_data['care_guide'] is None:
                        update_data['care_guide'] = None
                    if update_data['main_location'] is None:
                        update_data['main_location'] = None
                    if update_data['main_photo'] is None:  # ДОБАВЛЕНО
                        update_data['main_photo'] = None

                    self.service.Plant.update(**update_data).where(
                        self.service.Plant.id == plant_id
                    ).execute()

                    self.load_plants()
                    self.show_info_message("Успех", "Растение обновлено")
                    dialog.accept()
                except Exception as e:
                    self.show_error_message("Ошибка", f"Ошибка: {str(e)}")

            ok_button.clicked.connect(save)
            cancel_button.clicked.connect(dialog.reject)

            dialog.setLayout(main_layout)
            dialog.exec()
        else:
            self.show_warning_message("Внимание", "Выберите растение")

    def delete_plant(self):
        """Удаление растения"""
        selected = self.window.plants_table.currentRow()
        if selected >= 0:
            plant_name = self.window.plants_table.item(selected, 1).text()

            if self.show_confirmation_dialog("Подтверждение", f"Удалить растение '{plant_name}'?"):
                try:
                    plant_id = int(self.window.plants_table.item(selected, 0).text())
                    plant = self.service.Plant.get_by_id(plant_id)
                    plant.delete_instance()
                    self.reset_sequence(self.service.Plant)
                    self.load_plants()
                    self.show_info_message("Успех", "Растение удалено")
                except self.service.Plant.DoesNotExist:
                    self.show_error_message("Ошибка", "Растение не найдено")
                except Exception as e:
                    self.show_error_message("Ошибка", f"Ошибка: {str(e)}")
        else:
            self.show_warning_message("Внимание", "Выберите растение")

    def load_plants(self):
        """Загрузка растений с сортировкой по ID"""
        try:
            plants = list(self.service.Plant.select().order_by(self.service.Plant.id).dicts())
            if self.window.plants_table.columnCount() < 6:
                self.window.plants_table.setColumnCount(6)

            self.window.plants_table.setRowCount(len(plants))
            for i, plant in enumerate(plants):
                self.window.plants_table.setItem(i, 0, QTableWidgetItem(str(plant['id'])))
                self.window.plants_table.setItem(i, 1, QTableWidgetItem(plant['scientific_name']))
                self.window.plants_table.setItem(i, 2, QTableWidgetItem(plant.get('description', '')))

                care_guide_id = plant.get('care_guide')
                if care_guide_id:
                    self.window.plants_table.setItem(i, 3, QTableWidgetItem(str(care_guide_id)))
                else:
                    self.window.plants_table.setItem(i, 3, QTableWidgetItem(''))

                location_id = plant.get('main_location')
                if location_id:
                    self.window.plants_table.setItem(i, 4, QTableWidgetItem(str(location_id)))
                else:
                    self.window.plants_table.setItem(i, 4, QTableWidgetItem(''))

                photo_id = plant.get('main_photo')
                if photo_id:
                    self.window.plants_table.setItem(i, 5, QTableWidgetItem(str(photo_id)))
                else:
                    self.window.plants_table.setItem(i, 5, QTableWidgetItem(''))
        except Exception as e:
            self.show_error_message("Ошибка", f"Не удалось загрузить растения: {str(e)}")

    def load_plant_family_relations(self):
        """Загрузка связей растения-семейства с сортировкой по ID"""
        try:
            if hasattr(self.service, 'PlantFamilyRelation'):
                relations = list(self.service.PlantFamilyRelation.select(
                    self.service.PlantFamilyRelation,
                    self.service.Plant.scientific_name,
                    self.service.PlantFamily.name
                ).join(
                    self.service.Plant,
                    on=(self.service.PlantFamilyRelation.plant == self.service.Plant.id)
                ).join(
                    self.service.PlantFamily,
                    on=(self.service.PlantFamilyRelation.family == self.service.PlantFamily.id)
                ).order_by(self.service.PlantFamilyRelation.id).dicts())

                self.window.plant_family_table.setRowCount(len(relations))

                for i, rel in enumerate(relations):
                    self.window.plant_family_table.setItem(i, 0, QTableWidgetItem(str(rel['id'])))

                    plant_id = rel.get('plant_id') or (rel.get('plant') if isinstance(rel.get('plant'), int) else None)
                    family_id = rel.get('family_id') or (rel.get('family') if isinstance(rel.get('family'), int) else None)

                    self.window.plant_family_table.setItem(i, 1, QTableWidgetItem(str(plant_id) if plant_id else ''))
                    self.window.plant_family_table.setItem(i, 2, QTableWidgetItem(str(family_id) if family_id else ''))

                    plant_name = rel.get('scientific_name', f"ID: {plant_id}")
                    family_name = rel.get('name', f"ID: {family_id}")
                    self.window.plant_family_table.setItem(i, 3, QTableWidgetItem(f"{plant_name} → {family_name}"))
            else:
                self.window.plant_family_table.setRowCount(0)
        except Exception as e:
            self.window.plant_family_table.setRowCount(0)
            print(f"Ошибка загрузки связей растения-семейства: {e}")


    # Методы для вредителей
    def add_pest(self):
        """Добавление вредителя"""
        dialog, main_layout = self.create_styled_dialog("Добавить вредителя", 500, 500)

        # Форма
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        # Поле "Название вредителя"
        name_input = self.create_styled_line_edit("Введите название вредителя")
        name_label = QLabel("Название вредителя:")
        name_label.setStyleSheet("font-weight: bold; color: #485935;")
        form_layout.addRow(name_label, name_input)

        # Поле "Описание"
        description_input = self.create_styled_text_edit()
        description_label = QLabel("Описание:")
        description_label.setStyleSheet("font-weight: bold; color: #485935;")
        form_layout.addRow(description_label, description_input)

        # Поле "Методы лечения"
        treatment_input = self.create_styled_text_edit()
        treatment_label = QLabel("Методы лечения:")
        treatment_label.setStyleSheet("font-weight: bold; color: #485935;")
        form_layout.addRow(treatment_label, treatment_input)

        main_layout.addLayout(form_layout)

        # Спейсер
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        ok_button = self.create_styled_button("Сохранить", "primary")
        cancel_button = self.create_styled_button("Отмена", "secondary")

        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)
        main_layout.addLayout(buttons_layout)

        def save():
            name = name_input.text().strip()
            description = description_input.toPlainText().strip()
            treatment = treatment_input.toPlainText().strip()

            if not name:
                self.show_warning_message("Ошибка", "Введите название вредителя")
                return

            try:
                if hasattr(self.service, 'Pest'):
                    self.service.Pest.create(
                        name=name,
                        description=description if description else None,
                        treatment_methods=treatment if treatment else None
                    )
                    self.load_pests()
                    self.show_info_message("Успех", "Вредитель добавлен")
                    dialog.accept()
                else:
                    self.show_warning_message("Ошибка", "Модель вредителей не найдена в базе данных")
            except Exception as e:
                self.show_error_message("Ошибка", f"Ошибка: {str(e)}")

        ok_button.clicked.connect(save)
        cancel_button.clicked.connect(dialog.reject)

        dialog.setLayout(main_layout)
        dialog.exec()

    def edit_pest(self):
        """Редактирование вредителя"""
        selected = self.window.pests_table.currentRow()
        if selected >= 0:
            try:
                pest_id = int(self.window.pests_table.item(selected, 0).text())
                pest_name = self.window.pests_table.item(selected, 1).text()

                if not hasattr(self.service, 'Pest'):
                    self.show_warning_message("Ошибка", "Модель вредителей не найдена")
                    return

                pest = self.service.Pest.get_by_id(pest_id)

                dialog, main_layout = self.create_styled_dialog(f"Редактировать вредителя: {pest_name}", 500, 500)

                # Форма
                form_layout = QFormLayout()
                form_layout.setSpacing(10)

                # Поле "Название вредителя"
                name_input = self.create_styled_line_edit()
                name_input.setText(pest.name)
                name_label = QLabel("Название вредителя:")
                name_label.setStyleSheet("font-weight: bold; color: #485935;")
                form_layout.addRow(name_label, name_input)

                # Поле "Описание"
                description_input = self.create_styled_text_edit()
                description_input.setPlainText(pest.description or "")
                description_label = QLabel("Описание:")
                description_label.setStyleSheet("font-weight: bold; color: #485935;")
                form_layout.addRow(description_label, description_input)

                # Поле "Методы лечения"
                treatment_input = self.create_styled_text_edit()
                treatment_input.setPlainText(pest.treatment_methods or "")
                treatment_label = QLabel("Методы лечения:")
                treatment_label.setStyleSheet("font-weight: bold; color: #485935;")
                form_layout.addRow(treatment_label, treatment_input)

                main_layout.addLayout(form_layout)

                # Спейсер
                main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

                # Кнопки
                buttons_layout = QHBoxLayout()
                buttons_layout.setSpacing(15)

                ok_button = self.create_styled_button("Сохранить", "primary")
                cancel_button = self.create_styled_button("Отмена", "secondary")

                buttons_layout.addWidget(ok_button)
                buttons_layout.addWidget(cancel_button)
                main_layout.addLayout(buttons_layout)

                def save():
                    name = name_input.text().strip()
                    description = description_input.toPlainText().strip()
                    treatment = treatment_input.toPlainText().strip()

                    if not name:
                        self.show_warning_message("Ошибка", "Введите название вредителя")
                        return

                    try:
                        pest.name = name
                        pest.description = description if description else None
                        pest.treatment_methods = treatment if treatment else None
                        pest.save()

                        self.load_pests()
                        self.show_info_message("Успех", "Вредитель обновлен")
                        dialog.accept()
                    except Exception as e:
                        self.show_error_message("Ошибка", f"Ошибка: {str(e)}")

                ok_button.clicked.connect(save)
                cancel_button.clicked.connect(dialog.reject)

                dialog.setLayout(main_layout)
                dialog.exec()

            except self.service.Pest.DoesNotExist:
                self.show_error_message("Ошибка", "Вредитель не найден")
            except Exception as e:
                self.show_error_message("Ошибка", f"Ошибка: {str(e)}")
        else:
            self.show_warning_message("Внимание", "Выберите вредителя")

    def delete_pest(self):
        """Удаление вредителя"""
        selected = self.window.pests_table.currentRow()
        if selected >= 0:
            pest_name = self.window.pests_table.item(selected, 1).text()
            message = f"Удалить вредителя '{pest_name}'?" if pest_name else "Удалить вредителя?"

            if self.show_confirmation_dialog("Подтверждение", message):
                try:
                    pest_id = int(self.window.pests_table.item(selected, 0).text())

                    if not hasattr(self.service, 'Pest'):
                        self.show_warning_message("Ошибка", "Модель вредителей не найдена")
                        return

                    pest = self.service.Pest.get_by_id(pest_id)
                    pest.delete_instance()
                    self.reset_sequence(self.service.Pest)
                    self.load_pests()
                    self.show_info_message("Успех", "Вредитель удален")
                except self.service.Pest.DoesNotExist:
                    self.show_error_message("Ошибка", "Вредитель не найдена")
                except AttributeError:
                    self.show_warning_message("Ошибка", "Модель вредителей не поддерживает эту операцию")
                except Exception as e:
                    self.show_error_message("Ошибка", f"Ошибка: {str(e)}")
        else:
            self.show_warning_message("Внимание", "Выберите вредителя")

    def load_pests(self):
        """Загрузка вредителей с сортировкой по ID"""
        try:
            if hasattr(self.service, 'Pest'):
                pests = list(self.service.Pest.select().order_by(self.service.Pest.id).dicts())
                self.window.pests_table.setRowCount(len(pests))
                for i, pest in enumerate(pests):
                    self.window.pests_table.setItem(i, 0, QTableWidgetItem(str(pest['id'])))
                    self.window.pests_table.setItem(i, 1, QTableWidgetItem(pest.get('name', '')))
                    self.window.pests_table.setItem(i, 2, QTableWidgetItem(pest.get('description', '')))
                    self.window.pests_table.setItem(i, 3, QTableWidgetItem(pest.get('treatment_methods', '')))
            else:
                self.window.pests_table.setRowCount(0)
        except Exception as e:
            self.window.pests_table.setRowCount(0)
            print(f"Ошибка загрузки вредителей: {e}")

    # Методы для болезней
    def add_disease(self):
        """Добавление болезни"""
        dialog, main_layout = self.create_styled_dialog("Добавить болезнь", 500, 500)

        # Форма
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        # Поле "Название болезни"
        name_input = self.create_styled_line_edit("Введите название болезни")
        name_label = QLabel("Название болезни:")
        name_label.setStyleSheet("font-weight: bold; color: #485935;")
        form_layout.addRow(name_label, name_input)

        # Поле "Описание"
        description_input = self.create_styled_text_edit()
        description_label = QLabel("Описание:")
        description_label.setStyleSheet("font-weight: bold; color: #485935;")
        form_layout.addRow(description_label, description_input)

        # Поле "Методы лечения"
        treatment_input = self.create_styled_text_edit()
        treatment_label = QLabel("Методы лечения:")
        treatment_label.setStyleSheet("font-weight: bold; color: #485935;")
        form_layout.addRow(treatment_label, treatment_input)

        main_layout.addLayout(form_layout)

        # Спейсер
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        ok_button = self.create_styled_button("Сохранить", "primary")
        cancel_button = self.create_styled_button("Отмена", "secondary")

        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)
        main_layout.addLayout(buttons_layout)

        def save():
            name = name_input.text().strip()
            description = description_input.toPlainText().strip()
            treatment = treatment_input.toPlainText().strip()

            if not name:
                self.show_warning_message("Ошибка", "Введите название болезни")
                return

            try:
                if hasattr(self.service, 'Disease'):
                    self.service.Disease.create(
                        name=name,
                        description=description if description else None,
                        treatment_methods=treatment if treatment else None
                    )
                    self.load_diseases()
                    self.show_info_message("Успех", "Болезнь добавлена")
                    dialog.accept()
                else:
                    self.show_warning_message("Ошибка", "Модель болезней не найдена в базе данных")
            except Exception as e:
                self.show_error_message("Ошибка", f"Ошибка: {str(e)}")

        ok_button.clicked.connect(save)
        cancel_button.clicked.connect(dialog.reject)

        dialog.setLayout(main_layout)
        dialog.exec()

    def edit_disease(self):
        """Редактирование болезни"""
        selected = self.window.diseases_table.currentRow()
        if selected >= 0:
            try:
                disease_id = int(self.window.diseases_table.item(selected, 0).text())
                disease_name = self.window.diseases_table.item(selected, 1).text()

                if not hasattr(self.service, 'Disease'):
                    self.show_warning_message("Ошибка", "Модель болезней не найдена")
                    return

                disease = self.service.Disease.get_by_id(disease_id)

                dialog, main_layout = self.create_styled_dialog(f"Редактировать болезнь: {disease_name}", 500, 500)

                # Форма
                form_layout = QFormLayout()
                form_layout.setSpacing(10)

                # Поле "Название болезни"
                name_input = self.create_styled_line_edit()
                name_input.setText(disease.name)
                name_label = QLabel("Название болезни:")
                name_label.setStyleSheet("font-weight: bold; color: #485935;")
                form_layout.addRow(name_label, name_input)

                # Поле "Описание"
                description_input = self.create_styled_text_edit()
                description_input.setPlainText(disease.description or "")
                description_label = QLabel("Описание:")
                description_label.setStyleSheet("font-weight: bold; color: #485935;")
                form_layout.addRow(description_label, description_input)

                # Поле "Методы лечения"
                treatment_input = self.create_styled_text_edit()
                treatment_input.setPlainText(disease.treatment_methods or "")
                treatment_label = QLabel("Методы лечения:")
                treatment_label.setStyleSheet("font-weight: bold; color: #485935;")
                form_layout.addRow(treatment_label, treatment_input)

                main_layout.addLayout(form_layout)

                # Спейсер
                main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

                # Кнопки
                buttons_layout = QHBoxLayout()
                buttons_layout.setSpacing(15)

                ok_button = self.create_styled_button("Сохранить", "primary")
                cancel_button = self.create_styled_button("Отмена", "secondary")

                buttons_layout.addWidget(ok_button)
                buttons_layout.addWidget(cancel_button)
                main_layout.addLayout(buttons_layout)

                def save():
                    name = name_input.text().strip()
                    description = description_input.toPlainText().strip()
                    treatment = treatment_input.toPlainText().strip()

                    if not name:
                        self.show_warning_message("Ошибка", "Введите название болезни")
                        return

                    try:
                        disease.name = name
                        disease.description = description if description else None
                        disease.treatment_methods = treatment if treatment else None
                        disease.save()

                        self.load_diseases()
                        self.show_info_message("Успех", "Болезнь обновлена")
                        dialog.accept()
                    except Exception as e:
                        self.show_error_message("Ошибка", f"Ошибка: {str(e)}")

                ok_button.clicked.connect(save)
                cancel_button.clicked.connect(dialog.reject)

                dialog.setLayout(main_layout)
                dialog.exec()

            except self.service.Disease.DoesNotExist:
                self.show_error_message("Ошибка", "Болезнь не найдена")
            except Exception as e:
                self.show_error_message("Ошибка", f"Ошибка: {str(e)}")
        else:
            self.show_warning_message("Внимание", "Выберите болезнь")

    def delete_disease(self):
        """Удаление болезни"""
        selected = self.window.diseases_table.currentRow()
        if selected >= 0:
            disease_name = self.window.diseases_table.item(selected, 1).text()
            message = f"Удалить болезнь '{disease_name}'?" if disease_name else "Удалить болезнь?"

            if self.show_confirmation_dialog("Подтверждение", message):
                try:
                    disease_id = int(self.window.diseases_table.item(selected, 0).text())

                    if not hasattr(self.service, 'Disease'):
                        self.show_warning_message("Ошибка", "Модель болезней не найдена")
                        return

                    disease = self.service.Disease.get_by_id(disease_id)
                    disease.delete_instance()
                    self.reset_sequence(self.service.Disease)
                    self.load_diseases()
                    self.show_info_message("Успех", "Болезнь удалена")
                except self.service.Disease.DoesNotExist:
                    self.show_error_message("Ошибка", "Болезнь не найдена")
                except AttributeError:
                    self.show_warning_message("Ошибка", "Модель болезней не поддерживает эту операцию")
                except Exception as e:
                    self.show_error_message("Ошибка", f"Ошибка: {str(e)}")
        else:
            self.show_warning_message("Внимание", "Выберите болезнь")

    def load_diseases(self):
        """Загрузка болезней с сортировкой по ID"""
        try:
            if hasattr(self.service, 'Disease'):
                diseases = list(self.service.Disease.select().order_by(self.service.Disease.id).dicts())
                self.window.diseases_table.setRowCount(len(diseases))
                for i, disease in enumerate(diseases):
                    self.window.diseases_table.setItem(i, 0, QTableWidgetItem(str(disease['id'])))
                    self.window.diseases_table.setItem(i, 1, QTableWidgetItem(disease.get('name', '')))
                    self.window.diseases_table.setItem(i, 2, QTableWidgetItem(disease.get('description', '')))
                    self.window.diseases_table.setItem(i, 3, QTableWidgetItem(disease.get('treatment_methods', '')))
            else:
                self.window.diseases_table.setRowCount(0)
        except Exception as e:
            self.window.diseases_table.setRowCount(0)
            print(f"Ошибка загрузки болезней: {e}")



    # Методы для связей растений с семействами
    def add_plant_family_relation(self):
        """Добавление связи растение-семейство"""
        plants = list(self.service.Plant.select())
        families = list(self.service.PlantFamily.select())

        if not plants:
            self.show_warning_message("Ошибка", "Нет доступных растений")
            return
        if not families:
            self.show_warning_message("Ошибка", "Нет доступных семейств")
            return

        dialog, main_layout = self.create_styled_dialog("Добавить связь растение-семейство", 500, 300)

        # Форма
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        # Комбобокс для растений
        plant_combo = self.create_styled_combobox()
        plant_combo.addItem("Выберите растение", None)
        for plant in plants:
            plant_combo.addItem(f"{plant.id}: {plant.scientific_name}", plant.id)
        plant_label = QLabel("Растение:")
        plant_label.setStyleSheet("font-weight: bold; color: #485935;")
        form_layout.addRow(plant_label, plant_combo)

        # Комбобокс для семейств
        family_combo = self.create_styled_combobox()
        family_combo.addItem("Выберите семейство", None)
        for family in families:
            family_combo.addItem(f"{family.id}: {family.name}", family.id)
        family_label = QLabel("Семейство:")
        family_label.setStyleSheet("font-weight: bold; color: #485935;")
        form_layout.addRow(family_label, family_combo)

        main_layout.addLayout(form_layout)

        # Спейсер
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        ok_button = self.create_styled_button("Сохранить", "primary")
        cancel_button = self.create_styled_button("Отмена", "secondary")

        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)
        main_layout.addLayout(buttons_layout)

        def save():
            plant_id = plant_combo.currentData()
            family_id = family_combo.currentData()

            if not plant_id or not family_id:
                self.show_warning_message("Ошибка", "Выберите растение и семейство")
                return

            try:
                if hasattr(self.service, 'PlantFamilyRelation'):
                    existing = self.service.PlantFamilyRelation.select().where(
                        (self.service.PlantFamilyRelation.plant == plant_id) &
                        (self.service.PlantFamilyRelation.family == family_id)
                    ).first()

                    if existing:
                        self.show_warning_message("Ошибка", "Эта связь уже существует")
                        return

                    self.service.PlantFamilyRelation.create(
                        plant=plant_id,
                        family=family_id
                    )

                    self.load_plant_family_relations()
                    self.show_info_message("Успех", "Связь добавлена")
                    dialog.accept()
                else:
                    self.show_warning_message("Ошибка", "Модель связи растение-семейство не найдена")
            except Exception as e:
                self.show_error_message("Ошибка", f"Ошибка: {str(e)}")

        ok_button.clicked.connect(save)
        cancel_button.clicked.connect(dialog.reject)

        dialog.setLayout(main_layout)
        dialog.exec()

    def delete_plant_family_relation(self):
        """Удаление связи растение-семейство"""
        selected = self.window.plant_family_table.currentRow()
        if selected >= 0:
            plant_name = ""
            family_name = ""

            if self.window.plant_family_table.item(selected, 1):
                plant_name = self.window.plant_family_table.item(selected, 1).text()
            if self.window.plant_family_table.item(selected, 2):
                family_name = self.window.plant_family_table.item(selected, 2).text()

            message = f"Удалить связь растение-семейство?"
            if plant_name and family_name:
                message = f"Удалить связь '{plant_name}' - '{family_name}'?"

            if self.show_confirmation_dialog("Подтверждение", message):
                try:
                    relation_id = int(self.window.plant_family_table.item(selected, 0).text())

                    if hasattr(self.service, 'PlantFamilyRelation'):
                        relation = self.service.PlantFamilyRelation.get_by_id(relation_id)
                        relation.delete_instance()
                        self.reset_sequence(self.service.PlantFamilyRelation)
                        self.load_plant_family_relations()
                        self.show_info_message("Успех", "Связь удалена")
                    else:
                        self.show_warning_message("Ошибка", "Модель связи не найдена")

                except self.service.PlantFamilyRelation.DoesNotExist:
                    self.show_error_message("Ошибка", "Связь не найдена")
                except Exception as e:
                    self.show_error_message("Ошибка", f"Ошибка: {str(e)}")
        else:
            self.show_warning_message("Внимание", "Выберите связь")

    def load_plant_family_relations(self):
        """Загрузка связей растения-семейства с сортировкой по ID"""
        try:
            if hasattr(self.service, 'PlantFamilyRelation'):
                relations = list(self.service.PlantFamilyRelation.select(
                    self.service.PlantFamilyRelation,
                    self.service.Plant.scientific_name,
                    self.service.PlantFamily.name
                ).join(
                    self.service.Plant,
                    on=(self.service.PlantFamilyRelation.plant == self.service.Plant.id)
                ).join(
                    self.service.PlantFamily,
                    on=(self.service.PlantFamilyRelation.family == self.service.PlantFamily.id)
                ).order_by(self.service.PlantFamilyRelation.id).dicts())

                self.window.plant_family_table.setRowCount(len(relations))

                for i, rel in enumerate(relations):
                    self.window.plant_family_table.setItem(i, 0, QTableWidgetItem(str(rel['id'])))

                    plant_id = rel.get('plant_id') or (rel.get('plant') if isinstance(rel.get('plant'), int) else None)
                    family_id = rel.get('family_id') or (rel.get('family') if isinstance(rel.get('family'), int) else None)

                    self.window.plant_family_table.setItem(i, 1, QTableWidgetItem(str(plant_id) if plant_id else ''))
                    self.window.plant_family_table.setItem(i, 2, QTableWidgetItem(str(family_id) if family_id else ''))

                    plant_name = rel.get('scientific_name', f"ID: {plant_id}")
                    family_name = rel.get('name', f"ID: {family_id}")
                    self.window.plant_family_table.setItem(i, 3, QTableWidgetItem(f"{plant_name} → {family_name}"))
            else:
                self.window.plant_family_table.setRowCount(0)
        except Exception as e:
            self.window.plant_family_table.setRowCount(0)
            print(f"Ошибка загрузки связей растения-семейства: {e}")

    # Методы для связей растений с вредителями
    def add_plant_pest_relation(self):
        """Добавление связи растение-вредитель"""
        if not hasattr(self.service, 'Pest'):
            self.show_warning_message("Ошибка", "Модель вредителей не найдена")
            return

        plants = list(self.service.Plant.select())
        pests = list(self.service.Pest.select())

        if not plants:
            self.show_warning_message("Ошибка", "Нет доступных растений")
            return
        if not pests:
            self.show_warning_message("Ошибка", "Нет доступных вредителей")
            return

        dialog, main_layout = self.create_styled_dialog("Добавить связь растение-вредитель", 500, 300)

        # Форма
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        # Комбобокс для растений
        plant_combo = self.create_styled_combobox()
        plant_combo.addItem("Выберите растение", None)
        for plant in plants:
            plant_combo.addItem(f"{plant.id}: {plant.scientific_name}", plant.id)
        plant_label = QLabel("Растение:")
        plant_label.setStyleSheet("font-weight: bold; color: #485935;")
        form_layout.addRow(plant_label, plant_combo)

        # Комбобокс для вредителей
        pest_combo = self.create_styled_combobox()
        pest_combo.addItem("Выберите вредителя", None)
        for pest in pests:
            pest_combo.addItem(f"{pest.id}: {pest.name}", pest.id)
        pest_label = QLabel("Вредитель:")
        pest_label.setStyleSheet("font-weight: bold; color: #485935;")
        form_layout.addRow(pest_label, pest_combo)

        main_layout.addLayout(form_layout)

        # Спейсер
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        ok_button = self.create_styled_button("Сохранить", "primary")
        cancel_button = self.create_styled_button("Отмена", "secondary")

        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)
        main_layout.addLayout(buttons_layout)

        def save():
            plant_id = plant_combo.currentData()
            pest_id = pest_combo.currentData()

            if not plant_id or not pest_id:
                self.show_warning_message("Ошибка", "Выберите растение и вредителя")
                return

            try:
                if hasattr(self.service, 'PlantPest'):
                    existing = self.service.PlantPest.select().where(
                        (self.service.PlantPest.plant == plant_id) &
                        (self.service.PlantPest.pest == pest_id)
                    ).first()

                    if existing:
                        self.show_warning_message("Ошибка", "Эта связь уже существует")
                        return

                    self.service.PlantPest.create(
                        plant=plant_id,
                        pest=pest_id
                    )

                    self.load_plant_pest_relations()
                    self.show_info_message("Успех", "Связь добавлена")
                    dialog.accept()
                else:
                    self.show_warning_message("Ошибка", "Модель связи растение-вредитель не найдена")
            except Exception as e:
                self.show_error_message("Ошибка", f"Ошибка: {str(e)}")

        ok_button.clicked.connect(save)
        cancel_button.clicked.connect(dialog.reject)

        dialog.setLayout(main_layout)
        dialog.exec()

    def delete_plant_pest_relation(self):
        """Удаление связи растение-вредитель"""
        selected = self.window.plant_pest_table.currentRow()
        if selected >= 0:
            try:
                plant_name = ""
                pest_name = ""

                if self.window.plant_pest_table.item(selected, 3):
                    full_text = self.window.plant_pest_table.item(selected, 3).text()
                    if "→" in full_text:
                        parts = full_text.split("→")
                        plant_name = parts[0].strip()
                        pest_name = parts[1].strip() if len(parts) > 1 else ""

                message = "Удалить связь растение-вредитель?"
                if plant_name and pest_name:
                    message = f"Удалить связь '{plant_name}' - '{pest_name}'?"

                if self.show_confirmation_dialog("Подтверждение", message):
                    relation_id = int(self.window.plant_pest_table.item(selected, 0).text())

                    if hasattr(self.service, 'PlantPest'):
                        relation = self.service.PlantPest.get_by_id(relation_id)
                        relation.delete_instance()
                        self.reset_sequence(self.service.PlantPest)
                        self.load_plant_pest_relations()
                        self.show_info_message("Успех", "Связь растение-вредитель удалена")
                    else:
                        self.show_warning_message("Ошибка", "Модель связи не найдена")

            except self.service.PlantPest.DoesNotExist:
                self.show_error_message("Ошибка", "Связь не найдена")
            except Exception as e:
                self.show_error_message("Ошибка", f"Ошибка удаления связи: {str(e)}")
        else:
            self.show_warning_message("Внимание", "Выберите связь растение-вредитель")

    def load_plant_pest_relations(self):
        """Загрузка связей растения-вредители с сортировкой по ID"""
        try:
            if hasattr(self.service, 'PlantPest') and hasattr(self.service, 'Pest'):
                relations = list(self.service.PlantPest.select(
                    self.service.PlantPest,
                    self.service.Plant.scientific_name,
                    self.service.Pest.name
                ).join(
                    self.service.Plant,
                    on=(self.service.PlantPest.plant == self.service.Plant.id)
                ).join(
                    self.service.Pest,
                    on=(self.service.PlantPest.pest == self.service.Pest.id)
                ).order_by(self.service.PlantPest.id).dicts())

                self.window.plant_pest_table.setRowCount(len(relations))

                for i, rel in enumerate(relations):
                    self.window.plant_pest_table.setItem(i, 0, QTableWidgetItem(str(rel['id'])))

                    plant_id = rel.get('plant_id') or (rel.get('plant') if isinstance(rel.get('plant'), int) else None)
                    pest_id = rel.get('pest_id') or (rel.get('pest') if isinstance(rel.get('pest'), int) else None)

                    self.window.plant_pest_table.setItem(i, 1, QTableWidgetItem(str(plant_id) if plant_id else ''))
                    self.window.plant_pest_table.setItem(i, 2, QTableWidgetItem(str(pest_id) if pest_id else ''))

                    plant_name = rel.get('scientific_name', f"ID: {plant_id}")
                    pest_name = rel.get('name', f"ID: {pest_id}")
                    self.window.plant_pest_table.setItem(i, 3, QTableWidgetItem(f"{plant_name} → {pest_name}"))
            else:
                self.window.plant_pest_table.setRowCount(0)
        except Exception as e:
            self.window.plant_pest_table.setRowCount(0)
            print(f"Ошибка загрузки связей растения-вредители: {e}")

    # Методы для связей растений с болезнями
    def add_plant_disease_relation(self):
        """Добавление связи растение-болезнь"""
        if not hasattr(self.service, 'Disease'):
            self.show_warning_message("Ошибка", "Модель болезней не найдена")
            return

        plants = list(self.service.Plant.select())
        diseases = list(self.service.Disease.select())

        if not plants:
            self.show_warning_message("Ошибка", "Нет доступных растений")
            return
        if not diseases:
            self.show_warning_message("Ошибка", "Нет доступных болезней")
            return

        dialog, main_layout = self.create_styled_dialog("Добавить связь растение-болезнь", 500, 300)

        # Форма
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        # Комбобокс для растений
        plant_combo = self.create_styled_combobox()
        plant_combo.addItem("Выберите растение", None)
        for plant in plants:
            plant_combo.addItem(f"{plant.id}: {plant.scientific_name}", plant.id)
        plant_label = QLabel("Растение:")
        plant_label.setStyleSheet("font-weight: bold; color: #485935;")
        form_layout.addRow(plant_label, plant_combo)

        # Комбобокс для болезней
        disease_combo = self.create_styled_combobox()
        disease_combo.addItem("Выберите болезнь", None)
        for disease in diseases:
            disease_combo.addItem(f"{disease.id}: {disease.name}", disease.id)
        disease_label = QLabel("Болезнь:")
        disease_label.setStyleSheet("font-weight: bold; color: #485935;")
        form_layout.addRow(disease_label, disease_combo)

        main_layout.addLayout(form_layout)

        # Спейсер
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        ok_button = self.create_styled_button("Сохранить", "primary")
        cancel_button = self.create_styled_button("Отмена", "secondary")

        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)
        main_layout.addLayout(buttons_layout)

        def save():
            plant_id = plant_combo.currentData()
            disease_id = disease_combo.currentData()

            if not plant_id or not disease_id:
                self.show_warning_message("Ошибка", "Выберите растение и болезнь")
                return

            try:
                if hasattr(self.service, 'PlantDisease'):
                    existing = self.service.PlantDisease.select().where(
                        (self.service.PlantDisease.plant == plant_id) &
                        (self.service.PlantDisease.disease == disease_id)
                    ).first()

                    if existing:
                        self.show_warning_message("Ошибка", "Эта связь уже существует")
                        return

                    self.service.PlantDisease.create(
                        plant=plant_id,
                        disease=disease_id
                    )

                    self.load_plant_disease_relations()
                    self.show_info_message("Успех", "Связь добавлена")
                    dialog.accept()
                else:
                    self.show_warning_message("Ошибка", "Модель связи растение-болезнь не найдена")
            except Exception as e:
                self.show_error_message("Ошибка", f"Ошибка: {str(e)}")

        ok_button.clicked.connect(save)
        cancel_button.clicked.connect(dialog.reject)

        dialog.setLayout(main_layout)
        dialog.exec()

    def delete_plant_disease_relation(self):
        """Удаление связи растение-болезнь"""
        selected = self.window.plant_disease_table.currentRow()
        if selected >= 0:
            try:
                plant_name = ""
                disease_name = ""

                if self.window.plant_disease_table.item(selected, 3):
                    full_text = self.window.plant_disease_table.item(selected, 3).text()
                    if "→" in full_text:
                        parts = full_text.split("→")
                        plant_name = parts[0].strip()
                        disease_name = parts[1].strip() if len(parts) > 1 else ""

                message = "Удалить связь растение-болезнь?"
                if plant_name and disease_name:
                    message = f"Удалить связь '{plant_name}' - '{disease_name}'?"

                if self.show_confirmation_dialog("Подтверждение", message):
                    relation_id = int(self.window.plant_disease_table.item(selected, 0).text())

                    if hasattr(self.service, 'PlantDisease'):
                        relation = self.service.PlantDisease.get_by_id(relation_id)
                        relation.delete_instance()
                        self.reset_sequence(self.service.PlantDisease)
                        self.load_plant_disease_relations()
                        self.show_info_message("Успех", "Связь растение-болезнь удалена")
                    else:
                        self.show_warning_message("Ошибка", "Модель связи не найдена")

            except self.service.PlantDisease.DoesNotExist:
                self.show_error_message("Ошибка", "Связь не найдена")
            except Exception as e:
                self.show_error_message("Ошибка", f"Ошибка удаления связи: {str(e)}")
        else:
            self.show_warning_message("Внимание", "Выберите связь растение-болезнь")

    def load_plant_disease_relations(self):
        """Загрузка связей растения-болезни с сортировкой по ID"""
        try:
            if hasattr(self.service, 'PlantDisease') and hasattr(self.service, 'Disease'):
                relations = list(self.service.PlantDisease.select(
                    self.service.PlantDisease,
                    self.service.Plant.scientific_name,
                    self.service.Disease.name
                ).join(
                    self.service.Plant,
                    on=(self.service.PlantDisease.plant == self.service.Plant.id)
                ).join(
                    self.service.Disease,
                    on=(self.service.PlantDisease.disease == self.service.Disease.id)
                ).order_by(self.service.PlantDisease.id).dicts())

                self.window.plant_disease_table.setRowCount(len(relations))

                for i, rel in enumerate(relations):
                    self.window.plant_disease_table.setItem(i, 0, QTableWidgetItem(str(rel['id'])))

                    plant_id = rel.get('plant_id') or (rel.get('plant') if isinstance(rel.get('plant'), int) else None)
                    disease_id = rel.get('disease_id') or (rel.get('disease') if isinstance(rel.get('disease'), int) else None)

                    self.window.plant_disease_table.setItem(i, 1, QTableWidgetItem(str(plant_id) if plant_id else ''))
                    self.window.plant_disease_table.setItem(i, 2, QTableWidgetItem(str(disease_id) if disease_id else ''))

                    plant_name = rel.get('scientific_name', f"ID: {plant_id}")
                    disease_name = rel.get('name', f"ID: {disease_id}")
                    self.window.plant_disease_table.setItem(i, 3, QTableWidgetItem(f"{plant_name} → {disease_name}"))
            else:
                self.window.plant_disease_table.setRowCount(0)
        except Exception as e:
            self.window.plant_disease_table.setRowCount(0)
            print(f"Ошибка загрузки связей растения-болезни: {e}")

    # Методы экспорта
    def export_users(self):
        self.export_table("users", "Пользователи")

    def export_families(self):
        self.export_table("families", "Семейства растений")

    def export_care_guides(self):
        self.export_table("care_guides", "Руководства по уходу")

    def export_locations(self):
        self.export_table("locations", "Местоположения")

    def export_photos(self):
        self.export_table("photos", "Фотографии")

    def export_plants(self):
        self.export_table("plants", "Растения")

    def export_pests(self):
        self.export_table("pests", "Вредители")

    def export_diseases(self):
        self.export_table("diseases", "Болезни")

    def export_table(self, table_type, table_name):
        """Экспорт таблицы с выбором директории"""
        try:
            data = self.get_table_data(table_type)

            if not data:
                self.show_warning_message("Нет данных", "Нет данных для экспорта")
                return

            default_dir = os.path.join(os.path.expanduser("~"), "Desktop")
            directory = QFileDialog.getExistingDirectory(
                self.window,
                "Выберите директорию для сохранения",
                default_dir,
                QFileDialog.Option.ShowDirsOnly
            )

            if not directory:
                return

            format_ = self.window.export_format.currentText()
            filename = f"{table_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            filepath = None
            if format_ == "PDF":
                filepath = self.export_to_pdf(data, filename, directory, table_name)
            elif format_ == "DOCX":
                filepath = self.export_to_docx(data, filename, directory, table_name)

            if filepath and os.path.exists(filepath):
                dialog, main_layout = self.create_styled_dialog("Экспорт завершен", 450, 300)

                message = QLabel(f"Файл сохранен:\n{filepath}")
                message.setStyleSheet("""
                    QLabel {
                        font-size: 14px;
                        color: #2c3e50;
                        padding: 10px;
                    }
                """)
                message.setAlignment(Qt.AlignCenter)
                message.setWordWrap(True)
                main_layout.addWidget(message)

                icon_label = QLabel("✓")
                icon_label.setStyleSheet("""
                    QLabel {
                        font-size: 32px;
                        color: #27ae60;
                        font-weight: bold;
                    }
                """)
                icon_label.setAlignment(Qt.AlignCenter)
                main_layout.addWidget(icon_label)

                main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

                buttons_layout = QHBoxLayout()
                buttons_layout.setSpacing(15)

                open_button = self.create_styled_button("Открыть папку", "primary")
                ok_button = self.create_styled_button("OK", "secondary")

                def open_folder():
                    if os.name == 'nt':
                        os.startfile(os.path.dirname(filepath))
                    elif os.name == 'posix':
                        import subprocess
                        subprocess.call(['open' if sys.platform == 'darwin' else 'xdg-open',
                                       os.path.dirname(filepath)])

                open_button.clicked.connect(open_folder)
                ok_button.clicked.connect(dialog.accept)

                buttons_layout.addWidget(open_button)
                buttons_layout.addWidget(ok_button)
                main_layout.addLayout(buttons_layout)

                dialog.setLayout(main_layout)
                dialog.exec()
            else:
                self.show_error_message("Ошибка", "Не удалось создать файл экспорта")

        except Exception as e:
            self.show_error_message("Ошибка", f"Ошибка при экспорте:\n{str(e)}")

    def export_to_pdf(self, data, filename, directory, table_name):
        """Прямой экспорт в PDF"""
        try:
            from reportlab.lib.pagesizes import A4, landscape
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib import colors
            from reportlab.lib.units import cm
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            import os

            try:
                font_paths = [
                    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
                    'C:/Windows/Fonts/arial.ttf',
                    'C:/Windows/Fonts/tahoma.ttf',
                    'C:/Windows/Fonts/times.ttf',
                    './fonts/DejaVuSans.ttf',
                ]

                font_found = False
                for font_path in font_paths:
                    if os.path.exists(font_path):
                        pdfmetrics.registerFont(TTFont('RussianFont', font_path))
                        pdfmetrics.registerFont(TTFont('RussianFont-Bold', font_path))
                        font_found = True
                        break

                if not font_found:
                    russian_font = 'Helvetica'
            except Exception as e:
                print(f"Ошибка регистрации шрифта: {e}")
                russian_font = 'Helvetica'

            if not data:
                self.show_warning_message("Нет данных", "Нет данных для экспорта")
                return None

            pdf_filepath = os.path.join(directory, f"{filename}.pdf")

            if data and len(data[0]) > 6:
                pagesize = landscape(A4)
            else:
                pagesize = A4

            doc = SimpleDocTemplate(
                pdf_filepath,
                pagesize=pagesize,
                topMargin=2*cm,
                bottomMargin=2*cm,
                leftMargin=1.5*cm,
                rightMargin=1.5*cm
            )

            story = []
            styles = getSampleStyleSheet()

            if 'RussianFont' in pdfmetrics.getRegisteredFontNames():
                russian_font = 'RussianFont'
                styles['Title'].fontName = 'RussianFont-Bold'
                styles['Normal'].fontName = 'RussianFont'
            else:
                russian_font = 'Helvetica'

            title = Paragraph(f"Экспорт таблицы: {table_name}", styles['Title'])
            story.append(title)

            date_text = Paragraph(f"Дата экспорта: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
            story.append(date_text)

            count_text = Paragraph(f"Всего записей: {len(data)}", styles['Normal'])
            story.append(count_text)

            story.append(Spacer(1, 1*cm))

            if data:
                table_data = []
                headers = list(data[0].keys())
                formatted_headers = [h.replace('_', ' ') for h in headers]
                table_data.append(formatted_headers)

                for row in data:
                    table_row = []
                    for key in headers:
                        value = row.get(key, "")
                        if isinstance(value, str) and len(value) > 100:
                            value = value[:97] + "..."
                        table_row.append(str(value))
                    table_data.append(table_row)

                col_widths = [None] * len(headers)
                table = Table(table_data, colWidths=col_widths, repeatRows=1)

                table_style = [
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                    ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                    ('FONTSIZE', (0, 1), (-1, -1), 10),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.whitesmoke]),
                ]

                if 'RussianFont' in pdfmetrics.getRegisteredFontNames():
                    table_style.insert(3, ('FONTNAME', (0, 0), (-1, 0), 'RussianFont-Bold'))
                    table_style.insert(8, ('FONTNAME', (0, 1), (-1, -1), 'RussianFont'))
                else:
                    table_style.insert(3, ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'))
                    table_style.insert(8, ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'))

                table.setStyle(TableStyle(table_style))
                story.append(table)

            doc.build(story)
            return pdf_filepath

        except ImportError:
            self.show_error_message("Ошибка", "Для экспорта в PDF установите библиотеку:\npip install reportlab")
            return None
        except Exception as e:
            print(f"Ошибка прямого экспорта в PDF: {e}")
            import traceback
            traceback.print_exc()
            return None

    def export_to_docx(self, data, filename, directory, table_name):
        """Экспорт в DOCX файл"""
        try:
            from docx import Document
            from docx.shared import Inches, Pt, RGBColor
            from docx.enum.text import WD_ALIGN_PARAGRAPH
            from docx.enum.table import WD_TABLE_ALIGNMENT

            filepath = os.path.join(directory, f"{filename}.docx")
            doc = Document()

            title = doc.add_heading(f'Экспорт таблицы: {table_name}', 0)
            title.alignment = WD_ALIGN_PARAGRAPH.CENTER

            date_para = doc.add_paragraph()
            date_para.add_run(f'Дата экспорта: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

            if not data:
                doc.add_paragraph('Нет данных для экспорта')
            else:
                headers = list(data[0].keys())
                table = doc.add_table(rows=1, cols=len(headers))
                table.style = 'Table Grid'
                table.alignment = WD_TABLE_ALIGNMENT.CENTER

                header_cells = table.rows[0].cells
                for i, header in enumerate(headers):
                    header_cells[i].text = str(header)
                    header_para = header_cells[i].paragraphs[0]
                    header_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    run = header_para.runs[0]
                    run.bold = True
                    run.font.size = Pt(10)

                for row_data in data:
                    row_cells = table.add_row().cells
                    for i, header in enumerate(headers):
                        value = row_data.get(header, "")
                        if isinstance(value, datetime):
                            value = value.strftime('%Y-%m-%d %H:%M:%S')
                        elif value is None:
                            value = ""
                        else:
                            value = str(value)
                        row_cells[i].text = value
                        cell_para = row_cells[i].paragraphs[0]
                        cell_para.alignment = WD_ALIGN_PARAGRAPH.LEFT
                        run = cell_para.runs[0]
                        run.font.size = Pt(9)

                doc.add_paragraph()
                stats = doc.add_paragraph(f'Всего записей: {len(data)}')
                stats.alignment = WD_ALIGN_PARAGRAPH.RIGHT

            doc.save(filepath)
            return filepath

        except ImportError:
            self.show_error_message("Ошибка", "Для экспорта в DOCX установите библиотеку: pip install python-docx")
            return None
        except Exception as e:
            print(f"Ошибка экспорта в DOCX: {e}")
            return None

    def get_table_data(self, table_type):
        """Получение данных из разных таблиц с обработкой"""
        try:
            if table_type == "users":
                return self.prepare_export_data(self.service.User.select())
            elif table_type == "families":
                return self.prepare_export_data(self.service.PlantFamily.select())
            elif table_type == "care_guides":
                return self.prepare_export_data(self.service.CareGuide.select())
            elif table_type == "locations":
                return self.prepare_export_data(self.service.PlantLocation.select())
            elif table_type == "photos":
                return self.prepare_export_data(self.service.PlantPhoto.select())
            elif table_type == "plants":
                return self.prepare_export_data(self.service.Plant.select())
            elif table_type == "pests":
                return self.prepare_export_data(self.service.Pest.select())
            elif table_type == "diseases":
                return self.prepare_export_data(self.service.Disease.select())
            elif table_type == "plant_family_relations":
                return self.prepare_export_data(self.service.PlantFamilyRelation.select())
            elif table_type == "plant_pest_relations":
                return self.prepare_export_data(self.service.PlantPest.select())
            elif table_type == "plant_disease_relations":
                return self.prepare_export_data(self.service.PlantDisease.select())
            return []
        except Exception as e:
            print(f"Ошибка получения данных для экспорта: {e}")
            return []

    def prepare_export_data(self, query):
        """Подготовка данных для экспорта"""
        data = []

        try:
            items = list(query.dicts())

            for item in items:
                processed_item = {}
                for key, value in item.items():
                    if hasattr(value, 'strftime'):
                        processed_item[key] = value.strftime('%Y-%m-%d %H:%M:%S')
                    elif isinstance(value, bytes):
                        processed_item[key] = "[BINARY DATA]"
                    elif value is None:
                        processed_item[key] = ""
                    elif isinstance(value, (list, dict)):
                        processed_item[key] = str(value)
                    else:
                        processed_item[key] = value
                data.append(processed_item)

            return data

        except Exception as e:
            print(f"Ошибка подготовки данных: {e}")
            return []
