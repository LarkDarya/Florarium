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

