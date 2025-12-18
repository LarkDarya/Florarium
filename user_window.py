# windows/user_window.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLabel, QTableWidget, QTableWidgetItem,
                               QMessageBox, QTextEdit, QLineEdit, QComboBox,
                               QStackedWidget, QGroupBox, QFormLayout,
                               QFrame, QScrollArea, QSizePolicy, QGridLayout,
                               QDialog, QDateEdit, QSpinBox, QFileDialog, QSpacerItem,
                               QHeaderView)  # Добавлен QDialog
from PySide6.QtCore import Qt, QDate, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QFont, QIcon, QPixmap, QBrush, QColor  # Добавлен QPixmap
import os
from service import FlorariumService
from datetime import datetime

class UserWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.service = FlorariumService()
        self.sidebar_collapsed = False
        self.setup_ui()
        self.load_user_data()
        self.load_all_data()

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

    def create_styled_dialog(self, title, width=400, height=400):
        """Создание стилизованного диалогового окна"""
        dialog = QDialog(self)
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

    def setup_ui(self):
        """Настройка интерфейса пользователя с боковым меню"""
        self.setWindowTitle("Флорариум - Личный кабинет")
        self.resize(1200, 700)
        self.setStyleSheet("""
            QWidget {
                background-color: #FBFBFB;
            }
        """)

        # Главный layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Боковое меню
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(250)
        self.sidebar.setStyleSheet("""
            QFrame {
                background-color: #2C3E50;
                border: none;
            }
        """)

        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        # Кнопка сворачивания/разворачивания
        self.toggle_sidebar_btn = QPushButton("☰")
        self.toggle_sidebar_btn.setFixedHeight(50)
        self.toggle_sidebar_btn.setStyleSheet("""
            QPushButton {
                background-color: #1A252F;
                color: #ECF0F1;
                border: none;
                font-size: 20px;
                font-weight: bold;
                text-align: left;
                padding-left: 20px;
            }
            QPushButton:hover {
                background-color: #34495E;
            }
        """)
        self.toggle_sidebar_btn.clicked.connect(self.toggle_sidebar)
        sidebar_layout.addWidget(self.toggle_sidebar_btn)

        # Информация о пользователе в сайдбаре
        self.sidebar_user_info = QLabel()
        self.sidebar_user_info.setFixedHeight(100)
        self.sidebar_user_info.setStyleSheet("""
            QLabel {
                background-color: #1A252F;
                color: #ECF0F1;
                font-size: 14px;
                padding: 15px;
                border-bottom: 1px solid #34495E;
            }
        """)
        self.sidebar_user_info.setAlignment(Qt.AlignCenter)
        self.sidebar_user_info.setWordWrap(True)
        sidebar_layout.addWidget(self.sidebar_user_info)

        # Кнопки меню
        self.menu_buttons = []

        menu_items = [
            {"icon": "📚", "text": "Справочник растений", "id": "catalog"},
            {"icon": "🌱", "text": "Мои растения", "id": "my_plants"},
            {"icon": "📓", "text": "Журнал ухода", "id": "journal"},
            {"icon": "📊", "text": "Статистика", "id": "stats"},
            {"icon": "⚙️", "text": "Настройки", "id": "settings"},
            {"icon": "❓", "text": "Помощь", "id": "help"}
        ]

        for item in menu_items:
            btn = QPushButton(f"{item['icon']}  {item['text']}")
            btn.setObjectName(item['id'])
            btn.setFixedHeight(50)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #BDC3C7;
                    border: none;
                    font-size: 14px;
                    text-align: left;
                    padding-left: 20px;
                    border-bottom: 1px solid #34495E;
                }
                QPushButton:hover {
                    background-color: #34495E;
                    color: #ECF0F1;
                }
                QPushButton:pressed {
                    background-color: #1ABC9C;
                    color: white;
                }
            """)
            btn.clicked.connect(lambda checked, page_id=item['id']: self.switch_page(page_id))
            sidebar_layout.addWidget(btn)
            self.menu_buttons.append(btn)

        # Пустое пространство
        sidebar_layout.addStretch()

        # Кнопка выхода в сайдбаре
        self.sidebar_logout_btn = QPushButton("🚪  Выйти из системы")
        self.sidebar_logout_btn.setFixedHeight(50)
        self.sidebar_logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                border: none;
                font-size: 14px;
                font-weight: bold;
                text-align: center;
                margin: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        self.sidebar_logout_btn.clicked.connect(self.logout)
        sidebar_layout.addWidget(self.sidebar_logout_btn)

        self.content_area = QFrame()
        self.content_area.setStyleSheet("""
            QFrame {
                background-color: #FBFBFB;
                border: none;
            }
        """)

        content_layout = QVBoxLayout(self.content_area)
        content_layout.setContentsMargins(20, 20, 20, 20)

        # Заголовок страницы
        self.page_title = QLabel("Добро пожаловать!")
        self.page_title.setStyleSheet("""
            QLabel {
                color: #2C3E50;
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 20px;
            }
        """)
        content_layout.addWidget(self.page_title)

        # StackedWidget для страниц
        self.stacked_widget = QStackedWidget()
        content_layout.addWidget(self.stacked_widget)

        # Создаем страницы
        self.create_catalog_page()
        self.create_my_plants_page()
        self.create_journal_page()
        self.create_stats_page()
        self.create_settings_page()
        self.create_help_page()

        # Добавляем sidebar и content в главный layout
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_area, 1)  # 1 = растягивается

        self.setLayout(main_layout)

        # По умолчанию показываем первую страницу
        self.switch_page("catalog")
        self.set_active_button("catalog")

    def toggle_sidebar(self):
        """Свернуть/развернуть боковое меню"""
        if self.sidebar_collapsed:
            # Разворачиваем
            self.sidebar.setFixedWidth(250)
            for btn in self.menu_buttons:
                # Восстанавливаем полный текст
                btn_text = btn.text()
                icon = btn_text[0] if btn_text else ""
                for item in [{"icon": "📚", "text": "Справочник растений", "id": "catalog"},
                            {"icon": "🌱", "text": "Мои растения", "id": "my_plants"},
                            {"icon": "📓", "text": "Журнал ухода", "id": "journal"},
                            {"icon": "📊", "text": "Статистика", "id": "stats"},
                            {"icon": "⚙️", "text": "Настройки", "id": "settings"},
                            {"icon": "❓", "text": "Помощь", "id": "help"}]:
                    if btn.objectName() == item['id']:
                        btn.setText(f"{item['icon']}  {item['text']}")
                        break
            self.sidebar_logout_btn.setText("🚪  Выйти из системы")
        else:
            # Сворачиваем
            self.sidebar.setFixedWidth(60)
            for btn in self.menu_buttons:
                text = btn.text()
                if "  " in text:
                    btn.setText(text.split("  ")[0])
            self.sidebar_logout_btn.setText("🚪")

        self.sidebar_collapsed = not self.sidebar_collapsed

    def set_active_button(self, button_id):
        """Установить активную кнопку меню"""
        for btn in self.menu_buttons:
            if btn.objectName() == button_id:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #1ABC9C;
                        color: white;
                        border: none;
                        font-size: 14px;
                        text-align: left;
                        padding-left: 20px;
                        border-bottom: 1px solid #34495E;
                        border-left: 4px solid #16A085;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        color: #BDC3C7;
                        border: none;
                        font-size: 14px;
                        text-align: left;
                        padding-left: 20px;
                        border-bottom: 1px solid #34495E;
                    }
                    QPushButton:hover {
                        background-color: #34495E;
                        color: #ECF0F1;
                    }
                """)

    def switch_page(self, page_id):
        """Переключить страницу"""
        self.set_active_button(page_id)

        page_titles = {
            "catalog": "📚 Справочник растений",
            "my_plants": "🌱 Мои растения",
            "journal": "📓 Журнал ухода",
            "stats": "📊 Статистика",
            "settings": "⚙️ Настройки",
            "help": "❓ Помощь"
        }

        self.page_title.setText(page_titles.get(page_id, "Добро пожаловать!"))

        # Загружаем данные при переходе на страницу журнала
        if page_id == "journal":
            self.load_plant_combo()
            self.load_journal()

        # Обновляем при переходе на Мои растения
        if page_id == "my_plants":
            self.load_my_plants()

        # Показываем соответствующую страницу
        page_index = {
            "catalog": 0,
            "my_plants": 1,
            "journal": 2,
            "stats": 3,
            "settings": 4,
            "help": 5
        }.get(page_id, 0)

        self.stacked_widget.setCurrentIndex(page_index)




    # СОЗДАНИЕ СТРАНИЦ

    def create_catalog_page(self):
        """Создать страницу справочника растений в виде галереи"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(20)

        # Панель поиска
        search_container = QFrame()
        search_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 15px;
                border: 2px solid #E8F5E9;
            }
        """)

        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(10, 10, 10, 10)

        # Заголовок поиска
        search_header = QLabel("🔍 Поиск растения")
        search_header.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 16px;
                color: #2C3E50;
                padding-right: 15px;
            }
        """)
        search_layout.addWidget(search_header)

        # Поле поиска
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите название растения...")
        self.search_input.setMinimumHeight(40)
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px 15px;
                border: 2px solid #93a267;
                border-radius: 8px;
                font-size: 14px;
                background-color: white;
                selection-background-color: #93a267;
            }
            QLineEdit:focus {
                border: 2px solid #1ABC9C;
            }
            QLineEdit::placeholder {
                color: #95A5A6;
                font-style: italic;
            }
        """)
        search_layout.addWidget(self.search_input, 3)  # 3 = коэффициент растяжения

        # Кнопки поиска
        button_style = """
            QPushButton {
                background-color: #93a267;
                color: white;
                border: none;
                padding: 0 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
                min-width: 100px;
                height: 40px;
            }
            QPushButton:hover {
                background-color: #7a8a53;
            }
            QPushButton:pressed {
                background-color: #6a7949;
            }
        """

        self.btn_search = QPushButton("🔍 Найти")
        self.btn_search.setStyleSheet(button_style)

        self.btn_clear = QPushButton("🗑️ Сбросить")
        self.btn_clear.setStyleSheet(button_style.replace("#93a267", "#95A5A6")
                                           .replace("#7a8a53", "#7F8C8D")
                                           .replace("#6a7949", "#6C7A89"))

        search_layout.addWidget(self.btn_search)
        search_layout.addWidget(self.btn_clear)

        layout.addWidget(search_container)

        # Создаем scroll area для прокрутки
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.NoFrame)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #F0F0F0;
                width: 10px;
                border-radius: 5px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #93a267;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #71804e;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)

        # Контейнер для карточек
        self.gallery_container = QWidget()
        self.gallery_layout = QGridLayout(self.gallery_container)
        self.gallery_layout.setSpacing(25)
        self.gallery_layout.setContentsMargins(10, 10, 10, 10)
        self.gallery_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        scroll_area.setWidget(self.gallery_container)
        layout.addWidget(scroll_area, 1)  # 1 = растягивается

        # Подключение сигналов
        self.btn_search.clicked.connect(self.search_plants)
        self.btn_clear.clicked.connect(self.clear_search)

        self.stacked_widget.addWidget(page)

    def display_plants(self, plants):
        """Отображение растений в виде карточек-галереи"""
        for i in reversed(range(self.gallery_layout.count())):
            widget = self.gallery_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        if not plants:
            # Сообщение "нет растений"
            empty_label = QLabel("Растения не найдены")
            empty_label.setStyleSheet("""
                QLabel {
                    color: #7F8C8D;
                    font-size: 18px;
                    font-weight: bold;
                    padding: 50px;
                }
            """)
            empty_label.setAlignment(Qt.AlignCenter)
            self.gallery_layout.addWidget(empty_label, 0, 0, 1, 3, Qt.AlignCenter)
            return

        # Создаем карточки растений
        row, col = 0, 0
        max_columns = 3  # Можно уменьшить до 2 или 1 если нужно больше места

        for plant in plants:
            # Создаем карточку
            card = self.create_plant_card(plant)

            # Добавляем в сетку
            self.gallery_layout.addWidget(card, row, col, Qt.AlignTop)

            # Переходим к следующей ячейке
            col += 1
            if col >= max_columns:
                col = 0
                row += 1

        self.gallery_layout.setRowStretch(row + 1, 1)

    def create_plant_card(self, plant):
        """Создание простых карточек растений"""
        card = QFrame()
        card.setFixedSize(240, 320)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 12px;
                padding: 0px;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)

        # Верхняя часть - фото
        photo_container = QWidget()
        photo_container.setFixedHeight(180)
        photo_container.setStyleSheet("""
            QWidget {
                background-color: #F8F9FA;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }
        """)

        photo_layout = QVBoxLayout(photo_container)
        photo_layout.setContentsMargins(0, 0, 0, 0)
        photo_layout.setAlignment(Qt.AlignCenter)

        # Создаем QLabel для фото
        photo_label = QLabel()
        photo_label.setFixedSize(160, 160)
        photo_label.setAlignment(Qt.AlignCenter)

        photo_loaded = False

        try:
            plant_obj = self.service.Plant.get_by_id(plant['id'])

            if plant_obj.main_photo:
                photo = plant_obj.main_photo
                photo_path = photo.photo_url

                if photo_path:
                    if not os.path.isabs(photo_path):
                        base_dir = os.path.dirname(os.path.abspath(__file__))
                        photo_path = os.path.join(base_dir, photo_path)

                    if os.path.exists(photo_path):
                        pixmap = QPixmap(photo_path)
                        if not pixmap.isNull():
                            pixmap = pixmap.scaled(160, 160,
                                                  Qt.KeepAspectRatio,
                                                  Qt.SmoothTransformation)
                            photo_label.setPixmap(pixmap)
                            photo_loaded = True
        except Exception as e:
            print(f"Ошибка загрузки фото для растения {plant['id']}: {e}")

        if not photo_loaded:
            photo_label.setText("🌿\nНет фото")
            photo_label.setStyleSheet("""
                QLabel {
                    color: #7F8C8D;
                    font-size: 16px;
                    font-weight: bold;
                }
            """)

        photo_layout.addWidget(photo_label)
        card_layout.addWidget(photo_container)

        # Средняя часть - название растения
        name_container = QWidget()  # Меняем QFrame на QWidget!
        name_container.setFixedHeight(80)
        name_container.setStyleSheet("""
            QWidget {
                background-color: white;
                padding: 10px;
            }
        """)

        name_layout = QVBoxLayout(name_container)
        name_layout.setContentsMargins(10, 5, 10, 5)

        plant_name = plant.get('scientific_name', 'Без названия')

        name_label = QLabel(plant_name)
        name_label.setStyleSheet("""
            QLabel {
                color: #2C3E50;
                font-weight: bold;
                font-size: 16px;
                max-width: 220px;
                padding: 2px;
            }
        """)
        name_label.setWordWrap(True)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setMinimumHeight(40)

        name_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        name_layout.addWidget(name_label)
        card_layout.addWidget(name_container)

        button_container = QWidget()
        button_container.setFixedHeight(60)
        button_container.setStyleSheet("""
            QWidget {
                background-color: white;
                padding: 10px;
            }
        """)

        button_layout = QVBoxLayout(button_container)
        button_layout.setContentsMargins(20, 5, 20, 5)

        details_btn = QPushButton("🔍 Подробнее")
        details_btn.setFixedHeight(35)
        details_btn.setCursor(Qt.PointingHandCursor)
        details_btn.setStyleSheet("""
            QPushButton {
                background-color: #93a267;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7a8a53;
            }
            QPushButton:pressed {
                background-color: #6a7949;
            }
        """)
        details_btn.clicked.connect(lambda checked, p=plant: self.show_plant_details_window(p))

        button_layout.addWidget(details_btn)
        card_layout.addWidget(button_container)

        return card

    def show_plant_details_window(self, plant_data):
        """Открыть окно с детальной информацией о растении"""
        dialog = QDialog(self)
        dialog.setWindowTitle(f"🌿 {plant_data['scientific_name']}")
        dialog.setFixedSize(700, 500)

        dialog.setStyleSheet("""
            QDialog {
                background-color: #F5F5F5;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #E0E0E0;
                width: 10px;
                border-radius: 5px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #93a267;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #71804e;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)

        main_layout = QVBoxLayout(dialog)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(12)

        try:
            # Получаем полную информацию о растении
            plant = self.service.Plant.get_by_id(plant_data['id'])

            # Заголовок
            title_label = QLabel(plant.scientific_name)
            title_label.setStyleSheet("""
                QLabel {
                    font-size: 22px;
                    font-weight: bold;
                    color: #2C3E50;
                    padding-bottom: 8px;
                    border-bottom: 2px solid #93a267;
                    margin-bottom: 10px;
                }
            """)
            main_layout.addWidget(title_label)

            # Scroll area для содержимого с нормальной прокруткой
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setFrameStyle(QScrollArea.NoFrame)
            scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

            content_widget = QWidget()
            content_layout = QVBoxLayout(content_widget)
            content_layout.setContentsMargins(0, 0, 10, 0)
            content_layout.setSpacing(10)

            # Фотогалерея растения
            try:
                photos = list(self.service.PlantPhoto.select().where(
                    self.service.PlantPhoto.plant == plant
                ))

                if photos:
                    photos_label = QLabel("📷 Фотографии растения:")
                    photos_label.setStyleSheet("""
                        font-weight: bold;
                        color: #485935;
                        font-size: 15px;
                        margin-bottom: 5px;
                    """)
                    content_layout.addWidget(photos_label)

                    photos_scroll = QScrollArea()
                    photos_scroll.setFixedHeight(130)
                    photos_scroll.setWidgetResizable(True)
                    photos_scroll.setFrameStyle(QScrollArea.NoFrame)
                    photos_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
                    photos_widget = QWidget()
                    photos_hbox = QHBoxLayout(photos_widget)
                    photos_hbox.setSpacing(8)

                    photos_scroll.setWidget(photos_widget)
                    content_layout.addWidget(photos_scroll)
            except Exception as e:
                print(f"Ошибка загрузки фото: {e}")

            # Стиль для всех информационных блоков
            section_label_style = """
                font-weight: bold;
                color: #485935;
                font-size: 15px;
                margin-top: 8px;
                margin-bottom: 3px;
            """

            section_content_style = """
                font-size: 13px;
                color: #34495E;
                padding: 10px;
                background-color: white;
                border-radius: 6px;
                border: 1px solid #DDD;
                line-height: 1.4;
            """

            # Описание
            if plant.description:
                desc_label = QLabel("📝 Описание:")
                desc_label.setStyleSheet(section_label_style)
                content_layout.addWidget(desc_label)

                desc_text = QLabel(plant.description)
                desc_text.setWordWrap(True)
                desc_text.setStyleSheet(section_content_style)
                content_layout.addWidget(desc_text)

            # Информация об уходе
            if hasattr(plant, 'care_guide') and plant.care_guide:
                care_label = QLabel("💧 Уход за растением:")
                care_label.setStyleSheet(section_label_style)
                content_layout.addWidget(care_label)

                care = plant.care_guide
                care_info = QFrame()
                care_info.setStyleSheet(section_content_style)
                care_layout = QVBoxLayout(care_info)
                care_layout.setSpacing(4)
                care_layout.setContentsMargins(0, 5, 0, 5)

                if care.watering:
                    care_layout.addWidget(QLabel(f"💦 <b>Полив:</b> {care.watering}"))
                if care.light:
                    care_layout.addWidget(QLabel(f"☀️ <b>Свет:</b> {care.light} люминов"))
                if care.temperature_min and care.temperature_max:
                    care_layout.addWidget(QLabel(f"🌡️ <b>Температура мин:</b> {care.temperature_min}°C"))
                    care_layout.addWidget(QLabel(f"🌡️ <b>Температура макс:</b> {care.temperature_max}°C"))
                if care.soil:
                    care_layout.addWidget(QLabel(f"🌱 <b>Почва:</b> {care.soil}"))
                if care.fertilizers:
                    care_layout.addWidget(QLabel(f"🧪 <b>Удобрения:</b> {care.fertilizers}"))
                if care.humidity:
                    care_layout.addWidget(QLabel(f"💧 <b>Влажность:</b> {care.humidity}%"))

                # Добавляем рамку ухода в основной контент
                content_layout.addWidget(care_info)

            # Семейства
            try:
                families = list(self.service.PlantFamilyRelation.select().where(
                    self.service.PlantFamilyRelation.plant == plant
                ))
                if families:
                    families_label = QLabel("🌳 Семейства:")
                    families_label.setStyleSheet(section_label_style)
                    content_layout.addWidget(families_label)

                    family_list = []
                    for fam in families:
                        if hasattr(fam, 'family') and fam.family:
                            family_list.append(fam.family.name)

                    if family_list:
                        families_text = QLabel(", ".join(family_list))
                        families_text.setWordWrap(True)
                        families_text.setStyleSheet(section_content_style)
                        content_layout.addWidget(families_text)
            except Exception as e:
                print(f"Ошибка загрузки семейств: {e}")

            # Местоположение
            if hasattr(plant, 'main_location') and plant.main_location:
                location_label = QLabel("📍 Местоположение:")
                location_label.setStyleSheet(section_label_style)
                content_layout.addWidget(location_label)

                location_info = QLabel(f"<b>{plant.main_location.location_name}</b>")
                if plant.main_location.description:
                    location_info.setText(f"<b>{plant.main_location.location_name}</b><br>{plant.main_location.description}")
                location_info.setWordWrap(True)
                location_info.setStyleSheet(section_content_style)
                content_layout.addWidget(location_info)

            # Вредители
            try:
                pests = list(self.service.PlantPest.select().where(
                    self.service.PlantPest.plant == plant
                ))
                if pests:
                    pests_label = QLabel("🐛 Вредители:")
                    pests_label.setStyleSheet(section_label_style)
                    content_layout.addWidget(pests_label)

                    pest_list = []
                    for pest_relation in pests:
                        if hasattr(pest_relation, 'pest') and pest_relation.pest:
                            pest_list.append(pest_relation.pest.name)

                    if pest_list:
                        pests_text = QLabel(", ".join(pest_list))
                        pests_text.setWordWrap(True)
                        pests_text.setStyleSheet(section_content_style)
                        content_layout.addWidget(pests_text)
            except Exception as e:
                print(f"Ошибка загрузки вредителей: {e}")

            # Болезни
            try:
                diseases = list(self.service.PlantDisease.select().where(
                    self.service.PlantDisease.plant == plant
                ))
                if diseases:
                    diseases_label = QLabel("🤒 Болезни:")
                    diseases_label.setStyleSheet(section_label_style)
                    content_layout.addWidget(diseases_label)

                    disease_list = []
                    for disease_relation in diseases:
                        if hasattr(disease_relation, 'disease') and disease_relation.disease:
                            disease_list.append(disease_relation.disease.name)

                    if disease_list:
                        diseases_text = QLabel(", ".join(disease_list))
                        diseases_text.setWordWrap(True)
                        diseases_text.setStyleSheet(section_content_style)
                        content_layout.addWidget(diseases_text)
            except Exception as e:
                print(f"Ошибка загрузки болезней: {e}")

            # Пустое пространство внизу
            content_layout.addStretch()

            scroll_area.setWidget(content_widget)
            main_layout.addWidget(scroll_area)

            # Кнопка закрытия
            btn_close = QPushButton("Закрыть")
            btn_close.setFixedHeight(40)
            btn_close.setStyleSheet("""
                QPushButton {
                    background-color: #93a267;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 8px 20px;
                    font-weight: bold;
                    font-size: 14px;
                    min-width: 100px;
                }
                QPushButton:hover {
                    background-color: #71804e;
                }
                QPushButton:pressed {
                    background-color: #5a663c;
                }
            """)
            btn_close.clicked.connect(dialog.accept)
            main_layout.addWidget(btn_close)

        except Exception as e:
            error_label = QLabel(f"Ошибка загрузки данных растения: {str(e)}")
            error_label.setStyleSheet("color: #E74C3C; font-weight: bold; padding: 10px;")
            main_layout.addWidget(error_label)

        # Центрируем окно
        dialog.move(
            self.x() + (self.width() - dialog.width()) // 2,
            self.y() + (self.height() - dialog.height()) // 2
        )

        dialog.exec()

    def search_plants(self):
        """Поиск растений"""
        search_text = self.search_input.text().strip()
        if not search_text:
            self.load_plants()
            return

        try:
            plants = list(self.service.Plant.select().where(
                self.service.Plant.scientific_name.contains(search_text) |
                self.service.Plant.description.contains(search_text)
            ).dicts())
            self.display_plants(plants)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка поиска: {str(e)}")

    def clear_search(self):
        """Очистка поиска"""
        self.search_input.clear()
        self.load_plants()

    def create_my_plants_page(self):
        """Создать страницу 'Мои растения' в виде галереи"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(20)

        # Панель управления
        control_container = QFrame()
        control_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 15px;
                border: 2px solid #E8F5E9;
            }
        """)

        control_layout = QHBoxLayout(control_container)
        control_layout.setContentsMargins(10, 10, 10, 10)

        # Заголовок
        header_label = QLabel("🌿 Мои растения")
        header_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 18px;
                color: #2C3E50;
                padding-right: 20px;
            }
        """)
        control_layout.addWidget(header_label)

        # Стиль кнопок
        button_style = """
            QPushButton {
                background-color: #93a267;
                color: white;
                border: none;
                padding: 0 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
                min-width: 100px;
                height: 40px;
            }
            QPushButton:hover {
                background-color: #7a8a53;
            }
            QPushButton:pressed {
                background-color: #6a7949;
            }
        """

        delete_button_style = button_style.replace("#93a267", "#e74c3c") \
                                         .replace("#7a8a53", "#c0392b") \
                                         .replace("#6a7949", "#a93226")

        # Кнопки управления
        self.btn_add_my_plant = QPushButton("➕ Добавить")
        self.btn_add_my_plant.setStyleSheet(button_style)

        self.btn_edit_my_plant = QPushButton("✏️ Редактировать")
        self.btn_edit_my_plant.setStyleSheet(button_style)

        self.btn_delete_my_plant = QPushButton("🗑️ Удалить")
        self.btn_delete_my_plant.setStyleSheet(delete_button_style)

        self.btn_refresh_my_plants = QPushButton("🔄 Обновить")
        self.btn_refresh_my_plants.setStyleSheet(button_style)

        control_layout.addWidget(self.btn_add_my_plant)
        control_layout.addWidget(self.btn_edit_my_plant)
        control_layout.addWidget(self.btn_delete_my_plant)
        control_layout.addWidget(self.btn_refresh_my_plants)
        control_layout.addStretch()

        layout.addWidget(control_container)

        # Панель поиска
        search_container = QFrame()
        search_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 15px;
                border: 2px solid #E8F5E9;
            }
        """)

        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(10, 10, 10, 10)

        # Заголовок поиска
        search_header = QLabel("🔍 Поиск в моих растениях")
        search_header.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 16px;
                color: #2C3E50;
                padding-right: 15px;
            }
        """)
        search_layout.addWidget(search_header)

        # Поле поиска
        self.search_my_plants_input = QLineEdit()
        self.search_my_plants_input.setPlaceholderText("Введите название растения...")
        self.search_my_plants_input.setMinimumHeight(40)
        self.search_my_plants_input.setStyleSheet("""
            QLineEdit {
                padding: 8px 15px;
                border: 2px solid #93a267;
                border-radius: 8px;
                font-size: 14px;
                background-color: white;
                selection-background-color: #93a267;
            }
            QLineEdit:focus {
                border: 2px solid #1ABC9C;
            }
            QLineEdit::placeholder {
                color: #95A5A6;
                font-style: italic;
            }
        """)
        search_layout.addWidget(self.search_my_plants_input, 3)

        # Кнопки поиска
        self.btn_search_my_plants = QPushButton("🔍 Найти")
        self.btn_search_my_plants.setStyleSheet(button_style)

        self.btn_clear_my_plants = QPushButton("🗑️ Сбросить")
        self.btn_clear_my_plants.setStyleSheet(button_style.replace("#93a267", "#95A5A6")
                                                           .replace("#7a8a53", "#7F8C8D")
                                                           .replace("#6a7949", "#6C7A89"))

        search_layout.addWidget(self.btn_search_my_plants)
        search_layout.addWidget(self.btn_clear_my_plants)

        layout.addWidget(search_container)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.NoFrame)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #F0F0F0;
                width: 10px;
                border-radius: 5px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #93a267;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #71804e;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)

        # Контейнер для карточек
        self.my_plants_container = QWidget()
        self.my_plants_layout = QGridLayout(self.my_plants_container)
        self.my_plants_layout.setSpacing(25)
        self.my_plants_layout.setContentsMargins(10, 10, 10, 10)
        self.my_plants_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        scroll_area.setWidget(self.my_plants_container)
        layout.addWidget(scroll_area, 1)

        # Подключение сигналов
        self.btn_add_my_plant.clicked.connect(self.add_my_plant)
        def on_container_click(event):
            self.clear_selection()

        self.my_plants_container.mousePressEvent = on_container_click

        self.btn_edit_my_plant.clicked.connect(self.edit_my_plant)
        self.btn_delete_my_plant.clicked.connect(self.delete_my_plant)
        self.btn_refresh_my_plants.clicked.connect(self.load_my_plants)
        self.btn_search_my_plants.clicked.connect(self.search_my_plants)
        self.btn_clear_my_plants.clicked.connect(self.clear_my_plants_search)

        self.stacked_widget.addWidget(page)

    def clear_selection(self):
        """Сбросить выделение карточки"""
        if hasattr(self, 'selected_plant_card'):
            delattr(self, 'selected_plant_card')
        if hasattr(self, 'selected_plant_data'):
            delattr(self, 'selected_plant_data')
        self.update_my_plants_cards_style()

    def display_my_plants(self, plants):
        """Отображение моих растений в виде карточек-галереи"""
        for i in reversed(range(self.my_plants_layout.count())):
            widget = self.my_plants_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        if not plants:
            # Сообщение "нет растений"
            empty_label = QLabel("У вас пока нет растений\nНажмите 'Добавить', чтобы добавить первое растение")
            empty_label.setStyleSheet("""
                QLabel {
                    color: #7F8C8D;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 50px;
                    text-align: center;
                }
            """)
            empty_label.setAlignment(Qt.AlignCenter)
            self.my_plants_layout.addWidget(empty_label, 0, 0, 1, 3, Qt.AlignCenter)
            return

        # Создаем карточки растений
        row, col = 0, 0
        max_columns = 3

        for plant in plants:
            # Создаем карточку
            card = self.create_my_plant_card(plant)
            self.my_plants_layout.addWidget(card, row, col, Qt.AlignTop)

            # Переходим к следующей ячейке
            col += 1
            if col >= max_columns:
                col = 0
                row += 1

        # Добавляем растягивающийся элемент для правильного выравнивания
        self.my_plants_layout.setRowStretch(row + 1, 1)

    def create_my_plant_card(self, plant):
        """Создать карточку для моего растения"""
        card = QFrame()
        card.setFixedSize(240, 320)

        # Храним ID растения в объекте карточки
        card.plant_id = plant.get('id')
        card.plant_data = plant

        # Проверяем, выбрана ли эта карточка
        is_selected = hasattr(self, 'selected_plant_card') and self.selected_plant_card == card.plant_id

        # Стиль зависит от выбора
        if is_selected:
            card_style = """
                QFrame {
                    background-color: white;
                    border: 3px solid #93a267;
                    border-radius: 12px;
                    padding: 0px;
                }
            """
        else:
            card_style = """
                QFrame {
                    background-color: white;
                    border: 1px solid #E0E0E0;
                    border-radius: 12px;
                    padding: 0px;
                }
            """

        card.setStyleSheet(card_style)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)

        # Верхняя часть - фото
        photo_container = QWidget()
        photo_container.setFixedHeight(180)
        photo_container.setStyleSheet("""
            QWidget {
                background-color: #F8F9FA;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }
        """)

        photo_layout = QVBoxLayout(photo_container)
        photo_layout.setContentsMargins(0, 0, 0, 0)
        photo_layout.setAlignment(Qt.AlignCenter)

        # Создаем QLabel для фото
        photo_label = QLabel()
        photo_label.setFixedSize(160, 160)
        photo_label.setAlignment(Qt.AlignCenter)

        # Пытаемся загрузить фотографию растения
        photo_loaded = False

        try:
            # Для моих растений используем PlantInstance
            plant_id = plant.get('id')
            if plant_id:
                plant_obj = self.service.PlantInstance.get_by_id(plant_id)

                # Пытаемся получить фото из InstancePhoto
                try:
                    instance_photos = list(self.service.InstancePhoto.select().where(
                        self.service.InstancePhoto.instance == plant_obj,
                        self.service.InstancePhoto.is_current == True
                    ))

                    if instance_photos:
                        photo_path = instance_photos[0].photo_url

                        if photo_path:
                            if not os.path.isabs(photo_path):
                                base_dir = os.path.dirname(os.path.abspath(__file__))
                                photo_path = os.path.join(base_dir, photo_path)

                            if os.path.exists(photo_path):
                                pixmap = QPixmap(photo_path)
                                if not pixmap.isNull():
                                    pixmap = pixmap.scaled(160, 160,
                                                          Qt.KeepAspectRatio,
                                                          Qt.SmoothTransformation)
                                    photo_label.setPixmap(pixmap)
                                    photo_loaded = True
                except Exception as photo_e:
                    print(f"Ошибка загрузки фото для экземпляра растения {plant_id}: {photo_e}")

        except Exception as e:
            print(f"Ошибка загрузки растения пользователя {plant.get('id')}: {e}")

        if not photo_loaded:
            photo_label.setText("🌿\nНет фото")
            photo_label.setStyleSheet("""
                QLabel {
                    color: #7F8C8D;
                    font-size: 16px;
                    font-weight: bold;
                }
            """)

        photo_layout.addWidget(photo_label)
        card_layout.addWidget(photo_container)

        # Средняя часть - название растения
        name_container = QWidget()
        name_container.setFixedHeight(80)
        name_container.setStyleSheet("""
            QWidget {
                background-color: white;
                padding: 10px;
            }
        """)

        name_layout = QVBoxLayout(name_container)
        name_layout.setContentsMargins(10, 5, 10, 5)

        plant_name = plant.get('nickname', 'Мое растение')
        if not plant_name or plant_name == 'None':
            plant_name = 'Мое растение'

        name_label = QLabel(plant_name)
        name_label.setStyleSheet("""
            QLabel {
                color: #2C3E50;
                font-weight: bold;
                font-size: 16px;
                max-width: 220px;
                padding: 2px;
            }
        """)
        name_label.setWordWrap(True)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setMinimumHeight(40)
        name_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        name_layout.addWidget(name_label)
        card_layout.addWidget(name_container)

        # Нижняя часть - кнопка
        button_container = QWidget()
        button_container.setFixedHeight(60)
        button_container.setStyleSheet("""
            QWidget {
                background-color: white;
                padding: 10px;
            }
        """)

        button_layout = QVBoxLayout(button_container)
        button_layout.setContentsMargins(20, 5, 20, 5)

        details_btn = QPushButton("🔍 Подробнее")
        details_btn.setFixedHeight(35)
        details_btn.setCursor(Qt.PointingHandCursor)
        details_btn.setStyleSheet("""
            QPushButton {
                background-color: #93a267;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7a8a53;
            }
            QPushButton:pressed {
                background-color: #6a7949;
            }
        """)
        details_btn.clicked.connect(lambda: self.show_my_plant_details_window(plant))

        button_layout.addWidget(details_btn)
        card_layout.addWidget(button_container)

        # Добавляем обработчик клика
        def on_card_clicked(event):
            event.accept()

            # Проверяем, не выбрана ли уже эта карточка
            if hasattr(self, 'selected_plant_card') and self.selected_plant_card == card.plant_id:
                self.clear_selection()
            else:
                # Сохраняем выбранное растение
                self.selected_plant_card = card.plant_id
                self.selected_plant_data = card.plant_data
                self.update_my_plants_cards_style()

        card.mousePressEvent = on_card_clicked
        card.setCursor(Qt.PointingHandCursor)

        return card

    def show_my_plant_details_window(self, plant_data):
        """Открыть окно с детальной информацией о растении пользователя"""
        dialog = QDialog(self)

        try:
            plant = self.service.PlantInstance.get_by_id(plant_data['id'])

            # Получаем имя для заголовка окна
            plant_name = plant.nickname if plant.nickname and plant.nickname != 'None' else 'Мое растение'
            dialog.setWindowTitle(f"🌿 {plant_name}")
        except:
            dialog.setWindowTitle("🌿 Мое растение")

        dialog.setFixedSize(700, 500)

        dialog.setStyleSheet("""
            QDialog {
                background-color: #F5F5F5;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #E0E0E0;
                width: 10px;
                border-radius: 5px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #93a267;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #71804e;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)

        main_layout = QVBoxLayout(dialog)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(12)

        try:
            # Получаем полную информацию о растении
            plant = self.service.PlantInstance.get_by_id(plant_data['id'])

            # Заголовок - используем никнейм или "Мое растение"
            display_name = plant.nickname if plant.nickname and plant.nickname != 'None' else 'Мое растение'
            title_label = QLabel(display_name)
            title_label.setStyleSheet("""
                QLabel {
                    font-size: 22px;
                    font-weight: bold;
                    color: #2C3E50;
                    padding-bottom: 8px;
                    border-bottom: 2px solid #93a267;
                    margin-bottom: 10px;
                }
            """)
            main_layout.addWidget(title_label)

            # Scroll area для содержимого
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setFrameStyle(QScrollArea.NoFrame)
            scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

            content_widget = QWidget()
            content_layout = QVBoxLayout(content_widget)
            content_layout.setContentsMargins(0, 0, 10, 0)
            content_layout.setSpacing(10)

            section_label_style = """
                font-weight: bold;
                color: #485935;
                font-size: 15px;
                margin-top: 8px;
                margin-bottom: 3px;
            """

            section_content_style = """
                font-size: 13px;
                color: #34495E;
                padding: 10px;
                background-color: white;
                border-radius: 6px;
                border: 1px solid #DDD;
                line-height: 1.4;
            """

            # Никнейм
            if plant.nickname and plant.nickname != 'None':
                nickname_label = QLabel("🏷️ Прозвище:")
                nickname_label.setStyleSheet(section_label_style)
                content_layout.addWidget(nickname_label)

                nickname_info = QLabel(plant.nickname)
                nickname_info.setStyleSheet(section_content_style)
                content_layout.addWidget(nickname_info)

            # Описание
            if plant.description and plant.description != 'None':
                desc_label = QLabel("📝 Описание:")
                desc_label.setStyleSheet(section_label_style)
                content_layout.addWidget(desc_label)

                desc_text = QLabel(plant.description)
                desc_text.setWordWrap(True)
                desc_text.setStyleSheet(section_content_style)
                content_layout.addWidget(desc_text)

            # Дата приобретения
            if plant.acquisition_date:
                date_label = QLabel("📅 Дата приобретения:")
                date_label.setStyleSheet(section_label_style)
                content_layout.addWidget(date_label)

                date_info = QLabel(str(plant.acquisition_date))
                date_info.setStyleSheet(section_content_style)
                content_layout.addWidget(date_info)

            # Возраст
            if plant.age:
                age_label = QLabel("🎂 Возраст:")
                age_label.setStyleSheet(section_label_style)
                content_layout.addWidget(age_label)

                age_info = QLabel(f"{plant.age} месяцев")
                age_info.setStyleSheet(section_content_style)
                content_layout.addWidget(age_info)

            # Состояние
            if plant.health_status:
                health_label = QLabel("💚 Состояние здоровья:")
                health_label.setStyleSheet(section_label_style)
                content_layout.addWidget(health_label)

                status_dict = {
                    'excellent': 'Отличное 🌟',
                    'good': 'Хорошее ✅',
                    'fair': 'Среднее ⚠️',
                    'poor': 'Плохое ❗',
                    'critical': 'Критическое 💀'
                }
                status = status_dict.get(plant.health_status, plant.health_status)
                health_info = QLabel(status)
                health_info.setStyleSheet(section_content_style)
                content_layout.addWidget(health_info)

            # Местоположение
            if plant.room and plant.room != 'None':
                location_label = QLabel("📍 Комната:")
                location_label.setStyleSheet(section_label_style)
                content_layout.addWidget(location_label)

                location_info = QLabel(plant.room)
                location_info.setStyleSheet(section_content_style)
                content_layout.addWidget(location_info)

            # Примечания к местоположению
            if plant.location_notes and plant.location_notes != 'None':
                notes_label = QLabel("📌 Примечания к местоположению:")
                notes_label.setStyleSheet(section_label_style)
                content_layout.addWidget(notes_label)

                notes_info = QLabel(plant.location_notes)
                notes_info.setWordWrap(True)
                notes_info.setStyleSheet(section_content_style)
                content_layout.addWidget(notes_info)

            # График полива
            if hasattr(plant, 'watering_schedule') and plant.watering_schedule and plant.watering_schedule != 'None':
                water_label = QLabel("💧 График полива:")
                water_label.setStyleSheet(section_label_style)
                content_layout.addWidget(water_label)

                water_info = QLabel(plant.watering_schedule)
                water_info.setStyleSheet(section_content_style)
                content_layout.addWidget(water_info)

            # Индивидуальный уход
            if hasattr(plant, 'custom_care_notes') and plant.custom_care_notes and plant.custom_care_notes != 'None':
                care_label = QLabel("🌱 Индивидуальный уход:")
                care_label.setStyleSheet(section_label_style)
                content_layout.addWidget(care_label)

                care_info = QLabel(plant.custom_care_notes)
                care_info.setWordWrap(True)
                care_info.setStyleSheet(section_content_style)
                content_layout.addWidget(care_info)

            # Дата создания
            if hasattr(plant, 'created_at') and plant.created_at:
                created_label = QLabel("📅 Дата добавления:")
                created_label.setStyleSheet(section_label_style)
                content_layout.addWidget(created_label)

                created_info = QLabel(str(plant.created_at))
                created_info.setStyleSheet(section_content_style)
                content_layout.addWidget(created_info)

            # Пустое пространство внизу
            content_layout.addStretch()

            scroll_area.setWidget(content_widget)
            main_layout.addWidget(scroll_area)

            # Кнопка закрытия
            btn_close = QPushButton("Закрыть")
            btn_close.setFixedHeight(40)
            btn_close.setStyleSheet("""
                QPushButton {
                    background-color: #93a267;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 8px 20px;
                    font-weight: bold;
                    font-size: 14px;
                    min-width: 100px;
                }
                QPushButton:hover {
                    background-color: #71804e;
                }
                QPushButton:pressed {
                    background-color: #5a663c;
                }
            """)
            btn_close.clicked.connect(dialog.accept)
            main_layout.addWidget(btn_close)

        except Exception as e:
            error_label = QLabel(f"Ошибка загрузки данных растения: {str(e)}")
            error_label.setStyleSheet("color: #E74C3C; font-weight: bold; padding: 10px;")
            main_layout.addWidget(error_label)

        # Центрируем окно
        dialog.move(
            self.x() + (self.width() - dialog.width()) // 2,
            self.y() + (self.height() - dialog.height()) // 2
        )

        dialog.exec()

    def search_my_plants(self):
        """Поиск в моих растениях"""
        search_text = self.search_my_plants_input.text().strip()
        if not search_text:
            self.load_my_plants()
            return

        try:
            my_plants = list(self.service.UserPlant.select().where(
                self.service.UserPlant.name.contains(search_text) |
                self.service.UserPlant.notes.contains(search_text)
            ).dicts())
            self.display_my_plants(my_plants)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка поиска: {str(e)}")

    def clear_my_plants_search(self):
        """Очистка поиска в моих растениях"""
        self.search_my_plants_input.clear()
        self.load_my_plants()


    def create_journal_page(self):
        """Создать страницу журнала ухода"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(20)

        # Панель управления
        control_container = QFrame()
        control_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 15px;
                border: 2px solid #E8F5E9;
            }
        """)

        control_layout = QHBoxLayout(control_container)
        control_layout.setContentsMargins(10, 10, 10, 10)

        # Заголовок
        header_label = QLabel("📓 Журнал ухода")
        header_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 18px;
                color: #2C3E50;
                padding-right: 20px;
            }
        """)
        control_layout.addWidget(header_label)

        # Стиль кнопок
        button_style = """
            QPushButton {
                background-color: #93a267;
                color: white;
                border: none;
                padding: 0 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
                min-width: 100px;
                height: 40px;
            }
            QPushButton:hover {
                background-color: #7a8a53;
            }
            QPushButton:pressed {
                background-color: #6a7949;
            }
        """

        delete_button_style = button_style.replace("#93a267", "#e74c3c") \
                                         .replace("#7a8a53", "#c0392b") \
                                         .replace("#6a7949", "#a93226")

        # Кнопки управления
        self.btn_add_journal = QPushButton("➕ Добавить")
        self.btn_add_journal.setStyleSheet(button_style)

        self.btn_edit_journal = QPushButton("✏️ Редактировать")
        self.btn_edit_journal.setStyleSheet(button_style)

        self.btn_delete_journal = QPushButton("🗑️ Удалить")
        self.btn_delete_journal.setStyleSheet(delete_button_style)

        self.btn_refresh_journal = QPushButton("🔄 Обновить")
        self.btn_refresh_journal.setStyleSheet(button_style)

        control_layout.addWidget(self.btn_add_journal)
        control_layout.addWidget(self.btn_edit_journal)
        control_layout.addWidget(self.btn_delete_journal)
        control_layout.addWidget(self.btn_refresh_journal)
        control_layout.addStretch()

        layout.addWidget(control_container)

        # Панель поиска
        search_container = QFrame()
        search_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 15px;
                border: 2px solid #E8F5E9;
            }
        """)

        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(10, 10, 10, 10)

        # Заголовок поиска
        search_header = QLabel("🔍 Поиск в журнале")
        search_header.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 16px;
                color: #2C3E50;
                padding-right: 15px;
            }
        """)
        search_layout.addWidget(search_header)

        # Поле поиска
        self.journal_search_input = QLineEdit()
        self.journal_search_input.setPlaceholderText("Поиск по заметкам, типу ухода...")
        self.journal_search_input.setMinimumHeight(40)
        self.journal_search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px 15px;
                border: 2px solid #93a267;
                border-radius: 8px;
                font-size: 14px;
                background-color: white;
                selection-background-color: #93a267;
            }
            QLineEdit:focus {
                border: 2px solid #1ABC9C;
            }
            QLineEdit::placeholder {
                color: #95A5A6;
                font-style: italic;
            }
        """)
        search_layout.addWidget(self.journal_search_input, 3)

        # Кнопки поиска
        self.btn_search_journal = QPushButton("🔍 Найти")
        self.btn_search_journal.setStyleSheet(button_style)

        self.btn_clear_journal = QPushButton("🗑️ Сбросить")
        self.btn_clear_journal.setStyleSheet(button_style.replace("#93a267", "#95A5A6")
                                                         .replace("#7a8a53", "#7F8C8D")
                                                         .replace("#6a7949", "#6C7A89"))

        search_layout.addWidget(self.btn_search_journal)
        search_layout.addWidget(self.btn_clear_journal)

        layout.addWidget(search_container)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.NoFrame)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #F0F0F0;
                width: 10px;
                border-radius: 5px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #93a267;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #71804e;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)

        # Контейнер для карточек журнала
        self.journal_cards_container = QWidget()
        self.journal_cards_layout = QVBoxLayout(self.journal_cards_container)
        self.journal_cards_layout.setSpacing(10)
        self.journal_cards_layout.setContentsMargins(10, 10, 10, 10)
        self.journal_cards_layout.setAlignment(Qt.AlignTop)

        scroll_area.setWidget(self.journal_cards_container)
        layout.addWidget(scroll_area, 1)

        # Подключение сигналов
        self.btn_add_journal.clicked.connect(self.add_journal_dialog)
        self.btn_edit_journal.clicked.connect(self.edit_journal_entry)
        self.btn_delete_journal.clicked.connect(self.delete_journal_entry)
        self.btn_refresh_journal.clicked.connect(self.load_journal_cards)
        self.btn_search_journal.clicked.connect(self.search_journal)
        self.btn_clear_journal.clicked.connect(self.clear_journal_search)

        def on_journal_container_click(event):
            if hasattr(self, 'selected_journal_card'):
                self.clear_journal_selection()

        self.journal_cards_container.mousePressEvent = on_journal_container_click

        self.stacked_widget.addWidget(page)

    def create_journal_card(self, journal_data):
        """Создать горизонтальную карточку для записи журнала с кнопкой 'Подробнее'"""
        card = QFrame()
        card.setFixedHeight(100)
        card.setMinimumWidth(400)

        # Проверяем, выбрана ли эта карточка
        is_selected = hasattr(self, 'selected_journal_card') and self.selected_journal_card == journal_data.get('id')

        if is_selected:
            card_style = """
                QFrame {
                    background-color: white;
                    border: 3px solid #93a267;
                    border-radius: 10px;
                    padding: 0px;
                }
            """
        else:
            card_style = """
                QFrame {
                    background-color: white;
                    border: 1px solid #E0E0E0;
                    border-radius: 10px;
                    padding: 0px;
                }
                QFrame:hover {
                    background-color: #F8F9FA;
                    border: 1px solid #93a267;
                }
            """

        card.setStyleSheet(card_style)
        card.setCursor(Qt.PointingHandCursor)

        # Сохраняем ID записи в объекте карточки
        card.journal_id = journal_data.get('id')
        card.journal_data = journal_data

        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(15, 10, 15, 10)
        card_layout.setSpacing(15)

        # Иконка в зависимости от типа ухода
        care_type_icons = {
            "Полив": "💦",
            "Удобрение": "🧪",
            "Пересадка": "🔄",
            "Обрезка": "✂️",
            "Опрыскивание": "💨",
            "Другое": "📝"
        }

        care_type = journal_data.get('care_type', 'Другое')
        icon_text = care_type_icons.get(care_type, "📝")

        # Иконка
        icon_frame = QFrame()
        icon_frame.setFixedSize(50, 50)
        icon_frame.setStyleSheet("""
            QFrame {
                background-color: #E8F5E9;
                border-radius: 25px;
            }
        """)
        icon_layout = QVBoxLayout(icon_frame)
        icon_layout.setAlignment(Qt.AlignCenter)
        icon_label = QLabel(icon_text)
        icon_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
            }
        """)
        icon_layout.addWidget(icon_label)
        card_layout.addWidget(icon_frame)

        # Основная информация
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)
        info_layout.setContentsMargins(0, 0, 0, 0)

        # Дата и время
        date_text = "Дата неизвестна"
        if journal_data.get('care_date'):
            try:
                from datetime import datetime, date

                care_date = journal_data['care_date']

                if isinstance(care_date, datetime):
                    date_text = care_date.strftime('%d.%m.%Y')
                elif isinstance(care_date, date):
                    date_text = care_date.strftime('%d.%m.%Y')
                elif isinstance(care_date, str):
                    try:
                        for fmt in ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%d.%m.%Y', '%d.%m.%Y %H:%M']:
                            try:
                                parsed_date = datetime.strptime(care_date, fmt)
                                date_text = parsed_date.strftime('%d.%m.%Y')
                                break
                            except:
                                continue
                    except:
                        date_text = care_date[:10] if len(care_date) >= 10 else care_date
            except Exception as e:
                print(f"Ошибка форматирования даты: {e}")
                date_text = str(journal_data['care_date'])[:10]

        date_label = QLabel(f"📅 {date_text}")
        date_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #7F8C8D;
            }
        """)
        info_layout.addWidget(date_label)

        # Растение и тип ухода
        plant_text = journal_data.get('plant_name', 'Неизвестное растение')
        main_label = QLabel(f"🌿 <b>{plant_text}</b>  |  🛠️ {care_type}")
        main_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #2C3E50;
            }
        """)
        main_label.setWordWrap(True)
        info_layout.addWidget(main_label)

        # Краткие заметки
        notes = journal_data.get('description', journal_data.get('notes', ''))
        if notes and notes.strip():
            notes_preview = notes[:30] + "..." if len(notes) > 30 else notes
            notes_label = QLabel(f"📌 {notes_preview}")
            notes_label.setStyleSheet("""
                QLabel {
                    font-size: 12px;
                    color: #485935;
                    font-style: italic;
                }
            """)
            notes_label.setWordWrap(True)
            info_layout.addWidget(notes_label)

        card_layout.addLayout(info_layout, 1)  # 1 = растягивается

        # Кнопка "Подробнее"
        details_btn = QPushButton("🔍 Подробнее")
        details_btn.setFixedSize(100, 30)
        details_btn.setStyleSheet("""
            QPushButton {
                background-color: #93a267;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #71804e;
            }
            QPushButton:pressed {
                background-color: #5a663c;
            }
        """)
        details_btn.clicked.connect(lambda: self.show_journal_details(journal_data))
        card_layout.addWidget(details_btn)

        # Обработчик клика на всю карточку
        def on_card_click(event):
            event.accept()
            if hasattr(self, 'selected_journal_card') and self.selected_journal_card == card.journal_id:
                self.clear_journal_selection()
            else:
                self.selected_journal_card = card.journal_id
                self.selected_journal_data = card.journal_data
                self.update_journal_cards_style()

        card.mousePressEvent = on_card_click

        return card

    def show_journal_details(self, journal_data):
        """Показать детали записи журнала в отдельном окне"""
        dialog = self.create_details_style_dialog("📓 Детали записи журнала", 500, 400)

        try:
            # Получаем полную запись из базы
            journal_record = self.service.CareJournal.get_by_id(journal_data['id'])

            # Получаем растение
            plant_name = journal_data.get('plant_name', 'Неизвестное растение')
            try:
                if journal_record.instance:
                    plant = journal_record.instance
                    if plant.nickname and plant.nickname != 'None':
                        plant_name = plant.nickname
                    elif hasattr(plant, 'plant') and plant.plant:
                        if hasattr(plant.plant, 'scientific_name'):
                            plant_name = plant.plant.scientific_name
            except:
                pass

            date_text = "Дата неизвестна"
            if journal_record.care_date:
                try:
                    from datetime import datetime, date

                    care_date = journal_record.care_date

                    if isinstance(care_date, datetime):
                        date_text = care_date.strftime('%d.%m.%Y %H:%M')
                    elif isinstance(care_date, date):
                        date_text = care_date.strftime('%d.%m.%Y')
                    elif isinstance(care_date, str):
                        date_text = care_date[:19] if len(care_date) >= 19 else care_date
                except Exception as e:
                    print(f"Ошибка форматирования даты: {e}")
                    date_text = str(journal_record.care_date)

            # Создаем информационные блоки
            info_style = """
                font-size: 14px;
                color: #34495E;
                padding: 12px;
                background-color: white;
                border-radius: 8px;
                border: 1px solid #DDD;
                line-height: 1.4;
            """

            # Растение
            plant_label = QLabel(f"<b>🌿 Растение:</b> {plant_name}")
            plant_label.setStyleSheet(info_style)
            self.dialog_content_layout.addWidget(plant_label)

            # Тип ухода
            type_label = QLabel(f"<b>🛠️ Тип ухода:</b> {journal_record.care_type or 'Не указан'}")
            type_label.setStyleSheet(info_style)
            self.dialog_content_layout.addWidget(type_label)

            # Дата и время
            date_label = QLabel(f"<b>📅 Дата и время:</b> {date_text}")
            date_label.setStyleSheet(info_style)
            self.dialog_content_layout.addWidget(date_label)

            # Описание
            description = journal_record.description or ""
            if description:
                notes_label = QLabel(f"<b>📝 Заметки:</b><br>{description}")
                notes_label.setWordWrap(True)
                notes_label.setStyleSheet(info_style)
                self.dialog_content_layout.addWidget(notes_label)

            self.dialog_content_layout.addStretch()

            # Кнопка закрытия
            btn_close = QPushButton("Закрыть")
            btn_close.setFixedHeight(40)
            btn_close.setStyleSheet("""
                QPushButton {
                    background-color: #93a267;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 8px 20px;
                    font-weight: bold;
                    font-size: 14px;
                    min-width: 100px;
                }
                QPushButton:hover {
                    background-color: #71804e;
                }
                QPushButton:pressed {
                    background-color: #5a663c;
                }
            """)
            btn_close.clicked.connect(dialog.accept)

            # Добавляем кнопку в layout
            self.dialog_button_layout.addStretch()
            self.dialog_button_layout.addWidget(btn_close)

            # Центрируем окно
            dialog.move(
                self.x() + (self.width() - dialog.width()) // 2,
                self.y() + (self.height() - dialog.height()) // 2
            )

            dialog.exec()

        except Exception as e:
            error_label = QLabel(f"Ошибка загрузки данных записи: {str(e)}")
            error_label.setStyleSheet("color: #E74C3C; font-weight: bold; padding: 10px;")
            self.dialog_content_layout.addWidget(error_label)

    def clear_journal_selection(self):
        """Сбросить выделение карточки журнала"""
        if hasattr(self, 'selected_journal_card'):
            delattr(self, 'selected_journal_card')
        if hasattr(self, 'selected_journal_data'):
            delattr(self, 'selected_journal_data')
        self.update_journal_cards_style()

    def update_journal_cards_style(self):
        """Обновить стили всех карточек журнала (подсветить выбранную)"""
        for i in range(self.journal_cards_layout.count()):
            widget = self.journal_cards_layout.itemAt(i).widget()
            if widget and hasattr(widget, 'journal_id'):
                is_selected = hasattr(self, 'selected_journal_card') and self.selected_journal_card == widget.journal_id
                if is_selected:
                    widget.setStyleSheet("""
                        QFrame {
                            background-color: white;
                            border: 3px solid #93a267;
                            border-radius: 10px;
                            padding: 0px;
                        }
                    """)
                else:
                    widget.setStyleSheet("""
                        QFrame {
                            background-color: white;
                            border: 1px solid #E0E0E0;
                            border-radius: 10px;
                            padding: 0px;
                        }
                        QFrame:hover {
                            background-color: #F8F9FA;
                            border: 1px solid #93a267;
                        }
                    """)

    def search_journal(self):
        """Поиск в журнале"""
        search_text = self.journal_search_input.text().strip()
        if not search_text:
            self.load_journal_cards()
            return

        try:
            # Ищем записи журнала
            records = list(self.service.CareJournal.select().where(
                (self.service.CareJournal.user == self.user_id) &
                (
                    (self.service.CareJournal.care_type.contains(search_text)) |
                    (self.service.CareJournal.description.contains(search_text))
                )
            ).order_by(self.service.CareJournal.care_date.desc()))

            self.display_journal_cards(records)
        except Exception as e:
            print(f"Ошибка поиска в журнале: {e}")
            self.show_error_message("Ошибка", f"Ошибка поиска: {str(e)}")

    def clear_journal_search(self):
        """Очистка поиска в журнале"""
        self.journal_search_input.clear()
        self.load_journal_cards()


    def load_plant_combo(self):
        """Загрузить растения пользователя в комбобокс журнала"""
        try:
            my_plants = list(self.service.PlantInstance.select().where(
                self.service.PlantInstance.user == self.user_id
            ))

            if len(my_plants) == 0:
                print("У пользователя нет растений для журнала")
                return False
            else:
                print(f"У пользователя {len(my_plants)} растений для журнала")
                return True

        except Exception as e:
            print(f"Ошибка проверки растений для журнала: {e}")
            return False

    def load_journal_cards(self):
        """Загрузить записи журнала в виде карточек"""
        try:
            # Очищаем контейнер
            for i in reversed(range(self.journal_cards_layout.count())):
                widget = self.journal_cards_layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()

            # Получаем записи журнала
            records = list(self.service.CareJournal.select().where(
                self.service.CareJournal.user == self.user_id
            ).order_by(self.service.CareJournal.care_date.desc()))

            if not records:
                # Сообщение если нет записей
                empty_label = QLabel("📝 Нет записей в журнале\nДобавьте первую запись")
                empty_label.setStyleSheet("""
                    QLabel {
                        color: #7F8C8D;
                        font-size: 16px;
                        font-weight: bold;
                        padding: 40px;
                        text-align: center;
                    }
                """)
                empty_label.setAlignment(Qt.AlignCenter)
                self.journal_cards_layout.addWidget(empty_label)
                return

            # Создаем карточки для каждой записи
            for record in records:
                try:
                    journal_data = {
                        'id': record.id,
                        'care_type': record.care_type or "Другое",
                        'care_date': record.care_date,
                        'description': record.description or "",
                    }

                    # Получаем имя растения
                    plant_name = "Неизвестное растение"
                    if hasattr(record, 'instance') and record.instance:
                        try:
                            plant = record.instance
                            if plant.nickname and plant.nickname != 'None':
                                plant_name = plant.nickname
                            elif hasattr(plant, 'plant') and plant.plant:
                                if hasattr(plant.plant, 'scientific_name'):
                                    plant_name = plant.plant.scientific_name
                        except:
                            pass

                    journal_data['plant_name'] = plant_name

                    # Создаем карточку
                    card = self.create_journal_card(journal_data)
                    self.journal_cards_layout.addWidget(card)

                except Exception as card_e:
                    print(f"Ошибка создания карточки: {card_e}")
                    continue

            self.journal_cards_layout.addStretch()

        except Exception as e:
            print(f"Ошибка загрузки журнала: {e}")
            error_label = QLabel("⚠️ Ошибка загрузки журнала")
            error_label.setStyleSheet("""
                QLabel {
                    color: #e74c3c;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 20px;
                    text-align: center;
                }
            """)
            error_label.setAlignment(Qt.AlignCenter)
            self.journal_cards_layout.addWidget(error_label)

    def display_journal_cards(self, records):
        """Отобразить записи журнала в виде карточек"""
        for i in reversed(range(self.journal_cards_layout.count())):
            widget = self.journal_cards_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        if not records:
            # Сообщение если нет записей
            empty_label = QLabel("📝 Записи не найдены")
            empty_label.setStyleSheet("""
                QLabel {
                    color: #7F8C8D;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 40px;
                    text-align: center;
                }
            """)
            empty_label.setAlignment(Qt.AlignCenter)
            self.journal_cards_layout.addWidget(empty_label)
            return

        # Создаем карточки для каждой записи
        for record in records:
            try:
                journal_data = {
                    'id': record.id,
                    'care_type': record.care_type or "Другое",
                    'care_date': record.care_date,
                    'description': record.description or "",
                    'status': getattr(record, 'status', 'Выполнено')
                }

                # Получаем имя растения
                plant_name = "Неизвестное растение"
                if hasattr(record, 'instance') and record.instance:
                    try:
                        plant = record.instance
                        if plant.nickname and plant.nickname != 'None':
                            plant_name = plant.nickname
                        elif hasattr(plant, 'plant') and plant.plant:
                            if hasattr(plant.plant, 'scientific_name'):
                                plant_name = plant.plant.scientific_name
                    except:
                        pass

                journal_data['plant_name'] = plant_name

                # Создаем карточку
                card = self.create_journal_card(journal_data)
                self.journal_cards_layout.addWidget(card)

            except Exception as card_e:
                print(f"Ошибка создания карточки: {card_e}")
                continue

        self.journal_cards_layout.addStretch()

    def add_journal_entry(self):
        """Добавить запись в журнал"""
        try:
            if self.journal_plant_combo.currentIndex() <= 0:
                self.show_warning_message("Внимание", "Выберите растение из списка")
                return

            plant_name = self.journal_plant_combo.currentText().replace("🌿 ", "").strip()

            if plant_name == "-- Выберите растение --" or not plant_name:
                self.show_warning_message("Внимание", "Выберите растение из списка")
                return

            # Ищем растение в базе данных
            plant = None
            try:
                plant = self.service.PlantInstance.get_or_none(
                    (self.service.PlantInstance.user == self.user_id) &
                    (self.service.PlantInstance.nickname == plant_name)
                )

                if not plant:
                    my_plants = list(self.service.PlantInstance.select().where(
                        self.service.PlantInstance.user == self.user_id
                    ))
                    if my_plants and len(my_plants) > 0:
                        plant = my_plants[0]  # Берем первое растение
            except Exception as plant_e:
                print(f"Ошибка поиска растения: {plant_e}")

            if not plant:
                self.show_warning_message("Ошибка", "Не удалось найти растение. Сначала добавьте растение в разделе 'Мои растения'")
                return

            care_type = self.journal_type_combo.currentText()
            notes_text = self.journal_notes_edit.toPlainText().strip()
            care_date = self.journal_date_edit.date().toPython()

            # Формируем описание
            plant_display_name = plant.nickname if plant.nickname and plant.nickname != 'None' else "Мое растение"
            description = f"{care_type} растения '{plant_display_name}'"
            if notes_text:
                description += f". {notes_text}"

            # Создаем запись в журнале
            from datetime import datetime, time
            care_datetime = datetime.combine(care_date)

            print(f"DEBUG: Создание записи журнала:")
            print(f"  Plant ID: {plant.id}")
            print(f"  Care type: {care_type}")
            print(f"  Date: {care_datetime}")
            print(f"  User ID: {self.user_id}")
            print(f"  Description: {description}")

            # Создаем запись
            self.service.CareJournal.create(
                instance=plant,  # Растение
                care_type=care_type,
                care_date=care_datetime,
                user=self.user_id,  # Пользователь
                description=description,
            )

            # Сбрасываем форму
            self.journal_plant_combo.setCurrentIndex(0)
            self.journal_type_combo.setCurrentIndex(0)
            self.journal_date_edit.setDate(QDate.currentDate())
            self.journal_time_combo.setCurrentIndex(0)
            self.journal_notes_edit.clear()

            # Скрываем форму
            self.toggle_journal_form(False)

            # Обновляем список карточек
            self.load_journal_cards()

            self.show_info_message("Успех", f"Запись '{care_type}' добавлена для '{plant_display_name}'")

        except Exception as e:
            self.show_error_message("Ошибка", f"Не удалось добавить запись: {str(e)}")
            import traceback
            traceback.print_exc()

    def edit_journal_entry(self):
        """Редактировать запись журнала"""
        if not hasattr(self, 'selected_journal_card') or not self.selected_journal_card:
            self.show_warning_message("Внимание", "Выберите запись из журнала, кликнув на карточку")
            return

        try:
            # Получаем данные записи
            journal_record = self.service.CareJournal.get_by_id(self.selected_journal_card)

            dialog = QDialog(self)
            dialog.setWindowTitle(f"✏️ Редактировать запись журнала")
            dialog.setFixedSize(550, 450)  # Немного уменьшил высоту т.к. добавим прокрутку

            # Стиль окна
            dialog.setStyleSheet("""
                QDialog {
                    background-color: #F5F5F5;
                }
                QLabel {
                    font-size: 14px;
                    color: #2c3e50;
                }
                QPushButton {
                    padding: 8px 15px;
                    border-radius: 6px;
                    font-size: 14px;
                    font-weight: bold;
                    min-width: 100px;
                }
            """)

            main_layout = QVBoxLayout(dialog)
            main_layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы т.к. будет в scroll area
            main_layout.setSpacing(0)

            # Заголовок
            title_label = QLabel("✏️ Редактировать запись журнала")
            title_label.setStyleSheet("""
                QLabel {
                    font-size: 18px;
                    font-weight: bold;
                    color: #485935;
                    padding: 15px 20px 10px 20px;
                    border-bottom: 2px solid #93a267;
                    background-color: white;
                }
            """)
            title_label.setAlignment(Qt.AlignCenter)
            main_layout.addWidget(title_label)

            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setFrameStyle(QScrollArea.NoFrame)
            scroll_area.setStyleSheet("""
                QScrollArea {
                    border: none;
                    background-color: transparent;
                }
                QScrollBar:vertical {
                    border: none;
                    background-color: #E0E0E0;
                    width: 10px;
                    border-radius: 5px;
                    margin: 0px;
                }
                QScrollBar::handle:vertical {
                    background-color: #93a267;
                    border-radius: 5px;
                    min-height: 20px;
                }
                QScrollBar::handle:vertical:hover {
                    background-color: #71804e;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    border: none;
                    background: none;
                }
            """)

            # Виджет для содержимого с прокруткой
            scroll_content = QWidget()
            form_layout = QVBoxLayout(scroll_content)
            form_layout.setContentsMargins(20, 15, 25, 15)  # Отступ справа для полосы прокрутки
            form_layout.setSpacing(15)

            # Растение
            plant_label = QLabel("🌿 Растение:")
            plant_label.setStyleSheet("font-weight: bold; color: #485935;")

            # Получаем имя растения
            plant_name = self.selected_journal_data.get('plant_name', 'Неизвестное растение')
            plant_value = QLabel(plant_name)
            plant_value.setStyleSheet("""
                QLabel {
                    padding: 8px 15px;
                    border: 1px solid #DDD;
                    border-radius: 6px;
                    font-size: 14px;
                    background-color: #F8F9FA;
                }
            """)
            form_layout.addWidget(plant_label)
            form_layout.addWidget(plant_value)

            # Тип ухода
            type_label = QLabel("🛠️ Тип ухода:")
            type_label.setStyleSheet("font-weight: bold; color: #485935;")
            type_combo = QComboBox()
            type_combo.addItems(["Полив", "Удобрение", "Пересадка", "Обрезка", "Опрыскивание", "Другое"])
            current_type = journal_record.care_type or "Другое"
            type_combo.setCurrentText(current_type)
            type_combo.setMinimumHeight(35)
            type_combo.setStyleSheet("""
                QComboBox {
                    padding: 8px 15px;
                    border: 2px solid #93a267;
                    border-radius: 6px;
                    font-size: 14px;
                    background-color: white;
                }
                QComboBox:focus {
                    border: 2px solid #485935;
                }
            """)
            form_layout.addWidget(type_label)
            form_layout.addWidget(type_combo)

            # Дата ухода
            date_label = QLabel("📅 Дата ухода:")
            date_label.setStyleSheet("font-weight: bold; color: #485935;")
            date_edit = QDateEdit()
            date_edit.setCalendarPopup(True)

            # Устанавливаем текущую дату из записи
            if journal_record.care_date:
                care_date = journal_record.care_date
                from datetime import date, datetime

                if isinstance(care_date, datetime):
                    qdate = QDate(care_date.year, care_date.month, care_date.day)
                elif isinstance(care_date, date):
                    qdate = QDate(care_date.year, care_date.month, care_date.day)
                else:
                    qdate = QDate.currentDate()
                date_edit.setDate(qdate)
            else:
                date_edit.setDate(QDate.currentDate())

            date_edit.setDisplayFormat("dd.MM.yyyy")
            date_edit.setMinimumHeight(35)
            date_edit.setStyleSheet("""
                QDateEdit {
                    padding: 8px 15px;
                    border: 2px solid #93a267;
                    border-radius: 6px;
                    font-size: 14px;
                    background-color: white;
                }
                QDateEdit:focus {
                    border: 2px solid #485935;
                }
            """)
            form_layout.addWidget(date_label)
            form_layout.addWidget(date_edit)

            # Заметки
            notes_label = QLabel("📝 Заметки:")
            notes_label.setStyleSheet("font-weight: bold; color: #485935;")
            notes_edit = QTextEdit()
            notes_edit.setPlainText(journal_record.description or "")
            notes_edit.setMinimumHeight(120)  # Увеличил высоту для заметок
            notes_edit.setStyleSheet("""
                QTextEdit {
                    padding: 8px 15px;
                    border: 2px solid #93a267;
                    border-radius: 6px;
                    font-size: 14px;
                    background-color: white;
                }
                QTextEdit:focus {
                    border: 2px solid #485935;
                }
            """)
            form_layout.addWidget(notes_label)
            form_layout.addWidget(notes_edit)

            form_layout.addStretch()

            # Устанавливаем содержимое в scroll area
            scroll_area.setWidget(scroll_content)
            main_layout.addWidget(scroll_area, 1)

            # Кнопки
            buttons_container = QFrame()
            buttons_container.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border-top: 1px solid #E0E0E0;
                }
            """)
            buttons_layout = QHBoxLayout(buttons_container)
            buttons_layout.setContentsMargins(20, 15, 20, 15)
            buttons_layout.setSpacing(15)
            buttons_layout.addStretch()

            def save_changes():
                try:
                    # Обновляем запись
                    journal_record.care_type = type_combo.currentText()
                    journal_record.description = notes_edit.toPlainText().strip()

                    from datetime import datetime, time, date
                    new_date = date_edit.date().toPython()

                    current_care_date = journal_record.care_date

                    if isinstance(current_care_date, datetime):
                        current_time = current_care_date.time()
                        journal_record.care_date = datetime.combine(new_date, current_time)
                    else:
                        journal_record.care_date = datetime.combine(new_date, time(12, 0))

                    journal_record.save()

                    # Обновляем данные в выбранной карточке
                    if hasattr(self, 'selected_journal_data'):
                        self.selected_journal_data.update({
                            'care_type': journal_record.care_type,
                            'description': journal_record.description,
                            'care_date': journal_record.care_date,
                        })

                    self.show_info_message("Успех", "Запись обновлена!")
                    dialog.accept()
                    self.load_journal_cards()
                except Exception as e:
                    self.show_error_message("Ошибка", f"Не удалось сохранить изменения: {str(e)}")

            def cancel():
                dialog.reject()

            btn_save = QPushButton("💾 Сохранить")
            btn_save.clicked.connect(save_changes)
            btn_save.setStyleSheet("""
                QPushButton {
                    background-color: #93a267;
                    color: white;
                    border: none;
                    padding: 10px 25px;
                }
                QPushButton:hover {
                    background-color: #71804e;
                }
            """)

            btn_cancel = QPushButton("❌ Отмена")
            btn_cancel.clicked.connect(cancel)
            btn_cancel.setStyleSheet("""
                QPushButton {
                    background-color: #95A5A6;
                    color: white;
                    border: none;
                    padding: 10px 25px;
                }
                QPushButton:hover {
                    background-color: #7F8C8D;
                }
            """)

            buttons_layout.addWidget(btn_save)
            buttons_layout.addWidget(btn_cancel)
            main_layout.addWidget(buttons_container)

            # Центрируем окно
            dialog.move(
                self.x() + (self.width() - dialog.width()) // 2,
                self.y() + (self.height() - dialog.height()) // 2
            )

            dialog.exec()

        except Exception as e:
            self.show_error_message("Ошибка", f"Не удалось загрузить данные записи: {str(e)}")
            import traceback
            traceback.print_exc()

    def delete_journal_entry(self):
        """Удалить запись журнала"""
        if not hasattr(self, 'selected_journal_card') or not self.selected_journal_card:
            self.show_warning_message("Внимание", "Выберите запись из журнала, кликнув на карточку")
            return

        plant_name = self.selected_journal_data.get('plant_name', 'Растение')
        care_type = self.selected_journal_data.get('care_type', 'Запись')
        date_text = ""
        if self.selected_journal_data.get('care_date'):
            try:
                if isinstance(self.selected_journal_data['care_date'], str):
                    date_text = self.selected_journal_data['care_date'][:10]
                else:
                    from datetime import datetime
                    if isinstance(self.selected_journal_data['care_date'], datetime):
                        date_text = self.selected_journal_data['care_date'].strftime('%d.%m.%Y')
            except:
                pass

        if self.show_confirmation_dialog("Подтверждение удаления",
                                       f"Удалить запись журнала?\n\n"
                                       f"Растение: {plant_name}"):
            try:
                self.service.CareJournal.delete_by_id(self.selected_journal_card)

                # Сбрасываем выбор
                if hasattr(self, 'selected_journal_card'):
                    delattr(self, 'selected_journal_card')
                if hasattr(self, 'selected_journal_data'):
                    delattr(self, 'selected_journal_data')

                self.show_info_message("Успех", "Запись удалена из журнала")
                self.load_journal_cards()  # Обновляем список

            except Exception as e:
                self.show_error_message("Ошибка", f"Не удалось удалить запись: {str(e)}")

    def add_journal_dialog(self):
        """Показать диалоговое окно для добавления записи в журнал"""
        dialog = QDialog(self)
        dialog.setWindowTitle("➕ Добавить запись в журнал")
        dialog.setFixedSize(500, 450)

        # Стиль окна
        dialog.setStyleSheet("""
            QDialog {
                background-color: #F5F5F5;
            }
            QLabel {
                font-size: 14px;
                color: #2c3e50;
            }
            QPushButton {
                padding: 8px 15px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                min-width: 100px;
            }
        """)

        # Основной лэйаут
        main_layout = QVBoxLayout(dialog)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # Заголовок
        title_label = QLabel("➕ Добавить запись в журнал")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #485935;
                padding-bottom: 8px;
                border-bottom: 2px solid #93a267;
                margin-bottom: 10px;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameStyle(QScrollArea.NoFrame)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #E0E0E0;
                width: 10px;
                border-radius: 5px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #93a267;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #71804e;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)

        # Виджет для содержимого с прокруткой
        scroll_content = QWidget()
        form_layout = QVBoxLayout(scroll_content)
        form_layout.setContentsMargins(5, 5, 15, 5)  # Отступ справа для полосы прокрутки
        form_layout.setSpacing(15)

        # Растение
        plant_label = QLabel("🌿 Растение:")
        plant_label.setStyleSheet("font-weight: bold; color: #485935;")

        plant_combo = QComboBox()
        plant_combo.addItem("-- Выберите растение --", None)

        # Загружаем растения пользователя
        try:
            my_plants = list(self.service.PlantInstance.select().where(
                self.service.PlantInstance.user == self.user_id
            ))

            for plant in my_plants:
                display_name = plant.nickname if plant.nickname and plant.nickname != 'None' else "Мое растение"
                plant_combo.addItem(f"🌿 {display_name}", plant.id)
        except Exception as e:
            print(f"Ошибка загрузки растений: {e}")
            plant_combo.addItem("⚠️ Ошибка загрузки растений", None)

        plant_combo.setMinimumHeight(35)
        plant_combo.setStyleSheet("""
            QComboBox {
                padding: 8px 15px;
                border: 2px solid #93a267;
                border-radius: 6px;
                font-size: 14px;
                background-color: white;
            }
            QComboBox:focus {
                border: 2px solid #485935;
            }
        """)
        form_layout.addWidget(plant_label)
        form_layout.addWidget(plant_combo)

        # Тип ухода
        type_label = QLabel("🛠️ Тип ухода:")
        type_label.setStyleSheet("font-weight: bold; color: #485935;")
        type_combo = QComboBox()
        type_combo.addItems(["Полив", "Удобрение", "Пересадка", "Обрезка", "Опрыскивание", "Другое"])
        type_combo.setMinimumHeight(35)
        type_combo.setStyleSheet("""
            QComboBox {
                padding: 8px 15px;
                border: 2px solid #93a267;
                border-radius: 6px;
                font-size: 14px;
                background-color: white;
            }
            QComboBox:focus {
                border: 2px solid #485935;
            }
        """)
        form_layout.addWidget(type_label)
        form_layout.addWidget(type_combo)

        # Дата ухода
        date_label = QLabel("📅 Дата ухода:")
        date_label.setStyleSheet("font-weight: bold; color: #485935;")
        date_edit = QDateEdit()
        date_edit.setCalendarPopup(True)
        date_edit.setDate(QDate.currentDate())
        date_edit.setDisplayFormat("dd.MM.yyyy")
        date_edit.setMinimumHeight(35)
        date_edit.setStyleSheet("""
            QDateEdit {
                padding: 8px 15px;
                border: 2px solid #93a267;
                border-radius: 6px;
                font-size: 14px;
                background-color: white;
            }
            QDateEdit:focus {
                border: 2px solid #485935;
            }
        """)
        form_layout.addWidget(date_label)
        form_layout.addWidget(date_edit)

        # Заметки
        notes_label = QLabel("📝 Заметки (необязательно):")
        notes_label.setStyleSheet("font-weight: bold; color: #485935;")
        notes_edit = QTextEdit()
        notes_edit.setMaximumHeight(80)
        notes_edit.setPlaceholderText("Опишите что было сделано...")
        notes_edit.setStyleSheet("""
            QTextEdit {
                padding: 8px 15px;
                border: 2px solid #93a267;
                border-radius: 6px;
                font-size: 14px;
                background-color: white;
            }
            QTextEdit:focus {
                border: 2px solid #485935;
            }
        """)
        form_layout.addWidget(notes_label)
        form_layout.addWidget(notes_edit)

        # Растягивающийся элемент
        form_layout.addStretch()

        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area, 1)

        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        buttons_layout.addStretch()

        def save_journal_entry():
            # Проверяем выбор растения
            if plant_combo.currentIndex() <= 0:
                self.show_warning_message("Внимание", "Выберите растение из списка")
                return

            try:
                plant_id = plant_combo.currentData()
                care_type = type_combo.currentText()
                care_date = date_edit.date().toPython()  # Это уже date объект
                notes = notes_edit.toPlainText().strip()

                # Получаем растение
                plant = self.service.PlantInstance.get_by_id(plant_id)

                # Формируем описание
                description = notes if notes else ""
                print(f"DEBUG: Создание записи журнала:")
                print(f"  Plant ID: {plant_id}")
                print(f"  Plant: {plant.nickname if plant.nickname else 'Мое растение'}")
                print(f"  Care type: {care_type}")
                print(f"  Date: {care_date}")
                print(f"  Description: {description}")

                self.service.CareJournal.create(
                    instance=plant,
                    care_type=care_type,
                    care_date=care_date,
                    user=self.user_id,
                    description=description,
                )

                self.show_info_message("Успех", "Запись добавлена в журнал!")
                dialog.accept()
                self.load_journal_cards()

            except Exception as e:
                self.show_error_message("Ошибка", f"Не удалось добавить запись: {str(e)}")
                import traceback
                traceback.print_exc()

        def cancel():
            dialog.reject()

        btn_save = QPushButton("💾 Сохранить")
        btn_save.clicked.connect(save_journal_entry)
        btn_save.setStyleSheet("""
            QPushButton {
                background-color: #93a267;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #71804e;
            }
        """)

        btn_cancel = QPushButton("❌ Отмена")
        btn_cancel.clicked.connect(cancel)
        btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #95A5A6;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #7F8C8D;
            }
        """)

        buttons_layout.addWidget(btn_save)
        buttons_layout.addWidget(btn_cancel)
        main_layout.addLayout(buttons_layout)

        # Центрируем окно
        dialog.move(
            self.x() + (self.width() - dialog.width()) // 2,
            self.y() + (self.height() - dialog.height()) // 2
        )

        dialog.exec()

    def switch_page(self, page_id):
        """Переключить страницу"""
        self.set_active_button(page_id)

        page_titles = {
            "catalog": "📚 Справочник растений",
            "my_plants": "🌱 Мои растения",
            "journal": "📓 Журнал ухода",
            "stats": "📊 Статистика",
            "settings": "⚙️ Настройки",
            "help": "❓ Помощь"
        }

        self.page_title.setText(page_titles.get(page_id, "Добро пожаловать!"))

        # Загружаем данные при переходе на страницу журнала
        if page_id == "journal":
            self.load_journal_cards()

        # Обновляем при переходе на Мои растения
        if page_id == "my_plants":
            self.load_my_plants()

        # Показываем соответствующую страницу
        page_index = {
            "catalog": 0,
            "my_plants": 1,
            "journal": 2,
            "stats": 3,
            "settings": 4,
            "help": 5
        }.get(page_id, 0)

        self.stacked_widget.setCurrentIndex(page_index)


    def create_stats_page(self):
        """Создать страницу статистики с экспортом данных"""
        page = QWidget()

        # Основной layout с прокруткой
        main_layout = QVBoxLayout(page)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(25)

        # Заголовок
        title_label = QLabel("📊 Статистика")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2C3E50;
                padding-bottom: 10px;
                border-bottom: 2px solid #93a267;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Создаем ScrollArea для прокрутки
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.NoFrame)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #F0F0F0;
                width: 10px;
                border-radius: 5px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #93a267;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #71804e;
            }
        """)

        # Контейнер для содержимого
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 10, 0)
        content_layout.setSpacing(20)

        # Секция экспорта данных
        export_group = QGroupBox("📤 Экспорт данных")
        export_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                border: 2px solid #93a267;
                border-radius: 10px;
                padding-top: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px 0 10px;
                color: #485935;
            }
        """)

        export_layout = QVBoxLayout(export_group)
        export_layout.setSpacing(15)

        # Описание
        export_desc = QLabel("Экспортируйте ваши данные в различных форматах для сохранения или печати:")
        export_desc.setStyleSheet("""
            QLabel {
                color: #485935;
                font-size: 14px;
                padding: 5px;
            }
        """)
        export_desc.setWordWrap(True)
        export_layout.addWidget(export_desc)

        # Кнопки экспорта
        buttons_grid = QGridLayout()
        buttons_grid.setSpacing(15)

        export_button_style = """
        QPushButton {
            background-color: #93a267;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: bold;
            font-size: 14px;
            min-width: 180px;
            height: 40px;
        }
        QPushButton:hover {
            background-color: #7a8a53;
        }
        QPushButton:pressed {
            background-color: #6a7949;
        }
        """

        # Экспорт растений в PDF
        self.btn_export_plants_pdf = QPushButton("🌱 Экспорт растений\n📄 PDF формат")
        self.btn_export_plants_pdf.setStyleSheet(export_button_style)
        self.btn_export_plants_pdf.clicked.connect(lambda: self.export_plants('pdf'))
        buttons_grid.addWidget(self.btn_export_plants_pdf, 0, 0)

        # Экспорт растений в Word
        self.btn_export_plants_word = QPushButton("🌱 Экспорт растений\n📝 Word формат")
        self.btn_export_plants_word.setStyleSheet(export_button_style)
        self.btn_export_plants_word.clicked.connect(lambda: self.export_plants('word'))
        buttons_grid.addWidget(self.btn_export_plants_word, 0, 1)

        # Экспорт журнала в PDF
        self.btn_export_journal_pdf = QPushButton("📓 Экспорт журнала ухода\n📄 PDF формат")
        self.btn_export_journal_pdf.setStyleSheet(export_button_style)
        self.btn_export_journal_pdf.clicked.connect(lambda: self.export_journal('pdf'))
        buttons_grid.addWidget(self.btn_export_journal_pdf, 1, 0)

        # Экспорт журнала в Word
        self.btn_export_journal_word = QPushButton("📓 Экспорт журнала ухода\n📝 Word формат")
        self.btn_export_journal_word.setStyleSheet(export_button_style)
        self.btn_export_journal_word.clicked.connect(lambda: self.export_journal('word'))
        buttons_grid.addWidget(self.btn_export_journal_word, 1, 1)

        export_layout.addLayout(buttons_grid)
        content_layout.addWidget(export_group)

        # Секция статистики
        stats_group = QGroupBox("📈 Общая статистика")
        stats_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                border: 2px solid #93a267;
                border-radius: 10px;
                padding-top: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px 0 10px;
                color: #485935;
            }
        """)

        stats_layout = QVBoxLayout(stats_group)
        stats_layout.setSpacing(15)

        # Контейнер для статистики
        self.stats_container = QWidget()
        self.stats_container_layout = QVBoxLayout(self.stats_container)
        self.stats_container_layout.setSpacing(10)

        # Индикатор загрузки
        self.stats_loading_label = QLabel("Загрузка статистики...")
        self.stats_loading_label.setAlignment(Qt.AlignCenter)
        self.stats_loading_label.setStyleSheet("""
            QLabel {
                color: #7F8C8D;
                font-size: 16px;
                padding: 20px;
            }
        """)
        self.stats_container_layout.addWidget(self.stats_loading_label)

        stats_layout.addWidget(self.stats_container)

        self.btn_refresh_stats = QPushButton("🔄 Обновить статистику")
        self.btn_refresh_stats.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.btn_refresh_stats.clicked.connect(self.load_statistics)
        stats_layout.addWidget(self.btn_refresh_stats)

        content_layout.addWidget(stats_group)

        content_layout.addStretch()
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area, 1)
        self.stacked_widget.addWidget(page)

        # Загружаем статистику сразу при создании страницы
        self.load_statistics()

    def load_statistics(self):
        """Загрузить и отобразить статистику"""
        try:
            for i in reversed(range(self.stats_container_layout.count())):
                widget = self.stats_container_layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()

            # Получаем данные
            my_plants = list(self.service.PlantInstance.select().where(
                self.service.PlantInstance.user == self.user_id
            ))

            journal_records = list(self.service.CareJournal.select().where(
                self.service.CareJournal.user == self.user_id
            ))

            # Создаем виджеты статистики
            stats_style = """
                QLabel {
                    font-size: 14px;
                    color: #34495E;
                    padding: 8px 10px;
                    background-color: white;
                    border-radius: 6px;
                    border: 1px solid #DDD;
                    margin: 2px;
                }
            """

            # Общее количество растений
            plants_count = len(my_plants)
            plants_label = QLabel(f"🌿 <b>Общее количество растений:</b> {plants_count}")
            plants_label.setStyleSheet(stats_style)
            self.stats_container_layout.addWidget(plants_label)

            # Растения по состоянию здоровья
            if plants_count > 0:
                health_stats = {}
                for plant in my_plants:
                    status = plant.health_status or 'unknown'
                    health_stats[status] = health_stats.get(status, 0) + 1

                # Словарь для отображения статусов
                status_names = {
                    'excellent': 'Отличное 🌟',
                    'good': 'Хорошее ✅',
                    'fair': 'Среднее ⚠️',
                    'poor': 'Плохое ❗',
                    'critical': 'Критическое 💀',
                    'unknown': 'Не указано'
                }

                health_label = QLabel("💚 <b>Состояние здоровья растений:</b>")
                health_label.setStyleSheet(stats_style)
                self.stats_container_layout.addWidget(health_label)

                for status, count in health_stats.items():
                    display_name = status_names.get(status, status)
                    status_label = QLabel(f"   • {display_name}: {count} ({count/plants_count*100:.1f}%)")
                    status_label.setStyleSheet(stats_style.replace("white", "#F8F9FA"))
                    self.stats_container_layout.addWidget(status_label)

            # Статистика журнала
            journal_count = len(journal_records)
            journal_label = QLabel(f"📓 <b>Записей в журнале ухода:</b> {journal_count}")
            journal_label.setStyleSheet(stats_style)
            self.stats_container_layout.addWidget(journal_label)

            if journal_count > 0:
                # Типы ухода
                care_types = {}
                for record in journal_records:
                    care_type = record.care_type or 'Другое'
                    care_types[care_type] = care_types.get(care_type, 0) + 1

                care_label = QLabel("🛠️ <b>Типы ухода:</b>")
                care_label.setStyleSheet(stats_style)
                self.stats_container_layout.addWidget(care_label)

                for care_type, count in sorted(care_types.items(), key=lambda x: x[1], reverse=True):
                    percent = count/journal_count*100
                    type_label = QLabel(f"   • {care_type}: {count} ({percent:.1f}%)")
                    type_label.setStyleSheet(stats_style.replace("white", "#F8F9FA"))
                    self.stats_container_layout.addWidget(type_label)

                # Последняя запись
                if journal_records:
                    last_record = max(journal_records, key=lambda x: x.care_date if x.care_date else datetime.min)
                    last_date = last_record.care_date.strftime('%d.%m.%Y') if last_record.care_date else 'Не указана'
                    last_label = QLabel(f"📅 <b>Последняя запись:</b> {last_date} ({last_record.care_type})")
                    last_label.setStyleSheet(stats_style)
                    self.stats_container_layout.addWidget(last_label)

            # Информация если данных нет
            if plants_count == 0 and journal_count == 0:
                empty_label = QLabel("📭 У вас пока нет данных для статистики.\nДобавьте растения и записи в журнал ухода.")
                empty_label.setStyleSheet("""
                    QLabel {
                        color: #7F8C8D;
                        font-size: 16px;
                        padding: 30px;
                        text-align: center;
                        font-style: italic;
                    }
                """)
                empty_label.setAlignment(Qt.AlignCenter)
                self.stats_container_layout.addWidget(empty_label)

            self.stats_container_layout.addStretch()

        except Exception as e:
            error_label = QLabel(f"⚠️ Ошибка загрузки статистики: {str(e)}")
            error_label.setStyleSheet("""
                QLabel {
                    color: #e74c3c;
                    font-size: 14px;
                    padding: 20px;
                    text-align: center;
                }
            """)
            self.stats_container_layout.addWidget(error_label)

    def export_plants(self, format_type):
        """Экспорт растений в указанном формате"""
        try:
            # Получаем растения пользователя
            my_plants = list(self.service.PlantInstance.select().where(
                self.service.PlantInstance.user == self.user_id
            ))

            if not my_plants:
                self.show_warning_message("Нет данных", "У вас пока нет растений для экспорта.")
                return

            default_name = f"мои_растения_{datetime.now().strftime('%Y%m%d')}"

            if format_type == 'pdf':
                file_path, _ = QFileDialog.getSaveFileName(
                    self, "Сохранить растения в PDF",
                    f"{default_name}.pdf",
                    "PDF файлы (*.pdf)"
                )
                if file_path:
                    self._create_plants_pdf(my_plants, file_path)

            elif format_type == 'word':
                file_path, _ = QFileDialog.getSaveFileName(
                    self, "Сохранить растения в Word",
                    f"{default_name}.docx",
                    "Word документы (*.docx)"
                )
                if file_path:
                    self._create_plants_word(my_plants, file_path)

        except Exception as e:
            self.show_error_message("Ошибка", f"Не удалось экспортировать растения: {str(e)}")

    def export_journal(self, format_type):
        """Экспорт журнала ухода в указанном формате"""
        try:
            # Получаем записи журнала
            journal_records = list(self.service.CareJournal.select().where(
                self.service.CareJournal.user == self.user_id
            ).order_by(self.service.CareJournal.care_date.desc()))

            if not journal_records:
                self.show_warning_message("Нет данных", "У вас пока нет записей в журнале для экспорта.")
                return

            default_name = f"журнал_ухода_{datetime.now().strftime('%Y%m%d')}"

            if format_type == 'pdf':
                file_path, _ = QFileDialog.getSaveFileName(
                    self, "Сохранить журнал в PDF",
                    f"{default_name}.pdf",
                    "PDF файлы (*.pdf)"
                )
                if file_path:
                    self._create_journal_pdf(journal_records, file_path)

            elif format_type == 'word':
                file_path, _ = QFileDialog.getSaveFileName(
                    self, "Сохранить журнал в Word",
                    f"{default_name}.docx",
                    "Word документы (*.docx)"
                )
                if file_path:
                    self._create_journal_word(journal_records, file_path)

        except Exception as e:
            self.show_error_message("Ошибка", f"Не удалось экспортировать журнал: {str(e)}")


    def _create_plants_pdf(self, plants, file_path):
        """Создать PDF с растениями с поддержкой русских шрифтов"""
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.units import cm
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib import colors
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            import os

            font_found = False
            font_paths = [
                '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
                'C:/Windows/Fonts/arial.ttf',
                'C:/Windows/Fonts/tahoma.ttf',
                'C:/Windows/Fonts/times.ttf',
                './fonts/DejaVuSans.ttf',
            ]

            for font_path in font_paths:
                if os.path.exists(font_path):
                    try:
                        pdfmetrics.registerFont(TTFont('RussianFont', font_path))
                        pdfmetrics.registerFont(TTFont('RussianFont-Bold', font_path))
                        font_found = True
                        break
                    except:
                        continue

            # Если шрифт не найден, используем Helvetica
            if font_found:
                russian_font = 'RussianFont'
                russian_font_bold = 'RussianFont-Bold'
            else:
                russian_font = 'Helvetica'
                russian_font_bold = 'Helvetica-Bold'

            # Создаем документ
            doc = SimpleDocTemplate(
                file_path,
                pagesize=A4,
                topMargin=2*cm,
                bottomMargin=2*cm,
                leftMargin=1.5*cm,
                rightMargin=1.5*cm,
                encoding='utf-8'
            )

            story = []
            styles = getSampleStyleSheet()

            # Настраиваем стили
            if font_found:
                styles['Title'].fontName = russian_font_bold
                styles['Normal'].fontName = russian_font

            # Заголовок
            title = Paragraph("Мои растения", styles['Title'])
            story.append(title)

            # Дата экспорта
            from datetime import datetime
            date_text = f"Дата экспорта: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
            date_para = Paragraph(date_text, styles['Normal'])
            story.append(date_para)

            story.append(Spacer(1, 1*cm))

            # Подготавливаем данные для таблицы
            table_data = []

            # Заголовки таблицы
            headers = ['Название', 'Возраст', 'Состояние', 'Комната', 'Дата добавления']
            table_data.append(headers)

            # Данные растений
            for plant in plants:
                # Возраст
                age = f"{plant.age} мес." if plant.age else "Не указан"

                # Статус на русском
                status_dict = {
                    'excellent': 'Отличное',
                    'good': 'Хорошее',
                    'fair': 'Среднее',
                    'poor': 'Плохое',
                    'critical': 'Критическое'
                }
                status = status_dict.get(plant.health_status, 'Не указано')

                # Комната
                room = plant.room if plant.room else "Не указано"

                # Дата добавления
                date = plant.acquisition_date.strftime('%d.%m.%Y') if plant.acquisition_date else "Не указана"

                # Название растения
                plant_name = plant.nickname if plant.nickname else "Без названия"

                table_data.append([
                    str(plant_name),
                    str(age),
                    str(status),
                    str(room),
                    str(date)
                ])

            # Создаем таблицу
            col_widths = [5*cm, 3*cm, 4*cm, 4*cm, 4*cm]
            table = Table(table_data, colWidths=col_widths, repeatRows=1)

            # Настраиваем стиль таблицы
            table_style = [
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#93a267')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.whitesmoke]),
            ]

            # Добавляем настройки шрифтов
            if font_found:
                table_style.insert(3, ('FONTNAME', (0, 0), (-1, 0), russian_font_bold))
                table_style.insert(9, ('FONTNAME', (0, 1), (-1, -1), russian_font))
                table_style.append(('ALIGN', (0, 1), (-1, -1), 'LEFT'))
            else:
                table_style.insert(3, ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'))
                table_style.insert(9, ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'))
                table_style.append(('ALIGN', (0, 1), (-1, -1), 'LEFT'))

            table.setStyle(TableStyle(table_style))
            story.append(table)

            story.append(Spacer(1, 1*cm))

            # Итог
            total_text = f"Всего растений: {len(plants)}"
            total_para = Paragraph(total_text, styles['Normal'])
            story.append(total_para)

            # Строим документ
            doc.build(story)
            self.show_info_message("Успех", f"Растения экспортированы в PDF\nФайл: {file_path}")

        except ImportError:
            self.show_warning_message("Ошибка",
                "Для экспорта в PDF требуется библиотека reportlab.\n"
                "Установите её: pip install reportlab")
        except Exception as e:
            self.show_error_message("Ошибка", f"Не удалось создать PDF: {str(e)}")
            import traceback
            traceback.print_exc()

    def _create_journal_pdf(self, records, file_path):
        """Создать PDF с журналом ухода"""
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.units import cm
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib import colors
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            import os

            font_found = False
            font_paths = [
                '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
                'C:/Windows/Fonts/arial.ttf',
                'C:/Windows/Fonts/tahoma.ttf',
                'C:/Windows/Fonts/times.ttf',
                './fonts/DejaVuSans.ttf',
            ]

            for font_path in font_paths:
                if os.path.exists(font_path):
                    try:
                        pdfmetrics.registerFont(TTFont('RussianFont', font_path))
                        pdfmetrics.registerFont(TTFont('RussianFont-Bold', font_path))
                        font_found = True
                        break
                    except:
                        continue

            if font_found:
                russian_font = 'RussianFont'
                russian_font_bold = 'RussianFont-Bold'
            else:
                russian_font = 'Helvetica'
                russian_font_bold = 'Helvetica-Bold'

            # Размер страницы A4
            page_width_cm = 21.0
            left_margin_cm = 1.5
            right_margin_cm = 1.5
            available_width_cm = page_width_cm - left_margin_cm - right_margin_cm

            # Создаем документ
            doc = SimpleDocTemplate(
                file_path,
                pagesize=A4,
                topMargin=2*cm,
                bottomMargin=2*cm,
                leftMargin=left_margin_cm*cm,
                rightMargin=right_margin_cm*cm,
                encoding='utf-8'
            )

            story = []
            styles = getSampleStyleSheet()

            if font_found:
                styles['Title'].fontName = russian_font_bold
                styles['Normal'].fontName = russian_font

            # Заголовок
            title = Paragraph("Журнал ухода за растениями", styles['Title'])
            story.append(title)

            # Дата экспорта
            from datetime import datetime
            date_text = f"Дата экспорта: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
            date_para = Paragraph(date_text, styles['Normal'])
            story.append(date_para)

            story.append(Spacer(1, 1*cm))

            # Подготавливаем данные
            table_data = []
            headers = ['Дата', 'Растение', 'Тип ухода', 'Заметки']
            table_data.append(headers)

            for record in records:
                # Имя растения
                plant_name = "Неизвестное растение"
                try:
                    if record.instance and record.instance.nickname:
                        plant_name = record.instance.nickname
                    elif record.instance and record.instance.plant:
                        plant_name = record.instance.plant.scientific_name
                except:
                    pass

                # Дата
                date_str = record.care_date.strftime('%d.%m.%Y') if record.care_date else "Не указана"

                # Тип ухода
                care_type = record.care_type or "Другое"

                # Заметки
                notes = record.description or "Без заметок"
                if len(notes) > 40:
                    notes = notes[:37] + "..."

                table_data.append([date_str, plant_name, care_type, notes])

            # Рассчитываем ширину колонок (сумма должна быть <= available_width_cm)
            col_widths = [3*cm, 5*cm, 4*cm, 6*cm]

            # Если сумма больше доступной ширины, уменьшаем пропорционально
            total_table_width = sum(w/cm for w in col_widths)
            if total_table_width > available_width_cm:
                scale_factor = available_width_cm / total_table_width
                col_widths = [w * scale_factor for w in col_widths]

            table = Table(table_data, colWidths=col_widths, repeatRows=1)

            # Стиль таблицы
            table_style = [
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#93a267')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('LEFTPADDING', (0, 0), (-1, -1), 4),
                ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ]

            # Шрифты
            if font_found:
                table_style.append(('FONTNAME', (0, 0), (-1, 0), russian_font_bold))
                table_style.append(('FONTNAME', (0, 1), (-1, -1), russian_font))
            else:
                table_style.append(('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'))
                table_style.append(('FONTNAME', (0, 1), (-1, -1), 'Helvetica'))

            # Выравнивание
            table_style.append(('ALIGN', (0, 1), (0, -1), 'CENTER'))  # Дата по центру
            table_style.append(('ALIGN', (1, 1), (2, -1), 'LEFT'))    # Растение и тип ухода слева
            table_style.append(('ALIGN', (3, 1), (3, -1), 'LEFT'))    # Заметки слева

            # Перенос длинного текста
            table_style.append(('WORDWRAP', (3, 1), (3, -1), True))  # Включаем перенос слов в колонке заметок

            table.setStyle(TableStyle(table_style))
            story.append(table)

            story.append(Spacer(1, 1*cm))

            # Итог
            total_text = f"Всего записей: {len(records)}"
            total_para = Paragraph(total_text, styles['Normal'])
            story.append(total_para)

            # Автоматически подгоняем размер таблицы под страницу
            doc.build(story, onFirstPage=lambda canvas, doc: None,
                      onLaterPages=lambda canvas, doc: None)

            self.show_info_message("Успех", f"Журнал экспортирован в PDF\nФайл: {file_path}")

        except ImportError:
            self.show_warning_message("Ошибка",
                "Для экспорта в PDF требуется библиотека reportlab.\n"
                "Установите её: pip install reportlab")
        except Exception as e:
            self.show_error_message("Ошибка", f"Не удалось создать PDF: {str(e)}")
            import traceback
            traceback.print_exc()

    def _create_plants_word(self, plants, file_path):
        """Создать Word документ с растениями"""
        try:
            import docx
            from docx import Document
            from docx.shared import Inches, Pt, RGBColor
            from docx.enum.text import WD_ALIGN_PARAGRAPH
            from docx.oxml.ns import qn
            from docx.oxml import OxmlElement

            doc = Document()

            # Настройка стилей для поддержки русского языка
            style = doc.styles['Normal']
            style.font.name = 'Times New Roman'
            style.font.size = Pt(11)

            # Заголовок
            title = doc.add_heading('Мои растения', 0)
            title.alignment = WD_ALIGN_PARAGRAPH.CENTER

            # Дата экспорта
            from datetime import datetime
            date_para = doc.add_paragraph(f"Дата экспорта: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
            date_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

            doc.add_paragraph()  # Пустая строка

            # Таблица
            table = doc.add_table(rows=1, cols=5)
            table.style = 'Table Grid'

            # Заголовки таблицы
            headers = ['Название', 'Возраст', 'Состояние', 'Комната', 'Дата добавления']
            hdr_cells = table.rows[0].cells

            for i, header in enumerate(headers):
                hdr_cells[i].text = header
                paragraph = hdr_cells[i].paragraphs[0]
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = paragraph.runs[0]
                run.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)  # Белый текст

                # Заливка заголовков
                tcPr = hdr_cells[i]._tc.get_or_add_tcPr()
                shading = OxmlElement('w:shd')
                shading.set(qn('w:fill'), '93A267')  # HEX цвета
                tcPr.append(shading)

            # Данные растений
            for plant in plants:
                row_cells = table.add_row().cells

                age = f"{plant.age} мес." if plant.age else "Не указан"
                status_dict = {
                    'excellent': 'Отличное',
                    'good': 'Хорошее',
                    'fair': 'Среднее',
                    'poor': 'Плохое',
                    'critical': 'Критическое'
                }
                status = status_dict.get(plant.health_status, 'Не указано')
                room = plant.room if plant.room else "Не указано"
                date = plant.acquisition_date.strftime('%d.%m.%Y') if plant.acquisition_date else "Не указана"
                plant_name = plant.nickname if plant.nickname else "Без названия"

                data = [plant_name, age, status, room, date]

                for i, value in enumerate(data):
                    row_cells[i].text = str(value)
                    row_cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

            # Итог
            doc.add_paragraph()
            total_para = doc.add_paragraph(f"Всего растений: {len(plants)}")
            total_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

            doc.save(file_path)
            self.show_info_message("Успех", f"Растения экспортированы в Word\nФайл: {file_path}")

        except ImportError:
            self.show_warning_message("Ошибка",
                "Для экспорта в Word требуется библиотека python-docx.\n"
                "Установите её: pip install python-docx")
        except Exception as e:
            self.show_error_message("Ошибка", f"Не удалось создать Word документ: {str(e)}")
            import traceback
            traceback.print_exc()

    def _create_journal_word(self, records, file_path):
        """Создать Word документ с журналом ухода"""
        try:
            import docx
            from docx import Document
            from docx.shared import Inches, Pt, RGBColor
            from docx.enum.text import WD_ALIGN_PARAGRAPH

            doc = Document()

            # Настройка стилей
            style = doc.styles['Normal']
            style.font.name = 'Times New Roman'
            style.font.size = Pt(11)

            # Заголовок
            title = doc.add_heading('Журнал ухода за растениями', 0)
            title.alignment = WD_ALIGN_PARAGRAPH.CENTER

            # Дата экспорта
            from datetime import datetime
            date_para = doc.add_paragraph(f"Дата экспорта: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
            date_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

            doc.add_paragraph()

            # Таблица
            table = doc.add_table(rows=1, cols=4)
            table.style = 'Table Grid'

            # Заголовки таблицы
            headers = ['Дата', 'Растение', 'Тип ухода', 'Заметки']
            hdr_cells = table.rows[0].cells

            for i, header in enumerate(headers):
                hdr_cells[i].text = header
                paragraph = hdr_cells[i].paragraphs[0]
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = paragraph.runs[0]
                run.bold = True

            # Данные записей
            for record in records:
                row_cells = table.add_row().cells

                # Имя растения
                plant_name = "Неизвестное растение"
                try:
                    if record.instance and record.instance.nickname:
                        plant_name = record.instance.nickname
                    elif record.instance and record.instance.plant:
                        plant_name = record.instance.plant.scientific_name
                except:
                    pass

                date_str = record.care_date.strftime('%d.%m.%Y') if record.care_date else "Не указана"
                care_type = record.care_type or "Другое"
                notes = record.description or "Без заметок"

                data = [date_str, plant_name, care_type, notes]

                for i, value in enumerate(data):
                    row_cells[i].text = str(value)
                    row_cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

            # Итог
            doc.add_paragraph()
            total_para = doc.add_paragraph(f"Всего записей: {len(records)}")
            total_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

            doc.save(file_path)
            self.show_info_message("Успех", f"Журнал экспортирован в Word\nФайл: {file_path}")

        except ImportError:
            self.show_warning_message("Ошибка",
                "Для экспорта в Word требуется библиотека python-docx.\n"
                "Установите её: pip install python-docx")
        except Exception as e:
            self.show_error_message("Ошибка", f"Не удалось создать Word документ: {str(e)}")

