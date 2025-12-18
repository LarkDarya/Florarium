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
from backup_manager import BackupManager

class AdminWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.service = FlorariumService()
        self.backup_manager = BackupManager(self.service)
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

        # Вкладка 11: Резервное копирование
        backup_tab = self.create_backup_tab()

        # Вкладка 12: Статистика
        stats_tab = self.create_stats_tab()

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
        self.tabs.addTab(backup_tab, "💾 Бэкапы")
        self.tabs.addTab(stats_tab, "📊 Статистика")

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



    def create_backup_tab(self):
        """Создание вкладки управления резервным копированием"""
        tab = QWidget()
        layout = QVBoxLayout()

        title = QLabel("💾 Управление резервным копированием")
        title.setFont(QFont("Cambria Math", 14))
        title.setStyleSheet("color: #485935; margin: 5px;")
        layout.addWidget(title)

        # Панель быстрого действия
        quick_action_group = QGroupBox("Быстрые действия")
        quick_action_layout = QVBoxLayout()

        # Кнопки быстрых действий
        buttons_layout = QGridLayout()
        buttons_layout.setSpacing(10)

        self.btn_create_backup = QPushButton("🔄 Создать резервную копию")
        self.btn_create_backup.setStyleSheet(self.get_button_style())
        self.btn_create_backup.clicked.connect(self.create_backup_now)

        self.btn_list_backups = QPushButton("📋 Показать резервные копии")
        self.btn_list_backups.setStyleSheet(self.get_button_style())
        self.btn_list_backups.clicked.connect(self.show_backups_list)

        buttons_layout.addWidget(self.btn_create_backup, 0, 0)
        buttons_layout.addWidget(self.btn_list_backups, 0, 1)

        quick_action_layout.addLayout(buttons_layout)
        quick_action_group.setLayout(quick_action_layout)
        layout.addWidget(quick_action_group)

        # Натсройка автоматического резервного копирования
        auto_backup_group = QGroupBox("Настройки автоматического резервного копирования")
        auto_backup_layout = QFormLayout()

        # Включение автоматического резервного копирования
        self.auto_backup_enabled = QCheckBox("Включить автоматическое резервное копирование")
        self.auto_backup_enabled.setChecked(self.backup_manager.backup_config.get('enabled', False))
        auto_backup_layout.addRow(self.auto_backup_enabled)

        # Частота резервного копирования
        self.backup_frequency = QComboBox()
        self.backup_frequency.addItems(["Ежедневно", "Еженедельно", "Ежемесячно"])

        frequency_map = {'daily': 'Ежедневно', 'weekly': 'Еженедельно', 'monthly': 'Ежемесячно'}
        current_freq = self.backup_manager.backup_config.get('frequency', 'daily')
        self.backup_frequency.setCurrentText(frequency_map.get(current_freq, 'Ежедневно'))
        auto_backup_layout.addRow("Частота:", self.backup_frequency)

        # Время выполнения
        self.backup_time = QTimeEdit()
        time_str = self.backup_manager.backup_config.get('time', '02:00')
        try:
            backup_time = QTime.fromString(time_str, 'HH:mm')
            self.backup_time.setTime(backup_time)
        except:
            self.backup_time.setTime(QTime(2, 0))
        auto_backup_layout.addRow("Время выполнения:", self.backup_time)

        # Формат резервной копии
        self.backup_format = QComboBox()
        self.backup_format.addItems(["ZIP архив", "JSON файл"])
        current_format = self.backup_manager.backup_config.get('backup_format', 'zip')
        self.backup_format.setCurrentText("ZIP архив" if current_format == 'zip' else "JSON файл")
        auto_backup_layout.addRow("Формат:", self.backup_format)

        # Включение фотографий
        self.include_photos = QCheckBox("Включать фотографии растений в резервную копию")
        self.include_photos.setChecked(self.backup_manager.backup_config.get('include_photos', True))
        auto_backup_layout.addRow(self.include_photos)

        # Хранение локальных копий
        self.retention_days = QSpinBox()
        self.retention_days.setRange(1, 365)
        self.retention_days.setValue(self.backup_manager.backup_config.get('local_retention_days', 7))
        self.retention_days.setSuffix(" дней")
        auto_backup_layout.addRow("Хранить локально:", self.retention_days)

        auto_backup_group.setLayout(auto_backup_layout)
        layout.addWidget(auto_backup_group)

        # Удаленные цели резервного копирования
        remote_targets_group = QGroupBox("Удаленные цели резервного копирования")
        remote_layout = QVBoxLayout()

        # Список удаленных целей
        self.remote_targets_list = QListWidget()
        self.remote_targets_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #93a267;
                border-radius: 5px;
                min-height: 50px;
            }
        """)
        self.load_remote_targets_to_list()
        remote_layout.addWidget(self.remote_targets_list)

        # Кнопки управления удаленными целями
        remote_buttons = QHBoxLayout()

        self.btn_add_remote = QPushButton("➕ Добавить цель")
        self.btn_edit_remote = QPushButton("✏️ Редактировать")
        self.btn_delete_remote = QPushButton("🗑️ Удалить")

        for btn in [self.btn_add_remote, self.btn_edit_remote, self.btn_delete_remote]:
            btn.setStyleSheet(self.get_button_style())

        self.btn_add_remote.clicked.connect(self.add_remote_target)
        self.btn_delete_remote.clicked.connect(self.delete_remote_target)

        remote_buttons.addWidget(self.btn_add_remote)
        remote_buttons.addWidget(self.btn_edit_remote)
        remote_buttons.addWidget(self.btn_delete_remote)
        remote_buttons.addStretch()

        remote_layout.addLayout(remote_buttons)
        remote_targets_group.setLayout(remote_layout)
        layout.addWidget(remote_targets_group)

        # Кнопки управления
        control_buttons = QHBoxLayout()

        self.btn_save_settings = QPushButton("💾 Сохранить настройки")
        self.btn_save_settings.setStyleSheet(self.get_button_style())
        self.btn_save_settings.clicked.connect(self.save_backup_settings)

        control_buttons.addWidget(self.btn_save_settings)
        control_buttons.addStretch()

        layout.addLayout(control_buttons)
        layout.addStretch()

        tab.setLayout(layout)
        return tab

    def load_remote_targets_to_list(self):
        """Загрузка списка удаленных целей в ListWidget"""
        self.remote_targets_list.clear()
        remote_targets = self.backup_manager.backup_config.get('remote_targets', [])

        for target in remote_targets:
            target_type = target.get('type', 'unknown')
            target_name = target.get('name', 'Без названия')
            target_path = target.get('path', target.get('host', 'Не указан'))

            item_text = f"{self.get_target_icon(target_type)} {target_name} - {target_path}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, target)
            self.remote_targets_list.addItem(item)

    def get_target_icon(self, target_type):
        """Получение иконки для типа цели"""
        icons = {
            'network_share': '📁',
            'sftp': '🔒',
            'dropbox': '☁️',
            'google_drive': '📊',
            'yandex_disk': '🌐'
        }
        return icons.get(target_type, '❓')

    def create_backup_now(self):
        """Создание резервной копии сейчас"""
        try:
            # Показываем диалог прогресса
            progress_dialog = QProgressDialog("Создание резервной копии...", "Отмена", 0, 100, self)
            progress_dialog.setWindowTitle("Резервное копирование")
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.show()

            # Обновляем прогресс
            progress_dialog.setValue(10)
            QApplication.processEvents()

            # Создаем резервную копию
            backup_format = 'zip' if self.backup_format.currentText() == 'ZIP архив' else 'json'
            backup_file = self.backup_manager.create_backup(backup_format)

            progress_dialog.setValue(50)

            if backup_file:
                # Копируем в удаленные цели
                remote_targets = self.backup_manager.backup_config.get('remote_targets', [])
                for i, target in enumerate(remote_targets):
                    progress_dialog.setLabelText(f"Копирование в {target.get('name', 'цель')}...")
                    self.backup_manager.backup_to_network(backup_file, target)

                    progress_val = 50 + (i + 1) * (40 / len(remote_targets))
                    progress_dialog.setValue(int(progress_val))
                    QApplication.processEvents()

                progress_dialog.setValue(100)
                progress_dialog.close()

                # Показываем информацию о созданной резервной копии
                file_size = os.path.getsize(backup_file) / (1024 * 1024)  # в MB
                backup_info = f"""
