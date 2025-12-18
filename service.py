from typing import Optional, List, Dict, Any
from models import *
from peewee import fn, JOIN
from datetime import datetime, date, timedelta
import json, csv, os, docx
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from docx.shared import Inches

class FlorariumService:
    def __init__(self):
        # Импортируем db из models
        from models import db

        # Добавляем атрибут database для доступа к подключению БД
        self.database = db
        self.User = User
        self.Plant = Plant
        self.PlantFamily = PlantFamily
        self.CareGuide = CareGuide
        self.PlantLocation = PlantLocation
        self.PlantPhoto = PlantPhoto
        self.Pest = Pest
        self.Disease = Disease
        self.PlantFamilyRelation = PlantFamilyRelation
        self.PlantPest = PlantPest
        self.PlantDisease = PlantDisease
        self.PlantInstance = PlantInstance
        self.InstancePhoto = InstancePhoto
        self.CareJournal = CareJournal

        # Создаем администратора при первом запуске
        if not User.select().where(User.username == 'admin').exists():
            User.create(
                username='admin',
                password='12345',
                email='admin@florarium.ru',
                first_name='Админ',
                last_name='Системы',
                role='admin'
            )
            print("👑 Администратор создан: admin / 12345")

    def create_user(self, username: str, password: str, email: str,
                           first_name: str, last_name: str,
                           birth_date = None, role: str = 'user') -> Optional[int]:
        """Создание нового пользователя"""
        try:
            # Проверяем, существует ли уже пользователь с таким логином или email
            existing_user = User.select().where(
                (User.username == username) | (User.email == email)
            ).first()

            if existing_user:
                if existing_user.username == username:
                    print(f"Пользователь с логином '{username}' уже существует")
                if existing_user.email == email:
                    print(f"Пользователь с email '{email}' уже существует")
                return None

            # Преобразуем birth_date в правильный формат
            birth_date_parsed = None
            if birth_date:
                if isinstance(birth_date, str):
                    try:
                        birth_date_parsed = datetime.strptime(birth_date, '%Y-%m-%d').date()
                    except ValueError:
                        print(f"Некорректный формат даты: {birth_date}. Ожидается 'yyyy-MM-dd'")
                        try:
                            birth_date_parsed = datetime.strptime(birth_date, '%d.%m.%Y').date()
                        except ValueError:
                            print(f"Не удалось распознать дату рождения: {birth_date}")
                elif hasattr(birth_date, 'toString'):
                    birth_date_parsed = datetime.strptime(birth_date.toString('yyyy-MM-dd'), '%Y-%m-%d').date()
                elif isinstance(birth_date, (datetime, date)):
                    if isinstance(birth_date, datetime):
                        birth_date_parsed = birth_date.date()
                    else:
                        birth_date_parsed = birth_date
                else:
                    print(f"Неизвестный тип даты: {type(birth_date)}")

            # Создаем нового пользователя
            user = User.create(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                birth_date=birth_date_parsed,
                role=role,
                created_at=datetime.now()
            )

            print(f"Пользователь '{username}' успешно создан (ID: {user.id})")
            return user.id

        except Exception as e:
            print(f"Ошибка при создании пользователя: {e}")
            import traceback
            traceback.print_exc()
            return None

    def add_user(self, user_data: Dict) -> Optional[User]:
        """Добавление пользователя"""
        try:
            # Проверка уникальности логина и email
            if User.select().where(User.username == user_data['username']).exists():
                raise ValueError("Пользователь с таким логином уже существует")

            if User.select().where(User.email == user_data['email']).exists():
                raise ValueError("Пользователь с таким email уже существует")

            # Создание пользователя
            user = User.create(**user_data)
            return user
        except Exception as e:
            print(f"Ошибка при добавлении пользователя: {e}")
            return None

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Аутентификация пользователя"""
        try:
            user = User.get(
                (User.username == username) &
                (User.password == password)
            )
            return user
        except User.DoesNotExist:
            return None
        except Exception as e:
            print(f"Ошибка аутентификации: {e}")
            return None

    def get_user_role(self, user_id: int) -> str:
        """Получение роли пользователя"""
        user = User.get_by_id(user_id)
        return user.role

    def get_total_records_count(self):
        """Получение общего количества записей во всех таблицах"""
        tables = [
            self.User, self.Plant, self.PlantFamily, self.CareGuide,
            self.PlantLocation, self.PlantPhoto, self.Pest, self.Disease,
            self.PlantInstance, self.CareJournal
        ]

        total = 0
        for table in tables:
            try:
                total += table.select().count()
            except:
                pass
        return total

    def close(self):
        """Закрытие соединения с БД"""
        if not db.is_closed():
            db.close()
