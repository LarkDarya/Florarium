from peewee import *
import os
from datetime import datetime
from database import db

class BaseModel(Model):
    class Meta:
        database = db

# 1. Пользователи (роли: admin, user)
class User(BaseModel):
    id = AutoField()
    username = CharField(unique=True, max_length=50)
    password = CharField(max_length=255)
    email = CharField(unique=True, max_length=100)
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    role = CharField(default='user', choices=['admin', 'user'])
    created_at = DateTimeField(default=datetime.now)
    birth_date = DateField(null=True)

    class Meta:
        table_name = 'users'

# 2. Семейства растений (категории/семейства)
class PlantFamily(BaseModel):
    id = AutoField()
    name = CharField(unique=True, max_length=100)
    description = TextField(null=True)

    class Meta:
        table_name = 'plant_families'


# 3. Руководство по уходу
class CareGuide(BaseModel):
    id = AutoField()
    watering = CharField(max_length=500, null=True)  # Полив
    light = IntegerField(null=True)  # Свет в люминах
    temperature_min = IntegerField(null=True)  # Мин температура
    temperature_max = IntegerField(null=True)  # Макс температура
    soil = CharField(max_length=500, null=True)  # Почва
    fertilizers = CharField(max_length=500, null=True)  # Удобрения
    humidity = IntegerField(null=True)  # Влажность в %

    class Meta:
        table_name = 'care_guides'


# 4. Местоположения растений (справочник природных ареалов)
class PlantLocation(BaseModel):
    id = AutoField()
    location_name = CharField(max_length=100, unique=True)
    description = TextField(null=True)

    class Meta:
        table_name = 'plant_locations'
        indexes = (
            (('location_name',), True),
        )


# 5. Фотографии растений
class PlantPhoto(BaseModel):
    id = AutoField()
    photo_url = CharField(max_length=255)

    class Meta:
        table_name = 'plant_photos'


# 6. Растения
class Plant(BaseModel):
    id = AutoField()
    scientific_name = CharField(max_length=300)
    description = TextField(null=True)

    # Одно основное руководство по уходу
    care_guide = ForeignKeyField(
        CareGuide,
        null=True,
        on_delete='SET NULL',
        backref='plant_for_care'
    )

    # Одно основное местоположение
    main_location = ForeignKeyField(
        PlantLocation,
        null=True,
        on_delete='SET NULL',
        backref='plants_here_main'
    )

    # Одно основное фото
    main_photo = ForeignKeyField(
        PlantPhoto,
        null=True,
        on_delete='SET NULL',
        backref='plant_main_photo'  # Основное фото для растения
    )

    class Meta:
        table_name = 'plants'


# 7. Связь растения с семейством (многие-ко-многим)
class PlantFamilyRelation(BaseModel):
    plant = ForeignKeyField(Plant, backref='families')
    family = ForeignKeyField(PlantFamily, backref='plants')

    class Meta:
        table_name = 'plant_family_relations'
        indexes = (
            (('plant', 'family'), True),  # Уникальная пара растение-семейство
        )

# 8. Вредители
class Pest(BaseModel):
    id = AutoField()
    name = CharField(max_length=100)
    description = TextField()
    treatment_methods = TextField()  # Методы лечения

    class Meta:
        table_name = 'pests'


# 9. Болезни растений
class Disease(BaseModel):
    id = AutoField()
    name = CharField(max_length=100)
    description = TextField()
    treatment_methods = TextField()  # Методы лечения

    class Meta:
        table_name = 'diseases'


# 10. Связь растения с вредителями
class PlantPest(BaseModel):
    plant = ForeignKeyField(Plant, backref='pests')
    pest = ForeignKeyField(Pest, backref='plants')

    class Meta:
        table_name = 'plant_pests'
        indexes = (
            (('plant', 'pest'), True),
        )


# 11. Связь растения с болезнями
class PlantDisease(BaseModel):
    plant = ForeignKeyField(Plant, backref='diseases')
    disease = ForeignKeyField(Disease, backref='plants')

    class Meta:
        table_name = 'plant_diseases'
        indexes = (
            (('plant', 'disease'), True),
        )

# 12. Экземпляры растений пользователей
class PlantInstance(BaseModel):
    id = AutoField()
    user = ForeignKeyField(User, backref='plant_instances')
    nickname = CharField(max_length=100, null=True)  # Имя растения
    description = TextField(null=True)
    acquisition_date = DateField(null=True)  # Когда приобрели
    age = IntegerField(null=True)  # Возраст в месяцах/годах
    health_status = CharField(
        choices=['excellent', 'good', 'fair', 'poor', 'critical'],
        default='good'
    )
    room = CharField(max_length=100, null=True)  # Комната
    location_notes = TextField(null=True)  # Особенности местоположения

    class Meta:
        table_name = 'plant_instances'


# 13. Фотографии экземпляров растений
class InstancePhoto(BaseModel):
    id = AutoField()
    instance = ForeignKeyField(PlantInstance, backref='photos', on_delete='CASCADE')
    photo_url = CharField(max_length=255)
    photo_date = DateField(default=datetime.now)  # Дата фотографии
    is_current = BooleanField(default=False)

    class Meta:
        table_name = 'instance_photos'


# 16. Журнал ухода
class CareJournal(BaseModel):
    """Журнал ухода за растениями."""
    id = AutoField()

    # Только самые необходимые поля
    instance = ForeignKeyField(PlantInstance, backref='care_journal')  # Экземпляр
    description = TextField(null=True)  # Заметки по уходу
    care_date = DateField(default=datetime.now)  # Дата ухода
    care_type = CharField(max_length=50)  # Тип ухода
    user = ForeignKeyField(User, backref='care_journal')  # Пользователь

    class Meta:
        table_name = 'care_journal'

# Функция создания таблиц
def create_tables():
    tables = [
        # Основные таблицы
        User,
        PlantFamily,
        CareGuide,
        PlantLocation,
        PlantPhoto,
        Pest,
        Disease,

        # Растения и связи
        Plant,
        PlantFamilyRelation,
        PlantPest,
        PlantDisease,

        # Таблицы пользователей
        PlantInstance,
        InstancePhoto,
        CareJournal
    ]

    from database import db
    if db.is_closed():
        db.connect()

    # Создаем таблицы
    db.create_tables(tables, safe=True)

    print("Таблицы созданы успешно!")
    print(f"Создано таблиц: {len(tables)}")

    # Закрываем соединение
    db.close()

if __name__ == '__main__':
    create_tables()