✅ Резервная копия успешно создана!

📁 Файл: {os.path.basename(backup_file)}
📊 Размер: {file_size:.2f} MB
📍 Расположение: {backup_file}

Резервная копия содержит все данные базы данных и фотографии растений.
                """

                QMessageBox.information(self, "Успех", backup_info)
            else:
                progress_dialog.close()
                QMessageBox.warning(self, "Ошибка", "Не удалось создать резервную копию")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка создания резервной копии:\n{str(e)}")

    def show_backups_list(self):
        """Показать список резервных копий"""
        try:
            backups = self.backup_manager.list_backups()

            if not backups:
                QMessageBox.information(self, "Список резервных копий", "Резервные копии не найдены.")
                return

            # Создаем диалоговое окно для отображения списка
            dialog = QDialog(self)
            dialog.setWindowTitle("📋 Список резервных копий")
            dialog.resize(800, 500)

            layout = QVBoxLayout()

            # Создаем таблицу для отображения резервных копий
            table = QTableWidget()
            table.setColumnCount(5)
            table.setHorizontalHeaderLabels([
                "Имя файла", "Размер", "Дата создания", "Тип", "Целостность"
            ])
            table.setRowCount(len(backups))
            table.setEditTriggers(QTableWidget.NoEditTriggers)
            table.setSelectionBehavior(QTableWidget.SelectRows)

            # Заполняем таблицу
            for i, backup_info in enumerate(backups):
                # Имя файла
                file_path = backup_info.get('file', '') or backup_info.get('path', '') or backup_info.get('name', '')
                if isinstance(file_path, str):
                    file_name = os.path.basename(file_path)
                else:
                    file_name = str(file_path)
                table.setItem(i, 0, QTableWidgetItem(file_name))

                # Размер
                size = backup_info.get('size', 0)
                size_str = self._format_size(size)
                table.setItem(i, 1, QTableWidgetItem(size_str))

                # Дата создания
                created = backup_info.get('created')
                if created:
                    if isinstance(created, datetime):
                        date_str = created.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        date_str = str(created)
                else:
                    date_str = 'Неизвестно'
                table.setItem(i, 2, QTableWidgetItem(date_str))

                # Тип
                backup_type = backup_info.get('type', 'unknown')
                table.setItem(i, 3, QTableWidgetItem(backup_type))

                # Целостность
                integrity = backup_info.get('integrity', False)
                integrity_item = QTableWidgetItem('✓' if integrity else '✗')
                integrity_item.setTextAlignment(Qt.AlignCenter)
                integrity_item.setForeground(QColor('green' if integrity else 'red'))
                table.setItem(i, 4, integrity_item)

            table.resizeColumnsToContents()
            layout.addWidget(table)

            # Кнопки действий
            buttons_layout = QHBoxLayout()

            btn_restore = QPushButton("Восстановить")
            btn_delete = QPushButton("Удалить")
            btn_close = QPushButton("Закрыть")

            def restore_selected():
                selected = table.selectedItems()
                if not selected:
                    QMessageBox.warning(dialog, "Внимание", "Выберите резервную копию для восстановления")
                    return

                row = selected[0].row()
                file_path = backups[row].get('file') or backups[row].get('path')
                if file_path:
                    self.restore_backup(file_path)
                    dialog.close()

            def delete_selected():
                selected = table.selectedItems()
                if not selected:
                    QMessageBox.warning(dialog, "Внимание", "Выберите резервную копию для удаления")
                    return

                row = selected[0].row()
                file_path = backups[row].get('file') or backups[row].get('path')
                if file_path:
                    self.delete_backup(file_path)
                    # Обновляем список
                    dialog.close()
                    self.show_backups_list()

            btn_restore.clicked.connect(restore_selected)
            btn_delete.clicked.connect(delete_selected)
            btn_close.clicked.connect(dialog.close)

            buttons_layout.addWidget(btn_restore)
            buttons_layout.addWidget(btn_delete)
            buttons_layout.addStretch()
            buttons_layout.addWidget(btn_close)

            layout.addLayout(buttons_layout)
            dialog.setLayout(layout)
            dialog.exec()

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить список резервных копий:\n{str(e)}")

    def restore_backup(self, backup_path):
        """Восстановление из резервной копии"""
        try:
            if not os.path.exists(backup_path):
                QMessageBox.warning(self, "Ошибка", f"Файл не найден:\n{backup_path}")
                return

            backup_name = os.path.basename(backup_path)

            # Подтверждение
            reply = QMessageBox.question(
                self,
                "Подтверждение восстановления",
                f"Вы уверены, что хотите восстановить данные из резервной копии?\n\n{backup_name}\n\n"
                "⚠️ Внимание: Все текущие данные будут заменены!",
                QMessageBox.Yes | QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                # Показываем диалог прогресса
                progress_dialog = QProgressDialog("Восстановление данных...", "Отмена", 0, 100, self)
                progress_dialog.setWindowTitle("Восстановление")
                progress_dialog.setWindowModality(Qt.WindowModal)
                progress_dialog.show()

                progress_dialog.setValue(20)
                QApplication.processEvents()

                # Выполняем восстановление
                success = self.backup_manager.restore_backup(backup_path)

                progress_dialog.setValue(80)
                QApplication.processEvents()

                if success:
                    progress_dialog.setValue(100)
                    progress_dialog.close()
                    QMessageBox.information(self, "Успех", "Данные успешно восстановлены!")
                    # Обновляем данные в окне
                    self.load_data()
                else:
                    progress_dialog.close()
                    QMessageBox.warning(self, "Ошибка", "Не удалось восстановить данные")

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка восстановления:\n{str(e)}")

    def delete_backup(self, backup_path):
        """Удаление резервной копии"""
        try:
            backup_name = os.path.basename(backup_path)

            reply = QMessageBox.question(
                self,
                "Подтверждение удаления",
                f"Вы уверены, что хотите удалить резервную копию?\n\n{backup_name}",
                QMessageBox.Yes | QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                if os.path.exists(backup_path):
                    os.remove(backup_path)
                    QMessageBox.information(self, "Успех", f"Резервная копия удалена:\n{backup_name}")
                else:
                    QMessageBox.warning(self, "Ошибка", "Файл не найден")

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка удаления:\n{str(e)}")

    def _format_size(self, size_bytes):
        """Форматирование размера файла"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"

    def cleanup_old_backups(self):
        """Очистка старых резервных копий"""
        retention_days = self.backup_manager.backup_config.get('local_retention_days', 7)

        if QMessageBox.question(self, "Подтверждение",
                               f"Удалить резервные копии старше {retention_days} дней?") == QMessageBox.Yes:
            deleted_count = self.backup_manager.cleanup_old_backups(retention_days)

            if deleted_count > 0:
                QMessageBox.information(self, "Очистка", f"Удалено {deleted_count} старых резервных копий")
            else:
                QMessageBox.information(self, "Очистка", "Старые резервные копии не найдены")

    def add_remote_target(self):
        """Добавление новой удаленной цели"""
        dialog = QDialog(self)
        dialog.setWindowTitle("➕ Добавить удаленную цель")
        dialog.resize(400, 300)

        layout = QVBoxLayout()

        form_layout = QFormLayout()

        # Тип цели
        target_type_combo = QComboBox()
        target_type_combo.addItems(["Сетевая папка (Windows/Linux)", "SFTP сервер", "Dropbox"])
        form_layout.addRow("Тип цели:", target_type_combo)

        # Имя цели
        target_name = QLineEdit()
        target_name.setPlaceholderText("Мой сервер, Облако и т.д.")
        form_layout.addRow("Имя цели:", target_name)

        # Поля будут добавляться динамически
        dynamic_widgets = {}

        def on_type_changed(index):
            for widget in dynamic_widgets.values():
                if widget.parent():
                    form_layout.removeRow(widget)
            dynamic_widgets.clear()

            if index == 0:
                path_input = QLineEdit()
                path_input.setPlaceholderText("\\\\server\\backups или /mnt/backups")
                form_layout.addRow("Сетевой путь:", path_input)
                dynamic_widgets['path'] = path_input

                username_input = QLineEdit()
                username_input.setPlaceholderText("Имя пользователя (опционально)")
                form_layout.addRow("Пользователь:", username_input)
                dynamic_widgets['username'] = username_input

                password_input = QLineEdit()
                password_input.setPlaceholderText("Пароль (опционально)")
                password_input.setEchoMode(QLineEdit.Password)
                form_layout.addRow("Пароль:", password_input)
                dynamic_widgets['password'] = password_input

            elif index == 1:  # SFTP
                host_input = QLineEdit()
                host_input.setPlaceholderText("sftp.example.com")
                form_layout.addRow("Хост:", host_input)
                dynamic_widgets['host'] = host_input

                port_input = QSpinBox()
                port_input.setRange(1, 65535)
                port_input.setValue(22)
                form_layout.addRow("Порт:", port_input)
                dynamic_widgets['port'] = port_input

                username_input = QLineEdit()
                username_input.setPlaceholderText("Имя пользователя")
                form_layout.addRow("Пользователь:", username_input)
                dynamic_widgets['username'] = username_input

                password_input = QLineEdit()
                password_input.setPlaceholderText("Пароль")
                password_input.setEchoMode(QLineEdit.Password)
                form_layout.addRow("Пароль:", password_input)
                dynamic_widgets['password'] = password_input

                path_input = QLineEdit()
                path_input.setPlaceholderText("/backups/florarium")
                path_input.setText("/backups/florarium")
                form_layout.addRow("Удаленный путь:", path_input)
                dynamic_widgets['path'] = path_input

            elif index == 2:  # Dropbox
                token_input = QLineEdit()
                token_input.setPlaceholderText("access_token")
                form_layout.addRow("Access Token:", token_input)
                dynamic_widgets['access_token'] = token_input

                path_input = QLineEdit()
                path_input.setPlaceholderText("/florarium_backups")
                path_input.setText("/florarium_backups")
                form_layout.addRow("Путь в Dropbox:", path_input)
                dynamic_widgets['path'] = path_input

        target_type_combo.currentIndexChanged.connect(on_type_changed)
        on_type_changed(0)
        layout.addLayout(form_layout)

        # Кнопки
        buttons_layout = QHBoxLayout()
        btn_save = QPushButton("Сохранить")
        btn_cancel = QPushButton("Отмена")

        btn_save.clicked.connect(lambda: save_target())
        btn_cancel.clicked.connect(dialog.reject)

        buttons_layout.addWidget(btn_save)
        buttons_layout.addWidget(btn_cancel)
        layout.addLayout(buttons_layout)

        def save_target():
            # Собираем данные
            target_data = {
                'name': target_name.text().strip() or "Новая цель",
            }

            index = target_type_combo.currentIndex()
            if index == 0:  # Сетевая папка
                target_data.update({
                    'type': 'network_share',
                    'path': dynamic_widgets.get('path', '').text().strip(),
                    'username': dynamic_widgets.get('username', '').text().strip() or None,
                    'password': dynamic_widgets.get('password', '').text().strip() or None
                })
            elif index == 1:  # SFTP
                target_data.update({
                    'type': 'sftp',
                    'host': dynamic_widgets.get('host', '').text().strip(),
                    'port': dynamic_widgets.get('port', port_input).value(),
                    'username': dynamic_widgets.get('username', '').text().strip(),
                    'password': dynamic_widgets.get('password', '').text().strip(),
                    'path': dynamic_widgets.get('path', '').text().strip()
                })
            elif index == 2:  # Dropbox
                target_data.update({
                    'type': 'cloud',
                    'cloud_type': 'dropbox',
                    'access_token': dynamic_widgets.get('access_token', '').text().strip(),
                    'path': dynamic_widgets.get('path', '').text().strip()
                })

            # Добавляем в конфигурацию
            remote_targets = self.backup_manager.backup_config.get('remote_targets', [])
            remote_targets.append(target_data)
            self.backup_manager.backup_config['remote_targets'] = remote_targets

            # Обновляем список
            self.load_remote_targets_to_list()

            QMessageBox.information(self, "Успех", "Цель успешно добавлена!")
            dialog.accept()

        dialog.setLayout(layout)
        dialog.exec()

    def delete_remote_target(self):
        """Удаление выбранной удаленной цели"""
        selected_items = self.remote_targets_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Внимание", "Выберите цель для удаления")
            return

        item = selected_items[0]
        target_name = item.text().split(' - ')[0][2:]  # Убираем иконку и пробел

        if QMessageBox.question(self, "Подтверждение",
                               f"Удалить цель '{target_name}'?") == QMessageBox.Yes:
            # Удаляем из конфигурации
            current_row = self.remote_targets_list.row(item)
            remote_targets = self.backup_manager.backup_config.get('remote_targets', [])

            if 0 <= current_row < len(remote_targets):
                remote_targets.pop(current_row)
                self.backup_manager.backup_config['remote_targets'] = remote_targets
                self.load_remote_targets_to_list()

                QMessageBox.information(self, "Успех", "Цель удалена")

    def save_backup_settings(self):
        """Сохранение настроек резервного копирования"""
        try:
            self.backup_manager.backup_config['enabled'] = self.auto_backup_enabled.isChecked()

            # Частота
            frequency_map = {
                'Ежедневно': 'daily',
                'Еженедельно': 'weekly',
                'Ежемесячно': 'monthly'
            }
            self.backup_manager.backup_config['frequency'] = frequency_map.get(
                self.backup_frequency.currentText(), 'daily'
            )

            # Время
            self.backup_manager.backup_config['time'] = self.backup_time.time().toString('HH:mm')

            # Формат
            self.backup_manager.backup_config['backup_format'] = 'zip' if \
                self.backup_format.currentText() == 'ZIP архив' else 'json'

            # Фотографии
            self.backup_manager.backup_config['include_photos'] = self.include_photos.isChecked()

            # Хранение
            self.backup_manager.backup_config['local_retention_days'] = self.retention_days.value()

            # Сохраняем конфигурацию
            if self.backup_manager.save_config():
                QMessageBox.information(self, "Успех", "Настройки сохранены!")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось сохранить настройки")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка сохранения настроек:\n{str(e)}")

    def create_stats_tab(self):
        """Создание вкладки со статистикой пользователей"""
        tab = QWidget()
        layout = QVBoxLayout()

        title = QLabel("📊 Статистика пользователей")
        title.setFont(QFont("Cambria Math", 14))
        title.setStyleSheet("color: #485935; margin: 5px;")
        layout.addWidget(title)

        # Кнопки управления - добавляем как атрибуты
        stats_buttons = QHBoxLayout()
        self.btn_refresh_stats = QPushButton("🔄 Обновить")
        self.btn_refresh_stats.setStyleSheet(self.get_button_style())
        self.btn_refresh_stats.clicked.connect(self.load_stats)

        stats_buttons.addWidget(self.btn_refresh_stats)
        stats_buttons.addStretch()
        layout.addLayout(stats_buttons)

        # Общая статистика
        general_group = QGroupBox("Общая статистика")
        general_layout = QGridLayout()

        # Показатели общей статистики
        self.total_users_label = QLabel("Всего пользователей: 0")
        self.active_users_label = QLabel("Активных пользователей: 0")
        self.admins_label = QLabel("Администраторов: 0")
        self.regular_users_label = QLabel("Обычных пользователей: 0")
        self.avg_registration_label = QLabel("Среднее время регистрации: -")

        general_layout.addWidget(self.total_users_label, 0, 0)
        general_layout.addWidget(self.active_users_label, 0, 1)
        general_layout.addWidget(self.admins_label, 1, 0)
        general_layout.addWidget(self.regular_users_label, 1, 1)
        general_layout.addWidget(self.avg_registration_label, 2, 0, 1, 2)

        general_group.setLayout(general_layout)
        layout.addWidget(general_group)

        # Таблицы
        tables_container = QWidget()
        tables_layout = QHBoxLayout()
        tables_container.setLayout(tables_layout)

        # Статистика по дням недели
        days_group = QGroupBox("📅 Регистрации по дням недели")
        days_group.setMinimumWidth(350)
        days_layout = QVBoxLayout()

        self.days_table = QTableWidget()
        self.days_table.setColumnCount(2)
        self.days_table.setHorizontalHeaderLabels(["День недели", "Кол-во"])
        self.days_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.days_table.setStyleSheet(self.get_table_style())
        self.days_table.setMinimumHeight(300)

        # Устанавливаем фиксированные строки для дней недели
        days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        self.days_table.setRowCount(len(days_of_week))

        for i, day in enumerate(days_of_week):
            self.days_table.setItem(i, 0, QTableWidgetItem(day))
            self.days_table.setItem(i, 1, QTableWidgetItem("0"))

        # Настройка ширины колонок
        header = self.days_table.horizontalHeader()
        header.resizeSection(0, 180)  # День недели
        header.resizeSection(1, 100)  # Количество

        days_layout.addWidget(self.days_table)
        days_group.setLayout(days_layout)
        tables_layout.addWidget(days_group)

        # Статистика по месяцам
        months_group = QGroupBox("📆 Регистрации по месяцам")
        months_group.setMinimumWidth(350)
        months_layout = QVBoxLayout()

        self.months_table = QTableWidget()
        self.months_table.setColumnCount(2)
        self.months_table.setHorizontalHeaderLabels(["Месяц", "Кол-во"])
        self.months_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.months_table.setStyleSheet(self.get_table_style())
        self.months_table.setMinimumHeight(300)

        # Устанавливаем фиксированные строки для месяцев
        months_names = [
            "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
            "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
        ]
        self.months_table.setRowCount(len(months_names))

        for i, month in enumerate(months_names):
            self.months_table.setItem(i, 0, QTableWidgetItem(month))
            self.months_table.setItem(i, 1, QTableWidgetItem("0"))

        # Настройка ширины колонок
        header = self.months_table.horizontalHeader()
        header.resizeSection(0, 180)  # Месяц
        header.resizeSection(1, 100)  # Количество

        months_layout.addWidget(self.months_table)
        months_group.setLayout(months_layout)
        tables_layout.addWidget(months_group)

        # Статистика по возрастным группам
        age_group = QGroupBox("👤 Возрастные группы")
        age_group.setMinimumWidth(350)
        age_layout = QVBoxLayout()

        self.age_table = QTableWidget()
        self.age_table.setColumnCount(2)
        self.age_table.setHorizontalHeaderLabels(["Возрастная группа", "Кол-во"])
        self.age_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.age_table.setStyleSheet(self.get_table_style())
        self.age_table.setMinimumHeight(300)

        # Устанавливаем фиксированные строки для возрастных групп
        age_groups_names = ["До 18 лет", "18-25 лет", "26-35 лет", "36-50 лет", "Старше 50 лет", "Не указан"]
        self.age_table.setRowCount(len(age_groups_names))

        for i, group in enumerate(age_groups_names):
            self.age_table.setItem(i, 0, QTableWidgetItem(group))
            self.age_table.setItem(i, 1, QTableWidgetItem("0"))

        # Настройка ширины колонок
        header = self.age_table.horizontalHeader()
        header.resizeSection(0, 180)
        header.resizeSection(1, 100)

        age_layout.addWidget(self.age_table)
        age_group.setLayout(age_layout)
        tables_layout.addWidget(age_group)

        layout.addWidget(tables_container)
        layout.addStretch()

        tab.setLayout(layout)
        return tab

    def load_stats(self):
        """Загрузка статистики пользователей"""
        try:
            users = list(self.service.User.select().dicts())

            # Общая статистика
            total_users = len(users)
            admins = sum(1 for user in users if user.get('role') == 'admin')
            regular_users = total_users - admins

            # Активные пользователи
            active_users = 0
            avg_registration_days = 0
            registration_days = []
            now = datetime.now()

            for user in users:
                created_at = user.get('created_at')
                if created_at:
                    created_date = self.parse_date(created_at)

                    if created_date:
                        # Вычисляем разницу между двумя datetime объектами
                        days_since_registration = (now - created_date).days
                        registration_days.append(days_since_registration)

                        if days_since_registration <= 30:
                            active_users += 1

            avg_registration_days = sum(registration_days) // len(registration_days) if registration_days else 0

            # Обновляем общую статистику
            self.total_users_label.setText(f"Всего пользователей: {total_users}")
            self.active_users_label.setText(f"Активных пользователей: {active_users}")
            self.admins_label.setText(f"Администраторов: {admins}")
            self.regular_users_label.setText(f"Обычных пользователей: {regular_users}")
            self.avg_registration_label.setText(f"Среднее время регистрации: {avg_registration_days} дней")

            # Статистика по дням недели
            days_count = {"Понедельник": 0, "Вторник": 0, "Среда": 0, "Четверг": 0,
                         "Пятница": 0, "Суббота": 0, "Воскременье": 0}
            days_mapping = {0: "Понедельник", 1: "Вторник", 2: "Среда", 3: "Четверг",
                          4: "Пятница", 5: "Суббота", 6: "Воскресенье"}

            for user in users:
                created_at = user.get('created_at')
                if created_at:
                    created_date = self.parse_date(created_at)

                    if created_date:
                        day_of_week = created_date.weekday()
                        day_name = days_mapping.get(day_of_week, "Неизвестно")
                        if day_name in days_count:
                            days_count[day_name] += 1

            # Обновляем таблицу дней недели
            for i in range(self.days_table.rowCount()):
                day_name = self.days_table.item(i, 0).text()
                count = days_count.get(day_name, 0)
                self.days_table.setItem(i, 1, QTableWidgetItem(str(count)))

            # Статистика по месяцам
            months_count = {i: 0 for i in range(1, 13)}
            months_names = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                          "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

            for user in users:
                created_at = user.get('created_at')
                if created_at:
                    created_date = self.parse_date(created_at)

                    if created_date:
                        month = created_date.month
                        months_count[month] += 1

            # Обновляем таблицу месяцев
            for i in range(self.months_table.rowCount()):
                month_name = self.months_table.item(i, 0).text()
                month_index = months_names.index(month_name) + 1
                count = months_count.get(month_index, 0)
                self.months_table.setItem(i, 1, QTableWidgetItem(str(count)))

            # Статистика по возрасту
            age_groups = {
                "До 18 лет": 0,
                "18-25 лет": 0,
                "26-35 лет": 0,
                "36-50 лет": 0,
                "Старше 50 лет": 0,
                "Не указан": 0
            }

            today = date.today()

            for user in users:
                birth_date_str = user.get('birth_date')
                print(f"Пользователь {user.get('id')}: birth_date = {birth_date_str}")

                if birth_date_str:
                    # Пробуем распарсить дату рождения
                    birth_date = self.parse_birth_date(birth_date_str)

                    if birth_date:
                        # Вычисляем возраст
                        age = today.year - birth_date.year
                        if (today.month, today.day) < (birth_date.month, birth_date.day):
                            age -= 1

                        print(f"  Дата рождения: {birth_date}, Возраст: {age}")

                        if age < 18:
                            age_groups["До 18 лет"] += 1
                        elif 18 <= age <= 25:
                            age_groups["18-25 лет"] += 1
                        elif 26 <= age <= 35:
                            age_groups["26-35 лет"] += 1
                        elif 36 <= age <= 50:
                            age_groups["36-50 лет"] += 1
                        else:
                            age_groups["Старше 50 лет"] += 1
                    else:
                        print(f"  Не удалось распарсить дату рождения: {birth_date_str}")
                        age_groups["Не указан"] += 1
                else:
                    print(f"  Дата рождения не указана")
                    age_groups["Не указан"] += 1

            # Обновляем таблицу возрастных групп
            for i in range(self.age_table.rowCount()):
                group_name = self.age_table.item(i, 0).text()
                count = age_groups.get(group_name, 0)
                self.age_table.setItem(i, 1, QTableWidgetItem(str(count)))

            # Автоматически изменяем размер колонок
            self.days_table.resizeColumnsToContents()
            self.months_table.resizeColumnsToContents()
            self.age_table.resizeColumnsToContents()

            print(f"Итоговые возрастные группы: {age_groups}")

        except Exception as e:
            print(f"Ошибка при загрузке статистики: {e}")
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить статистику:\n{str(e)}")

    def parse_date(self, date_value):
        """Парсинг даты из разных форматов"""
        if not date_value:
            return None

        try:
            if isinstance(date_value, datetime):
                return date_value
            elif isinstance(date_value, str):
                for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%Y-%m-%dT%H:%M:%S',
                           '%d.%m.%Y %H:%M:%S', '%d.%m.%Y', '%Y/%m/%d', '%d/%m/%Y']:
                    try:
                        return datetime.strptime(date_value, fmt)
                    except ValueError:
                        continue
        except Exception as e:
            print(f"Ошибка парсинга даты {date_value}: {e}")

        return None

    def parse_birth_date(self, birth_date_str):
        """Специальный метод для парсинга даты рождения"""
        if not birth_date_str:
            return None

        if isinstance(birth_date_str, datetime):
            return birth_date_str.date()
        elif isinstance(birth_date_str, date):
            return birth_date_str

        if isinstance(birth_date_str, str):
            birth_date_str = birth_date_str.strip()

            date_formats = [
                '%Y-%m-%d',      # 2023-12-31
                '%d.%m.%Y',      # 31.12.2023
                '%Y/%m/%d',      # 2023/12/31
                '%d/%m/%Y',      # 31/12/2023
                '%Y-%m-%d %H:%M:%S',  # 2023-12-31 00:00:00
                '%d.%m.%Y %H:%M:%S',  # 31.12.2023 00:00:00
            ]

            for fmt in date_formats:
                try:
                    if ' %H:%M:%S' in fmt:
                        dt = datetime.strptime(birth_date_str, fmt)
                        return dt.date()
                    else:
                        return datetime.strptime(birth_date_str, fmt).date()
                except ValueError:
                    continue

            try:
                if len(birth_date_str) == 4 and birth_date_str.isdigit():
                    year = int(birth_date_str)
                    return date(year, 1, 1)
            except:
                pass

        return None

    def export_stats(self):
        """Экспорт статистики в файл"""
        try:
            # Собираем данные статистики
            stats_data = {
                "total_users": self.total_users_label.text().split(": ")[1],
                "active_users": self.active_users_label.text().split(": ")[1],
                "admins": self.admins_label.text().split(": ")[1],
                "regular_users": self.regular_users_label.text().split(": ")[1],
                "avg_registration": self.avg_registration_label.text().split(": ")[1],
                "days_of_week": {},
                "months": {},
                "age_groups": {}
            }

            # Собираем данные из таблиц
            for i in range(self.days_table.rowCount()):
                day = self.days_table.item(i, 0).text()
                count = self.days_table.item(i, 1).text()
                stats_data["days_of_week"][day] = count

            for i in range(self.months_table.rowCount()):
                month = self.months_table.item(i, 0).text()
                count = self.months_table.item(i, 1).text()
                stats_data["months"][month] = count

            for i in range(self.age_table.rowCount()):
                group = self.age_table.item(i, 0).text()
                count = self.age_table.item(i, 1).text()
                stats_data["age_groups"][group] = count

            # Используем экспорт из сервиса
            format_ = self.export_format.currentText()
            filename = f"user_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            if format_ == "PDF":
                filepath = self.service.export_to_pdf(stats_data, filename)
            elif format_ == "DOCX":
                filepath = self.service.export_to_docx(stats_data, filename)

            if filepath and os.path.exists(filepath):
                QMessageBox.information(self, "Успех", f"Экспорт завершен:\n{filepath}")
            else:
                QMessageBox.warning(self, "Внимание", "Экспорт завершен")

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось экспортировать статистику:\n{str(e)}")

    def logout(self):
        """Выход из системы"""
        self.service.close()
        self.close()



