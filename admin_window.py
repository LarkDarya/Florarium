# windows/admin_window.py
# В admin_window.py исправьте импорты:

# Разделите импорты правильно:
from PySide6.QtCore import Qt, QDate, QTime, QTimer, Signal  # QTime здесь!
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QApplication, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox,
    QTabWidget, QComboBox, QGroupBox, QFormLayout, QCheckBox,
    QTimeEdit,  # QTimeEdit здесь, а QTime - выше в QtCore
    QMainWindow, QGridLayout, QTextEdit, QDateEdit, QRadioButton,
    QButtonGroup, QSpinBox, QDoubleSpinBox, QSlider, QProgressBar,
    QListView, QTreeView, QTreeWidget, QTreeWidgetItem, QHeaderView,
    QSplitter, QFrame, QDialog, QDialogButtonBox, QStyleFactory,
    QFileDialog, QInputDialog, QMenu, QSystemTrayIcon,
    QToolBar, QStatusBar, QMenuBar, QSizePolicy, QSpacerItem, QListWidget, QProgressDialog
)

from PySide6.QtGui import QFont, QColor, QIcon, QPixmap, QAction
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QBrush, QColor
from service import FlorariumService
import os
from admin_controller import AdminController
from datetime import datetime, date

class AdminWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.service = FlorariumService()
        self.setup_ui()
        self.controller = AdminController(self.service, self)
        self.load_data()
        self.center_window()

    def center_window(self):
        """Центрировать окно на экране"""
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)

        # Устанавливаем позицию окна
        self.move(window_geometry.topLeft())

    def setup_ui(self):
        """Настройка интерфейса администратора"""
        self.setWindowTitle("Панель администратора - Флорариум")
        self.resize(1200, 700)

        main_layout = QVBoxLayout()

        # Заголовок
        title = QLabel("👑 Панель администратора")
        title.setFont(QFont("Times New Roman", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #485935; margin: 10px;")
        main_layout.addWidget(title)

        # Вкладки
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid rgba(147, 162, 103, 0.3);
                border-radius: 10px;
                background: #FBFBFB;
            }
            QTabBar::tab {
                background-color: rgba(147, 162, 103, 0.7);
                color: #f8efda;
                padding: 12px 25px;
                border-bottom: none;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                font-family: "Times New Roman", serif;
                font-size: 14px;
                font-weight: bold;
                min-width: 100px;
                min-height: 15px;
            }
            QTabBar::tab:selected {
                background-color: rgba(147, 162, 103, 1);
                color: #f8efda;
                border-bottom: none;
                font-weight: bold;
            }
            QTabBar::tab:hover {
                background-color: rgba(113, 128, 78, 1);
                color: #f8efda;
            }
            QTabBar::tab:!selected {
                margin-top: 7px;
            }
        """)

        # Вкладка 1: Пользователи (теперь с возможностью управления)
        users_tab = QWidget()
        users_layout = QVBoxLayout()

        # Заголовок для вкладки пользователей
        users_title = QLabel("👥 Управление пользователями")
        users_title.setFont(QFont("Cambria Math", 14))
        users_title.setStyleSheet("color: #485935; margin: 5px;")
        users_layout.addWidget(users_title)

        # Кнопки управления пользователями - добавляем как атрибуты
        users_buttons = QHBoxLayout()
        self.btn_add_user = QPushButton("➕ Добавить")
        self.btn_edit_user = QPushButton("✏️ Редактировать")
        self.btn_delete_user = QPushButton("🗑️ Удалить")

        for btn in [self.btn_add_user, self.btn_edit_user, self.btn_delete_user]:
            btn.setStyleSheet(self.get_button_style())

        users_buttons.addWidget(self.btn_add_user)
        users_buttons.addWidget(self.btn_edit_user)
        users_buttons.addWidget(self.btn_delete_user)
        users_buttons.addStretch()
        users_layout.addLayout(users_buttons)

        # Таблица пользователей
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(8)
        self.users_table.setHorizontalHeaderLabels([
            "ID", "Логин", "Email", "Имя", "Фамилия", "Роль", "Дата регистрации", "Дата рождения"
        ])
        self.users_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.users_table.verticalHeader().setMinimumSectionSize(35)

        header = self.users_table.horizontalHeader()

        header.resizeSection(0, 50)     # ID
        header.resizeSection(1, 120)    # Логин
        header.resizeSection(2, 212)    # Email
        header.resizeSection(3, 130)    # Имя
        header.resizeSection(4, 160)    # Фамилия
        header.resizeSection(5, 80)     # Роль
        header.resizeSection(6, 160)    # Дата
        header.resizeSection(7, 160)    # Дата

        # Настройка стилей таблицы пользователей
        self.users_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 2px solid rgba(147, 162, 103, 1);
                border-radius: 5px;
                font-family: "Cambria Math";
                font-size: 12px;
                gridline-color: rgba(147, 162, 103, 0.3);
            }
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid rgba(147, 162, 103, 0.2);
            }
            QTableWidget::item:selected {
                background-color: #ffe4b5;
                color: black;
            }
            QHeaderView::section {
                background-color: #f8efda;
                color: #485935;
                padding: 8px;
                border: none;
                border-right: 1px solid rgba(147, 162, 103, 0.5);
                border-bottom: 2px solid rgba(147, 162, 103, 1);
                font-family: "Cambria Math";
                font-size: 13px;
                font-weight: bold;
            }
            QHeaderView::section:last {
                border-right: none;
            }
            QTableCornerButton::section {
                background-color: #f8efda;
                border: none;
                border-bottom: 2px solid rgba(147, 162, 103, 1);
                border-right: 1px solid rgba(147, 162, 103, 0.5);
            }
            QScrollBar:vertical {
                border: none;
                background: white;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: rgba(147, 162, 103, 0.5);
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(147, 162, 103, 0.7);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)

        users_layout.addWidget(self.users_table)
        users_tab.setLayout(users_layout)

        # Вкладка 2: Семейства растений
        families_tab = self.create_families_tab()

        # Вкладка 3: Руководства по уходу
        care_guides_tab = self.create_care_guides_tab()

        # Вкладка 4: Местоположения
        locations_tab = self.create_locations_tab()

        # Вкладка 5: Фотографии
        photos_tab = self.create_photos_tab()

        # Вкладка 6: Растения
        plants_tab = self.create_plants_tab()

        # Вкладка 7: Вредители
        pests_tab = self.create_pests_tab()

        # Вкладка 8: Болезни
        diseases_tab = self.create_diseases_tab()

        # Вкладка 9: Связи
        relations_tab = self.create_relations_tab()

        # Вкладка 10: Экспорт
        system_tab = self.create_system_tab()

        # Добавление вкладок
        self.tabs.addTab(users_tab, "👥 Пользователи")
        self.tabs.addTab(families_tab, "🌳 Семейства")
        self.tabs.addTab(care_guides_tab, "📚 Уход")
        self.tabs.addTab(locations_tab, "🗺️ Местоположения")
        self.tabs.addTab(photos_tab, "📸 Фотографии")
        self.tabs.addTab(plants_tab, "🌿 Растения")
        self.tabs.addTab(pests_tab, "🐛 Вредители")
        self.tabs.addTab(diseases_tab, "🩺 Болезни")
        self.tabs.addTab(relations_tab, "🔗 Связи")
        self.tabs.addTab(system_tab, "⚙️ Экспорт")

        main_layout.addWidget(self.tabs)

        # Кнопка выхода
        self.btn_logout = QPushButton("Выйти")
        self.btn_logout.setStyleSheet("""
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
        main_layout.addWidget(self.btn_logout, alignment=Qt.AlignRight)

        self.setLayout(main_layout)

        # Подключение сигналов
        self.btn_logout.clicked.connect(self.logout)

    def format_date_for_display(self, date_value, include_time=True):
        """Форматирование даты для отображения в диалогах"""
        if not date_value:
            return ""

        try:
            if isinstance(date_value, datetime):
                date_obj = date_value
            elif isinstance(date_value, str):
                # Пробуем разные форматы
                for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%Y-%m-%dT%H:%M:%S', '%d.%m.%Y']:
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

    def create_families_tab(self):
        """Создание вкладки для семейств растений"""
        tab = QWidget()
        layout = QVBoxLayout()

        title = QLabel("🌳 Управление семействами растений")
        title.setFont(QFont("Cambria Math", 14))
        title.setStyleSheet("color: #485935; margin: 5px;")
        layout.addWidget(title)

        # Кнопки - сохраняем как атрибуты
        buttons = QHBoxLayout()
        self.btn_add_family = QPushButton("➕ Добавить")
        self.btn_edit_family = QPushButton("✏️ Редактировать")
        self.btn_delete_family = QPushButton("🗑️ Удалить")

        for btn in [self.btn_add_family, self.btn_edit_family, self.btn_delete_family]:
            btn.setStyleSheet(self.get_button_style())

        buttons.addWidget(self.btn_add_family)
        buttons.addWidget(self.btn_edit_family)
        buttons.addWidget(self.btn_delete_family)
        buttons.addStretch()
        layout.addLayout(buttons)

        # Таблица семейств - сохраняем как атрибут
        self.families_table = QTableWidget()
        self.families_table.setColumnCount(3)
        self.families_table.setHorizontalHeaderLabels(["ID", "Название", "Описание"])
        self.families_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.families_table.setStyleSheet(self.get_table_style())

        header = self.families_table.horizontalHeader()
        header.resizeSection(0, 50)   # ID
        header.resizeSection(1, 200)  # Название
        header.resizeSection(2, 300)  # Описание

        layout.addWidget(self.families_table)
        tab.setLayout(layout)
        return tab

    def create_care_guides_tab(self):
        """Создание вкладки для руководств по уходу"""
        tab = QWidget()
        layout = QVBoxLayout()

        title = QLabel("📚 Управление руководствами по уходу")
        title.setFont(QFont("Cambria Math", 14))
        title.setStyleSheet("color: #485935; margin: 5px;")
        layout.addWidget(title)

        # Кнопки
        buttons = QHBoxLayout()
        self.btn_add_care_guide = QPushButton("➕ Добавить")
        self.btn_edit_care_guide = QPushButton("✏️ Редактировать")
        self.btn_delete_care_guide = QPushButton("🗑️ Удалить")

        for btn in [self.btn_add_care_guide, self.btn_edit_care_guide, self.btn_delete_care_guide]:
            btn.setStyleSheet(self.get_button_style())

        buttons.addWidget(self.btn_add_care_guide)
        buttons.addWidget(self.btn_edit_care_guide)
        buttons.addWidget(self.btn_delete_care_guide)
        buttons.addStretch()
        layout.addLayout(buttons)

        # Таблица руководств
        self.care_guides_table = QTableWidget()
        self.care_guides_table.setColumnCount(8)
        self.care_guides_table.setHorizontalHeaderLabels([
            "ID", "Полив", "Свет (лк)", "Темп. мин.", "Темп. макс.",
            "Почва", "Удобрения", "Влажность (%)"
        ])
        self.care_guides_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.care_guides_table.setStyleSheet(self.get_table_style())

        header = self.care_guides_table.horizontalHeader()
        header.resizeSection(0, 50)   # ID
        header.resizeSection(1, 150)  # Полив
        header.resizeSection(2, 100)  # Свет
        header.resizeSection(3, 100)  # Т мин
        header.resizeSection(4, 100)  # Т макс
        header.resizeSection(5, 150)  # Почва
        header.resizeSection(6, 150)  # Удобрения
        header.resizeSection(7, 130)  # Влажность

        layout.addWidget(self.care_guides_table)
        tab.setLayout(layout)
        return tab

    def create_locations_tab(self):
        """Создание вкладки для местоположений"""
        tab = QWidget()
        layout = QVBoxLayout()

        title = QLabel("🗺️ Управление природными местоположениями")
        title.setFont(QFont("Cambria Math", 14))
        title.setStyleSheet("color: #485935; margin: 5px;")
        layout.addWidget(title)

        # Кнопки
        buttons = QHBoxLayout()
        self.btn_add_location = QPushButton("➕ Добавить")
        self.btn_edit_location = QPushButton("✏️ Редактировать")
        self.btn_delete_location = QPushButton("🗑️ Удалить")

        for btn in [self.btn_add_location, self.btn_edit_location, self.btn_delete_location]:
            btn.setStyleSheet(self.get_button_style())

        buttons.addWidget(self.btn_add_location)
        buttons.addWidget(self.btn_edit_location)
        buttons.addWidget(self.btn_delete_location)
        buttons.addStretch()
        layout.addLayout(buttons)

        # Таблица местоположений - сохраняем как атрибут
        self.locations_table = QTableWidget()
        self.locations_table.setColumnCount(3)
        self.locations_table.setHorizontalHeaderLabels(["ID", "Название местности", "Описание"])
        self.locations_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.locations_table.setStyleSheet(self.get_table_style())

        header = self.locations_table.horizontalHeader()
        header.resizeSection(0, 50)   # ID
        header.resizeSection(1, 250)  # Название
        header.resizeSection(2, 300)  # Описание

        layout.addWidget(self.locations_table)
        tab.setLayout(layout)
        return tab

    def create_photos_tab(self):
        """Создание вкладки для фотографий"""
        tab = QWidget()
        layout = QVBoxLayout()

        title = QLabel("📸 Управление фотографиями растений")
        title.setFont(QFont("Cambria Math", 14))
        title.setStyleSheet("color: #485935; margin: 5px;")
        layout.addWidget(title)

        # Кнопки
        buttons = QHBoxLayout()
        self.btn_add_photo = QPushButton("➕ Добавить")
        self.btn_edit_photo = QPushButton("✏️ Редактировать")
        self.btn_delete_photo = QPushButton("🗑️ Удалить")

        for btn in [self.btn_add_photo, self.btn_edit_photo, self.btn_delete_photo]:
            btn.setStyleSheet(self.get_button_style())

        buttons.addWidget(self.btn_add_photo)
        buttons.addWidget(self.btn_edit_photo)
        buttons.addWidget(self.btn_delete_photo)
        buttons.addStretch()
        layout.addLayout(buttons)

        # Таблица фотографий
        self.photos_table = QTableWidget()
        self.photos_table.setColumnCount(2)
        self.photos_table.setHorizontalHeaderLabels(["ID", "URL фотографии"])
        self.photos_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.photos_table.setStyleSheet(self.get_table_style())

        header = self.photos_table.horizontalHeader()
        header.resizeSection(0, 50)   # ID
        header.resizeSection(1, 500)  # URL

        layout.addWidget(self.photos_table)
        tab.setLayout(layout)
        return tab

    def create_plants_tab(self):
        """Создание вкладки для растений"""
        tab = QWidget()
        layout = QVBoxLayout()

        title = QLabel("🌿 Управление растениями")
        title.setFont(QFont("Cambria Math", 14))
        title.setStyleSheet("color: #485935; margin: 5px;")
        layout.addWidget(title)

        # Кнопки
        buttons = QHBoxLayout()
        self.btn_add_plant = QPushButton("➕ Добавить")
        self.btn_edit_plant = QPushButton("✏️ Редактировать")
        self.btn_delete_plant = QPushButton("🗑️ Удалить")

        for btn in [self.btn_add_plant, self.btn_edit_plant, self.btn_delete_plant]:
            btn.setStyleSheet(self.get_button_style())

        buttons.addWidget(self.btn_add_plant)
        buttons.addWidget(self.btn_edit_plant)
        buttons.addWidget(self.btn_delete_plant)
        buttons.addStretch()
        layout.addLayout(buttons)

        # Таблица растений
        self.plants_table = QTableWidget()
        self.plants_table.setColumnCount(6)
        self.plants_table.setHorizontalHeaderLabels([
            "ID", "Научное название", "Описание", "ID руководства", "ID местоположения", "ID фото"  # Добавлена колонка фото
        ])
        self.plants_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.plants_table.setStyleSheet(self.get_table_style())

        header = self.plants_table.horizontalHeader()
        header.resizeSection(0, 50)   # ID
        header.resizeSection(1, 250)  # Научное название
        header.resizeSection(2, 300)  # Описание
        header.resizeSection(3, 130)  # ID руководства
        header.resizeSection(4, 150)  # ID местоположения
        header.resizeSection(5, 100)  # ID фото - новая колонка

        layout.addWidget(self.plants_table)
        tab.setLayout(layout)
        return tab

    def create_pests_tab(self):
        """Создание вкладки для вредителей"""
        tab = QWidget()
        layout = QVBoxLayout()

        title = QLabel("🐛 Управление вредителями растений")
        title.setFont(QFont("Cambria Math", 14))
        title.setStyleSheet("color: #485935; margin: 5px;")
        layout.addWidget(title)

        # Кнопки - сохраняем как атрибуты
        buttons = QHBoxLayout()
        self.btn_add_pest = QPushButton("➕ Добавить")
        self.btn_edit_pest = QPushButton("✏️ Редактировать")
        self.btn_delete_pest = QPushButton("🗑️ Удалить")

        for btn in [self.btn_add_pest, self.btn_edit_pest, self.btn_delete_pest]:
            btn.setStyleSheet(self.get_button_style())

        buttons.addWidget(self.btn_add_pest)
        buttons.addWidget(self.btn_edit_pest)
        buttons.addWidget(self.btn_delete_pest)
        buttons.addStretch()
        layout.addLayout(buttons)

        # Таблица вредителей
        self.pests_table = QTableWidget()
        self.pests_table.setColumnCount(4)
        self.pests_table.setHorizontalHeaderLabels(["ID", "Название", "Описание", "Методы лечения"])
        self.pests_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.pests_table.setStyleSheet(self.get_table_style())

        header = self.pests_table.horizontalHeader()
        header.resizeSection(0, 50)   # ID
        header.resizeSection(1, 150)  # Название
        header.resizeSection(2, 250)  # Описание
        header.resizeSection(3, 250)  # Методы лечения

        layout.addWidget(self.pests_table)
        tab.setLayout(layout)
        return tab

    def create_diseases_tab(self):
        """Создание вкладки для болезней"""
        tab = QWidget()
        layout = QVBoxLayout()

        title = QLabel("🩺 Управление болезнями растений")
        title.setFont(QFont("Cambria Math", 14))
        title.setStyleSheet("color: #485935; margin: 5px;")
        layout.addWidget(title)

        # Кнопки
        buttons = QHBoxLayout()
        self.btn_add_disease = QPushButton("➕ Добавить")
        self.btn_edit_disease = QPushButton("✏️ Редактировать")
        self.btn_delete_disease = QPushButton("🗑️ Удалить")

        for btn in [self.btn_add_disease, self.btn_edit_disease, self.btn_delete_disease]:
            btn.setStyleSheet(self.get_button_style())

        buttons.addWidget(self.btn_add_disease)
        buttons.addWidget(self.btn_edit_disease)
        buttons.addWidget(self.btn_delete_disease)
        buttons.addStretch()
        layout.addLayout(buttons)

        # Таблица болезней
        self.diseases_table = QTableWidget()
        self.diseases_table.setColumnCount(4)
        self.diseases_table.setHorizontalHeaderLabels(["ID", "Название", "Описание", "Методы лечения"])
        self.diseases_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.diseases_table.setStyleSheet(self.get_table_style())

        header = self.diseases_table.horizontalHeader()
        header.resizeSection(0, 50)   # ID
        header.resizeSection(1, 150)  # Название
        header.resizeSection(2, 250)  # Описание
        header.resizeSection(3, 250)  # Методы лечения

        layout.addWidget(self.diseases_table)
        tab.setLayout(layout)
        return tab

    def create_relations_tab(self):
        """Создание вкладки для связей между таблицами"""
        tab = QWidget()
        layout = QVBoxLayout()

        title = QLabel("🔗 Управление связями между таблицами")
        title.setFont(QFont("Cambria Math", 14))
        title.setStyleSheet("color: #485935; margin: 5px;")
        layout.addWidget(title)

        # Подвкладки для разных типов связей
        self.relations_subtabs = QTabWidget()
        self.relations_subtabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid rgba(147, 162, 103, 0.3);
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: rgba(147, 162, 103, 0.5);
                color: #f8efda;
                padding: 8px 15px;
                border-radius: 5px;
                margin: 2px;
                font-size: 12px;
            }
            QTabBar::tab:selected {
                background-color: rgba(147, 162, 103, 0.8);
            }
        """)

        # Подвкладка 1: Растения-Семейства
        plant_family_tab = QWidget()
        plant_family_layout = QVBoxLayout()
        plant_family_title = QLabel("🌿 ↔️ 🌳 Связи растений с семействами")
        plant_family_title.setFont(QFont("Cambria Math", 12))
        plant_family_layout.addWidget(plant_family_title)

        plant_family_buttons = QHBoxLayout()
        self.btn_add_plant_family = QPushButton("➕ Добавить связь")
        self.btn_delete_plant_family = QPushButton("➖ Удалить связь")

        for btn in [self.btn_add_plant_family, self.btn_delete_plant_family]:
            btn.setStyleSheet(self.get_button_style())

        plant_family_buttons.addWidget(self.btn_add_plant_family)
        plant_family_buttons.addWidget(self.btn_delete_plant_family)
        plant_family_buttons.addStretch()
        plant_family_layout.addLayout(plant_family_buttons)

        self.plant_family_table = QTableWidget()
        self.plant_family_table.setColumnCount(4)
        self.plant_family_table.setHorizontalHeaderLabels(["ID связи", "ID растения", "ID семейства", "Растение → Семейство"])
        self.plant_family_table.setStyleSheet(self.get_table_style())

        # Размеры колонок для таблицы растений-семейств
        header = self.plant_family_table.horizontalHeader()
        header.resizeSection(0, 80)    # ID связи
        header.resizeSection(1, 100)   # ID растения
        header.resizeSection(2, 100)   # ID семейства
        header.resizeSection(3, 300)   # Растение → Семейство

        plant_family_layout.addWidget(self.plant_family_table)
        plant_family_tab.setLayout(plant_family_layout)

        # Подвкладка 2: Растения-Вредители
        plant_pest_tab = QWidget()
        plant_pest_layout = QVBoxLayout()
        plant_pest_title = QLabel("🌿 ↔️ 🐛 Связи растений с вредителями")
        plant_pest_title.setFont(QFont("Cambria Math", 12))
        plant_pest_layout.addWidget(plant_pest_title)

        plant_pest_buttons = QHBoxLayout()
        self.btn_add_plant_pest = QPushButton("➕ Добавить связь")
        self.btn_delete_plant_pest = QPushButton("➖ Удалить связь")

        for btn in [self.btn_add_plant_pest, self.btn_delete_plant_pest]:
            btn.setStyleSheet(self.get_button_style())

        plant_pest_buttons.addWidget(self.btn_add_plant_pest)
        plant_pest_buttons.addWidget(self.btn_delete_plant_pest)
        plant_pest_buttons.addStretch()
        plant_pest_layout.addLayout(plant_pest_buttons)

        self.plant_pest_table = QTableWidget()
        self.plant_pest_table.setColumnCount(4)
        self.plant_pest_table.setHorizontalHeaderLabels(["ID связи", "ID растения", "ID вредителя", "Растение → Вредитель"])
        self.plant_pest_table.setStyleSheet(self.get_table_style())

        # Размеры колонок для таблицы растений-вредителей
        header = self.plant_pest_table.horizontalHeader()
        header.resizeSection(0, 80)    # ID связи
        header.resizeSection(1, 100)   # ID растения
        header.resizeSection(2, 100)   # ID вредителя
        header.resizeSection(3, 300)   # Растение → Вредитель

        plant_pest_layout.addWidget(self.plant_pest_table)
        plant_pest_tab.setLayout(plant_pest_layout)

        # Подвкладка 3: Растения-Болезни
        plant_disease_tab = QWidget()
        plant_disease_layout = QVBoxLayout()
        plant_disease_title = QLabel("🌿 ↔️ 🩺 Связи растений с болезнями")
        plant_disease_title.setFont(QFont("Cambria Math", 12))
        plant_disease_layout.addWidget(plant_disease_title)

        plant_disease_buttons = QHBoxLayout()
        self.btn_add_plant_disease = QPushButton("➕ Добавить связь")
        self.btn_delete_plant_disease = QPushButton("➖ Удалить связь")

        for btn in [self.btn_add_plant_disease, self.btn_delete_plant_disease]:
            btn.setStyleSheet(self.get_button_style())

        plant_disease_buttons.addWidget(self.btn_add_plant_disease)
        plant_disease_buttons.addWidget(self.btn_delete_plant_disease)
        plant_disease_buttons.addStretch()
        plant_disease_layout.addLayout(plant_disease_buttons)

        self.plant_disease_table = QTableWidget()
        self.plant_disease_table.setColumnCount(4)
        self.plant_disease_table.setHorizontalHeaderLabels(["ID связи", "ID растения", "ID болезни", "Растение → Болезнь"])
        self.plant_disease_table.setStyleSheet(self.get_table_style())

        # Размеры колонок для таблицы растений-болезней
        header = self.plant_disease_table.horizontalHeader()
        header.resizeSection(0, 80)    # ID связи
        header.resizeSection(1, 100)   # ID растения
        header.resizeSection(2, 100)   # ID болезни
        header.resizeSection(3, 300)   # Растение → Болезнь

        plant_disease_layout.addWidget(self.plant_disease_table)
        plant_disease_tab.setLayout(plant_disease_layout)

        # Добавляем подвкладки
        self.relations_subtabs.addTab(plant_family_tab, "Растения ↔ Семейства")
        self.relations_subtabs.addTab(plant_pest_tab, "Растения ↔ Вредители")
        self.relations_subtabs.addTab(plant_disease_tab, "Растения ↔ Болезни")

        layout.addWidget(self.relations_subtabs)
        tab.setLayout(layout)
        return tab

    def create_system_tab(self):
        """Создание вкладки для экспорта"""
        tab = QWidget()
        layout = QVBoxLayout()

        title = QLabel("⚙️ Экспорт данных")
        title.setFont(QFont("Cambria Math", 14))
        title.setStyleSheet("color: #485935; margin: 5px;")
        layout.addWidget(title)

        # Экспорт
        export_layout = QHBoxLayout()
        export_layout.addWidget(QLabel("Формат экспорта:"))

        self.export_format = QComboBox()
        self.export_format.addItems(["PDF", "DOCX"])
        export_layout.addWidget(self.export_format)
        export_layout.addStretch()

        layout.addLayout(export_layout)

        # Кнопки экспорта для разных таблиц - сохраняем как атрибуты
        export_buttons = QVBoxLayout()

        sections = [
            ("Пользователи", "📊", "btn_export_users"),
            ("Семейства растений", "🌳", "btn_export_families"),
            ("Руководства по уходу", "📚", "btn_export_care_guides"),
            ("Местоположения", "🗺️", "btn_export_locations"),
            ("Фотографии", "📸", "btn_export_photos"),
            ("Растения", "🌿", "btn_export_plants"),
            ("Вредители", "🐛", "btn_export_pests"),
            ("Болезни", "🩺", "btn_export_diseases")
        ]

        for section_name, icon, btn_name in sections:
            btn_layout = QHBoxLayout()
            # Создаем атрибуты кнопок динамически
            setattr(self, btn_name, QPushButton(f"{icon} Экспорт {section_name}"))
            btn = getattr(self, btn_name)
            btn.setStyleSheet(self.get_button_style())
            btn_layout.addWidget(btn)
            btn_layout.addStretch()
            export_buttons.addLayout(btn_layout)

        layout.addLayout(export_buttons)
        layout.addStretch()

        tab.setLayout(layout)
        return tab

    def get_button_style(self):
        """Возвращает стиль для кнопок"""
        return """
            QPushButton {
                background-color: rgba(147, 162, 103, 1);
                color: #f8efda;
                border: none;
                border-radius: 20px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                font-family: "Times New Roman", serif;
                margin: 3px;
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
        """

    def get_table_style(self):
        """Возвращает стиль для таблиц"""
        return """
            QTableWidget {
                background-color: white;
                border: 2px solid rgba(147, 162, 103, 1);
                border-radius: 5px;
                font-family: "Cambria Math";
                font-size: 12px;
                gridline-color: rgba(147, 162, 103, 0.3);
            }
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid rgba(147, 162, 103, 0.2);
            }
            QTableWidget::item:selected {
                background-color: #ffe4b5;
                color: black;
            }
            QHeaderView::section {
                background-color: #f8efda;
                color: #485935;
                padding: 8px;
                border: none;
                border-right: 1px solid rgba(147, 162, 103, 0.5);
                border-bottom: 2px solid rgba(147, 162, 103, 1);
                font-family: "Cambria Math";
                font-size: 13px;
                font-weight: bold;
            }
            QHeaderView::section:last {
                border-right: none;
            }
            QTableCornerButton::section {
                background-color: #f8efda;
                border: none;
                border-bottom: 2px solid rgba(147, 162, 103, 1);
                border-right: 1px solid rgba(147, 162, 103, 0.5);
            }
            QScrollBar:vertical {
                border: none;
                background: white;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: rgba(147, 162, 103, 0.5);
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(147, 162, 103, 0.7);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """

    def load_data(self):
        """Загрузка данных всех таблиц"""
        self.controller.load_users()
        self.controller.load_families()
        self.controller.load_care_guides()
        self.controller.load_locations()
        self.controller.load_photos()
        self.controller.load_plants()
        self.controller.load_pests()
        self.controller.load_diseases()

        self.controller.load_plant_family_relations()
        self.controller.load_plant_pest_relations()
        self.controller.load_plant_disease_relations()

    def load_users(self):
        """Загрузка пользователей"""
        try:
            users = list(self.service.User.select().dicts())

            self.users_table.setRowCount(len(users))

            for i, user in enumerate(users):
                self.users_table.setItem(i, 0, QTableWidgetItem(str(user['id'])))
                self.users_table.setItem(i, 1, QTableWidgetItem(user['username']))
                self.users_table.setItem(i, 2, QTableWidgetItem(user.get('email', '')))
                self.users_table.setItem(i, 3, QTableWidgetItem(user.get('first_name', '')))
                self.users_table.setItem(i, 4, QTableWidgetItem(user.get('last_name', '')))

                role_item = QTableWidgetItem(user.get('role', 'user'))
                role_item.setForeground(QBrush(QColor("#FF5722") if user.get('role') == 'admin' else QColor("#2196F3")))
                self.users_table.setItem(i, 5, role_item)

                date_str = user.get('created_at', '')
                if date_str:
                    if isinstance(date_str, datetime):
                        date_item = QTableWidgetItem(date_str.strftime('%Y-%m-%d %H:%M:%S'))
                    else:
                        date_item = QTableWidgetItem(str(date_str)[:19])
                else:
                    date_item = QTableWidgetItem("N/A")
                self.users_table.setItem(i, 6, date_item)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка",
                               f"Не удалось загрузить пользователей:\n{str(e)}")

    def export_users(self):
        """Экспорт пользователей"""
        try:
            users = list(self.service.User.select().dicts())

            format_ = self.export_format.currentText()
            filename = f"users_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            if format_ == "JSON":
                filepath = self.service.export_to_json(users, filename)
            elif format_ == "CSV":
                filepath = self.service.export_to_csv(users, filename)

            if filepath and os.path.exists(filepath):
                QMessageBox.information(self, "Успех", f"Экспорт завершен:\n{filepath}")
            else:
                QMessageBox.warning(self, "Внимание", "Экспорт завершен")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка: {str(e)}")

    def logout(self):
        """Выход из системы"""
        self.service.close()
        self.close()



