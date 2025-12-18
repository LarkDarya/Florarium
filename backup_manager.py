# backup_manager.py
import json
import os
import shutil
import zipfile
import hashlib
import threading
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Any
from peewee import Model, ForeignKeyField, DoesNotExist
import pickle

class BackupManager:
    """Улучшенный менеджер резервного копирования с использованием ORM"""

    def __init__(self, service):
        self.service = service
        self.config_file = 'backup_config.json'
        self.backup_config = self.load_default_config()
        self.load_config()

        # Получаем все модели из сервиса
        self.models = self._get_all_models()

        # Порядок таблиц для корректного экспорта/импорта
        self.table_order = self._determine_table_order()

        # Карта моделей для быстрого доступа
        self.model_map = self._create_model_map()

    def _get_all_models(self):
        """Получаем все модели из сервиса через рефлексию"""
        models = []
        for attr_name in dir(self.service):
            attr = getattr(self.service, attr_name)
            if isinstance(attr, type) and issubclass(attr, Model) and attr != Model:
                models.append(attr)
        return models

    def _create_model_map(self):
        """Создаем карту имя_таблицы -> модель"""
        model_map = {}
        for model in self.models:
            model_map[model._meta.table_name] = model
        return model_map

    def _determine_table_order(self):
        """Определяем порядок таблиц на основе зависимостей"""
        dependencies = {}

        for model in self.models:
            deps = []
            for field_name, field in model._meta.fields.items():
                if isinstance(field, ForeignKeyField):
                    # Получаем модель, на которую ссылается ForeignKey
                    rel_model = field.rel_model
                    deps.append(rel_model._meta.table_name)
            dependencies[model._meta.table_name] = deps

        # Топологическая сортировка
        visited = set()
        order = []

        def dfs(table):
            if table in visited:
                return
            visited.add(table)
            for dep in dependencies.get(table, []):
                if dep in dependencies:  # Проверяем, что зависимость есть в наших таблицах
                    dfs(dep)
            order.append(table)

        for table in dependencies.keys():
            dfs(table)

        return order

    def load_default_config(self):
        """Загрузка конфигурации по умолчанию"""
        return {
            'enabled': False,
            'frequency': 'daily',
            'time': '02:00',
            'local_retention_days': 7,
            'remote_targets': [],
            'backup_format': 'zip',
            'include_photos': True,
            'encryption_enabled': False,
            'encryption_password': '',
            'compression_level': 6,
            'verify_integrity': True,
            'test_restore_after_backup': False,
            'use_orm_only': True  # Флаг использования
        }

    def load_config(self):
        """Загрузка конфигурации из файла"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    self.backup_config.update(loaded_config)
                return True
        except Exception as e:
            print(f"Ошибка загрузки конфигурации: {e}")
        return False

    def save_config(self):
        """Сохранение конфигурации в файл"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.backup_config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Ошибка сохранения конфигурации: {e}")
        return False

    def create_backup(self, backup_format='zip', progress_callback=None) -> Optional[str]:
        """Создание резервной копии"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_dir = Path("data/backups")
            backup_dir.mkdir(parents=True, exist_ok=True)

            if progress_callback:
                progress_callback(5, "Начинаю создание резервной копии...")

            backup_file = None

            if backup_format == 'json':
                backup_file = backup_dir / f"backup_{timestamp}.json"
                self._create_json_backup(backup_file, progress_callback)

            elif backup_format == 'zip':
                backup_file = backup_dir / f"backup_{timestamp}.zip"
                self._create_zip_backup(backup_file, progress_callback)

            elif backup_format == 'orm':
                backup_file = backup_dir / f"backup_{timestamp}.orm"
                self._create_orm_backup(backup_file, progress_callback)

            elif backup_format == 'full':
                backup_file = backup_dir / f"backup_{timestamp}.full"
                self._create_full_backup(backup_file, progress_callback)

            else:
                print(f"Неизвестный формат: {backup_format}")
                return None

            # Проверка целостности
            if self.backup_config.get('verify_integrity', True):
                if progress_callback:
                    progress_callback(95, "Проверка целостности...")
                if not self.verify_backup_integrity(backup_file):
                    raise Exception("Проверка целостности не пройдена")

            if progress_callback:
                progress_callback(100, "Резервная копия создана успешно!")

            print(f"Резервная копия создана: {backup_file}")
            return str(backup_file)

        except Exception as e:
            print(f"Ошибка создания резервной копии: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _create_json_backup(self, backup_file, progress_callback=None):
        """Создание резервной копии в формате JSON"""
        try:
            all_data = {}
            total_tables = len(self.table_order)

            if progress_callback:
                progress_callback(10, "Получение схемы базы данных...")

            # Получаем схему
            all_data['schema'] = self._get_orm_schema()

            # Получаем данные в правильном порядке
            for i, table_name in enumerate(self.table_order):
                if progress_callback:
                    progress = 15 + (i * 70 / total_tables)
                    progress_callback(int(progress), f"Экспорт таблицы: {table_name}...")

                model = self.model_map.get(table_name)
                if model:
                    try:
                        # Получаем все записи
                        records = []
                        for record in model.select():
                            # Конвертируем в словарь
                            record_dict = self._model_to_dict(record)
                            records.append(record_dict)

                        all_data[table_name] = records
                    except Exception as e:
                        print(f"Ошибка загрузки таблицы {table_name}: {e}")
                        all_data[table_name] = []
                else:
                    all_data[table_name] = []
                    print(f"Модель для таблицы {table_name} не найдена")

            # Добавляем метаданные
            all_data['metadata'] = {
                'timestamp': datetime.now().isoformat(),
                'database': 'florarium',
                'version': '1.0',
                'backup_type': 'full',
                'created_by': 'BackupManager',
                'tables_order': self.table_order,
                'checksum': self._calculate_checksum(all_data),
                'record_counts': {table: len(all_data.get(table, []))
                                 for table in self.table_order},
                'orm_schema_hash': self._get_orm_schema_hash()
            }

            if progress_callback:
                progress_callback(90, "Сохранение JSON файла...")

            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, ensure_ascii=False, indent=2, default=self._json_serializer)

        except Exception as e:
            raise Exception(f"Ошибка создания JSON бэкапа: {e}")

    def _model_to_dict(self, model_instance):
        """Конвертация экземпляра модели в словарь"""
        data = {}
        for field_name, field in model_instance._meta.fields.items():
            value = getattr(model_instance, field_name)

            # Обрабатываем ForeignKey поля
            if isinstance(field, ForeignKeyField):
                if value is not None:
                    # Сохраняем только ID связанной записи
                    if hasattr(value, 'id'):
                        data[field_name] = value.id
                    else:
                        data[field_name] = value
                else:
                    data[field_name] = None
            else:
                # Обработка специальных типов данных
                data[field_name] = self._serialize_value(value)

        return data

    def _serialize_value(self, value):
        """Сериализация значения для JSON"""
        if value is None:
            return None
        elif hasattr(value, 'isoformat'):  # Дата/время
            return value.isoformat()
        elif isinstance(value, (int, float, str, bool)):
            return value
        elif isinstance(value, bytes):
            return value.hex()  # Конвертируем байты в hex строку
        else:
            return str(value)  # Fallback

    def _json_serializer(self, obj):
        """Кастомный сериализатор для JSON"""
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        elif isinstance(obj, bytes):
            return obj.hex()
        elif callable(obj):
            return None
        elif hasattr(obj, '__dict__'):
            # Попытка сериализовать объект через его __dict__
            try:
                return obj.__dict__
            except:
                return str(obj)
        raise TypeError(f"Type {type(obj)} not serializable")

    def _get_orm_schema(self):
        """Получение схемы базы данных"""
        schema = {}

        for model in self.models:
            table_name = model._meta.table_name
            table_info = {
                'model_name': model.__name__,
                'table_name': table_name,
                'fields': {},
                'indexes': model._meta.indexes if hasattr(model._meta, 'indexes') else [],
                'primary_key': model._meta.primary_key.name if model._meta.primary_key else None,
                'database': model._meta.database.database if model._meta.database else None
            }

            # Информация о полях
            for field_name, field in model._meta.fields.items():
                field_info = {
                    'field_type': field.field_type,
                    'null': field.null,
                    'unique': field.unique,
                    'index': field.index,
                    'default': field.default,
                    'primary_key': field.primary_key,
                }

                if isinstance(field, ForeignKeyField):
                    field_info['field_type'] = 'ForeignKey'
                    field_info['rel_model'] = field.rel_model.__name__
                    field_info['rel_table'] = field.rel_model._meta.table_name
                    field_info['on_delete'] = field.on_delete if hasattr(field, 'on_delete') else 'RESTRICT'
                    field_info['on_update'] = field.on_update if hasattr(field, 'on_update') else 'RESTRICT'

                table_info['fields'][field_name] = field_info

            schema[table_name] = table_info

        return schema

    def _get_orm_schema_hash(self):
        """Получение хеша схемы для проверки совместимости"""
        schema = self._get_orm_schema()
        schema_str = json.dumps(schema, sort_keys=True, default=str)
        return hashlib.md5(schema_str.encode('utf-8')).hexdigest()

    def _create_zip_backup(self, backup_file, progress_callback=None):
        """Создание ZIP архива"""
        try:
            if progress_callback:
                progress_callback(10, "Подготовка архива...")

            # Создаем временную директорию
            temp_dir = tempfile.mkdtemp()
            json_file = Path(temp_dir) / "database.json"

            # Создаем JSON бэкап
            self._create_json_backup(json_file,
                lambda p, msg: progress_callback(10 + p*0.4, msg) if progress_callback else None)

            # Создаем ZIP архив
            if progress_callback:
                progress_callback(50, "Создание ZIP архива...")

            with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Добавляем JSON файл
                zipf.write(json_file, 'database.json')

                # Добавляем схему
                schema_file = Path(temp_dir) / "orm_schema.json"
                with open(schema_file, 'w', encoding='utf-8') as f:
                    json.dump(self._get_orm_schema(), f, indent=2, default=str)
                zipf.write(schema_file, 'orm_schema.json')

                # Добавляем фотографии если включено
                if self.backup_config.get('include_photos', True):
                    if progress_callback:
                        progress_callback(60, "Добавление фотографий...")
                    self._add_photos_to_zip(zipf)

                # Добавляем файл проверки целостности
                checksum_file = Path(temp_dir) / "checksum.txt"
                self._create_checksum_file(checksum_file, [json_file, schema_file])
                zipf.write(checksum_file, 'checksum.txt')

            # Очистка временных файлов
            shutil.rmtree(temp_dir)

            if progress_callback:
                progress_callback(90, "Архив создан, проверка...")

            # Проверяем архив
            if not self._verify_zip_integrity(backup_file):
                raise Exception("Ошибка проверки целостности архива")

        except Exception as e:
            raise Exception(f"Ошибка создания ZIP архива: {e}")

    def _create_orm_backup(self, backup_file, progress_callback=None):
        """Создание бэкапа в бинарном формате с использованием pickle"""
        try:
            if progress_callback:
                progress_callback(20, "Подготовка ORM бэкапа...")

            backup_data = {
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'database': 'florarium',
                    'version': '1.0',
                    'orm_backup': True,
                    'schema_hash': self._get_orm_schema_hash()
                },
                'schema': self._get_orm_schema(),
                'data': {}
            }

            # Собираем данные
            total_tables = len(self.table_order)
            for i, table_name in enumerate(self.table_order):
                if progress_callback:
                    progress = 30 + (i * 50 / total_tables)
                    progress_callback(int(progress), f"Сбор данных: {table_name}...")

                model = self.model_map.get(table_name)
                if model:
                    table_data = []
                    for record in model.select():
                        table_data.append(self._model_to_dict(record))
                    backup_data['data'][table_name] = table_data

            if progress_callback:
                progress_callback(85, "Сериализация данных...")

            # Сериализуем через pickle
            with open(backup_file, 'wb') as f:
                pickle.dump(backup_data, f, protocol=pickle.HIGHEST_PROTOCOL)

            if progress_callback:
                progress_callback(95, "Готово!")

        except Exception as e:
            raise Exception(f"Ошибка создания ORM бэкапа: {e}")

    def _create_full_backup(self, backup_file, progress_callback=None):
        """Создание полной копии (экспорт в SQL)"""
        try:
            if progress_callback:
                progress_callback(20, "Создание полного бэкапа...")

            from peewee import Database
            db = self.models[0]._meta.database

            # Создаем SQL дамп через ORM
            sql_dump = []

            for model in self.models:
                # Получаем SQL создания таблицы
                create_sql = db.compiler().create_table(model)
                sql_dump.append(create_sql)

            total_tables = len(self.table_order)
            for i, table_name in enumerate(self.table_order):
                if progress_callback:
                    progress = 40 + (i * 40 / total_tables)
                    progress_callback(int(progress), f"Экспорт данных: {table_name}...")

                model = self.model_map.get(table_name)
                if model:
                    for record in model.select():
                        insert_sql = db.compiler().insert(record)
                        sql_dump.append(insert_sql)

            # Сохраняем в файл
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(sql_dump))

            if progress_callback:
                progress_callback(90, "Полный бэкап создан!")

        except Exception as e:
            raise Exception(f"Ошибка создания полного бэкапа: {e}")

    def _add_photos_to_zip(self, zipf):
        """Добавление фотографий в ZIP архив"""
        try:
            photo_fields = []
            for model in self.models:
                for field_name, field in model._meta.fields.items():
                    if 'photo' in field_name.lower() or 'image' in field_name.lower():
                        photo_fields.append((model, field_name))

            # Собираем пути к фотографиям
            photo_paths = set()

            for model, field_name in photo_fields:
                try:
                    for record in model.select():
                        photo_path = getattr(record, field_name, None)
                        if photo_path and isinstance(photo_path, str) and os.path.exists(photo_path):
                            photo_paths.add(photo_path)
                except Exception as e:
                    print(f"Ошибка при получении фото из {model.__name__}.{field_name}: {e}")

            # Добавляем фотографии в архив
            for i, photo_path in enumerate(photo_paths):
                try:
                    rel_path = os.path.relpath(photo_path)
                    zipf.write(photo_path, f"photos/{os.path.basename(photo_path)}")
                except Exception as e:
                    print(f"Ошибка добавления фото {photo_path}: {e}")

            # Также добавляем стандартные директории
            standard_dirs = ['data/photos', 'user_photos', 'photos']
            for dir_path in standard_dirs:
                if os.path.exists(dir_path):
                    for root, dirs, files in os.walk(dir_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            rel_path = os.path.relpath(file_path, dir_path)
                            zipf.write(file_path, f"{dir_path}/{rel_path}")

        except Exception as e:
            print(f"Ошибка добавления фотографий в архив: {e}")

    def _create_checksum_file(self, checksum_file, files):
        """Создание файла контрольных сумм"""
        try:
            with open(checksum_file, 'w', encoding='utf-8') as f:
                for file_path in files:
                    if os.path.exists(file_path):
                        checksum = self._calculate_file_checksum(file_path)
                        f.write(f"{os.path.basename(file_path)}: {checksum}\n")
        except Exception as e:
            print(f"Ошибка создания файла checksum: {e}")

    def _calculate_file_checksum(self, file_path):
        """Вычисление контрольной суммы файла"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def _calculate_checksum(self, data):
        """Вычисление контрольной суммы данных"""
        data_str = json.dumps(data, sort_keys=True, default=str)
        return hashlib.md5(data_str.encode('utf-8')).hexdigest()

    def _verify_zip_integrity(self, zip_file):
        """Проверка целостности ZIP архива"""
        try:
            with zipfile.ZipFile(zip_file, 'r') as zipf:
                return zipf.testzip() is None
        except:
            return False

    def verify_backup_integrity(self, backup_file):
        """Проверка целостности резервной копии через ORM"""
        try:
            backup_path = Path(backup_file)

            if backup_path.suffix == '.zip':
                if not self._verify_zip_integrity(backup_file):
                    return False

                with zipfile.ZipFile(backup_file, 'r') as zipf:
                    if 'database.json' not in zipf.namelist():
                        return False

                    # Проверяем схему ORM
                    json_data = zipf.read('database.json')
                    data = json.loads(json_data.decode('utf-8'))

                    # Проверяем хеш схемы
                    if 'metadata' in data and 'orm_schema_hash' in data['metadata']:
                        current_hash = self._get_orm_schema_hash()
                        backup_hash = data['metadata']['orm_schema_hash']
                        if current_hash != backup_hash:
                            print("Схема БД изменилась с момента создания бэкапа")
                            # Не прерываем, но предупреждаем

                    return True

            elif backup_path.suffix == '.json':
                with open(backup_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                required_keys = ['metadata', 'schema', 'data']
                for key in required_keys:
                    if key not in data:
                        return False

                # Проверяем контрольную сумму
                if 'checksum' in data['metadata']:
                    original_checksum = data['metadata'].pop('checksum')
                    current_checksum = self._calculate_checksum(data)
                    data['metadata']['checksum'] = original_checksum

                    if original_checksum != current_checksum:
                        return False

                return True

            elif backup_path.suffix == '.orm':
                try:
                    with open(backup_file, 'rb') as f:
                        data = pickle.load(f)

                    if 'metadata' not in data or 'schema' not in data or 'data' not in data:
                        return False

                    # Проверяем совместимость схемы
                    if 'schema_hash' in data['metadata']:
                        current_hash = self._get_orm_schema_hash()
                        backup_hash = data['metadata']['schema_hash']
                        if current_hash != backup_hash:
                            print("Схема БД изменилась с момента создания бэкапа")

                    return True

                except:
                    return False

            elif backup_path.suffix in ['.full', '.sql']:
                # Для SQL файлов просто проверяем существование
                return os.path.exists(backup_file) and os.path.getsize(backup_file) > 0

            return False

        except Exception as e:
            print(f"Ошибка проверки целостности: {e}")
            return False

    def restore_from_backup(self, backup_file, progress_callback=None):
        """Восстановление из резервной копии"""
        try:
            if not os.path.exists(backup_file):
                raise Exception(f"Файл не существует: {backup_file}")

            if progress_callback:
                progress_callback(5, "Начинаю восстановление...")

            # Проверяем целостность
            if not self.verify_backup_integrity(backup_file):
                raise Exception("Резервная копия повреждена или не прошла проверку целостности")

            # Создаем резервную копию текущей БД
            if progress_callback:
                progress_callback(10, "Создание резервной копии текущей БД...")

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            current_backup = Path(f"data/backups/pre_restore_{timestamp}.db")
            current_backup.parent.mkdir(parents=True, exist_ok=True)

            self.create_backup('json', lambda p, msg: None)

            try:
                # Восстанавливаем
                if progress_callback:
                    progress_callback(30, "Восстановление данных...")

                success = self._restore_from_backup_orm(backup_file, progress_callback)

                if success:
                    if progress_callback:
                        progress_callback(95, "Проверка восстановленных данных...")

                    # Проверяем восстановление
                    if self._verify_restored_data_orm():
                        if progress_callback:
                            progress_callback(100, "Восстановление успешно завершено!")
                        print("✓ Восстановление успешно завершено")
                        return True
                    else:
                        raise Exception("Проверка восстановленных данных не пройдена")
                else:
                    raise Exception("Ошибка восстановления данных")

            except Exception as e:
                if progress_callback:
                    progress_callback(50, "Ошибка! Восстанавливаю предыдущее состояние...")

                # Находим последний backup
                backups = self.list_backups()
                if backups and len(backups) > 1:
                    last_backup = backups[1]['file']  # Предпоследний (последний - текущий)
                    self._restore_from_backup_orm(last_backup, lambda p, msg: None)

                raise Exception(f"Ошибка восстановления: {e}. Возвращено предыдущее состояние.")

        except Exception as e:
            print(f"Ошибка восстановления: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _restore_from_backup_orm(self, backup_file, progress_callback=None):
        """Восстановление из бэкапа"""
        try:
            backup_path = Path(backup_file)
            data = None

            if backup_path.suffix == '.zip':
                with zipfile.ZipFile(backup_file, 'r') as zipf:
                    json_data = zipf.read('database.json')
                    data = json.loads(json_data.decode('utf-8'))

            elif backup_path.suffix == '.json':
                with open(backup_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

            elif backup_path.suffix == '.orm':
                with open(backup_file, 'rb') as f:
                    data = pickle.load(f)

            if not data:
                raise Exception("Не удалось загрузить данные из бэкапа")

            # Очищаем текущие данные (в правильном порядке - обратном)
            if progress_callback:
                progress_callback(40, "Очистка текущих данных...")

            reverse_order = list(reversed(self.table_order))
            total_tables = len(reverse_order)

            for i, table_name in enumerate(reverse_order):
                if progress_callback:
                    progress = 40 + (i * 10 / total_tables)
                    progress_callback(int(progress), f"Очистка таблицы: {table_name}...")

                model = self.model_map.get(table_name)
                if model:
                    # Удаляем все записи
                    model.delete().execute()

            # Восстанавливаем данные
            if progress_callback:
                progress_callback(60, "Восстановление записей...")

            tables_order = data.get('metadata', {}).get('tables_order', self.table_order)
            backup_data = data.get('data', data)  # Поддержка старого формата

            total_tables = len(tables_order)
            for i, table_name in enumerate(tables_order):
                if progress_callback:
                    progress = 60 + (i * 30 / total_tables)
                    progress_callback(int(progress), f"Восстановление таблицы: {table_name}...")

                model = self.model_map.get(table_name)
                if model and table_name in backup_data:
                    records = backup_data[table_name]

                    # Вставляем записи
                    for record_data in records:
                        # Подготавливаем данные для модели
                        prepared_data = {}
                        for field_name, value in record_data.items():
                            if value is not None:
                                field = model._meta.fields.get(field_name)
                                if isinstance(field, ForeignKeyField):
                                    rel_model = field.rel_model
                                    try:
                                        # Ищем существующую запись
                                        rel_instance = rel_model.get_by_id(value)
                                        prepared_data[field_name] = rel_instance
                                    except DoesNotExist:
                                        prepared_data[field_name] = value
                                else:
                                    prepared_data[field_name] = value

                        # Создаем запись
                        try:
                            model.create(**prepared_data)
                        except Exception as e:
                            print(f"Ошибка создания записи в {table_name}: {e}")
                            try:
                                if 'id' in prepared_data:
                                    model.update(**prepared_data).where(model.id == prepared_data['id']).execute()
                            except:
                                pass

            if progress_callback:
                progress_callback(95, "Финализация...")

            return True

        except Exception as e:
            print(f"✗ Ошибка восстановления через ORM: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _verify_restored_data_orm(self):
        """Проверка восстановленных данных"""
        try:
            for table_name in self.table_order:
                model = self.model_map.get(table_name)
                if not model:
                    print(f"✗ Модель для таблицы {table_name} не найдена")
                    return False

            # Проверяем что таблицы не пустые (кроме возможно пустых)
            non_empty_tables = ['users', 'plants']
            for table_name in non_empty_tables:
                model = self.model_map.get(table_name)
                if model:
                    count = model.select().count()
                    if count == 0:
                        print(f"✗ Таблица {table_name} пуста после восстановления")
                        return False

            # Проверяем целостность ForeignKey
            for model in self.models:
                for field_name, field in model._meta.fields.items():
                    if isinstance(field, ForeignKeyField):
                        rel_model = field.rel_model
                        try:
                            test_query = model.select().join(rel_model).limit(1)
                            list(test_query)
                        except Exception as e:
                            print(f"Проблема с ForeignKey {model.__name__}.{field_name}: {e}")

            return True

        except Exception as e:
            print(f"✗ Ошибка проверки восстановленных данных: {e}")
            return False

    def get_backup_info(self, backup_file):
        """Получение информации о резервной копии"""
        try:
            info = {
                'file': backup_file,
                'exists': os.path.exists(backup_file),
                'size': 0,
                'created': None,
                'tables': {},
                'integrity': False,
                'type': 'unknown',
                'orm_compatible': False
            }

            if not info['exists']:
                return info

            backup_path = Path(backup_file)
            info['size'] = os.path.getsize(backup_file)
            info['created'] = datetime.fromtimestamp(os.path.getctime(backup_file))

            # Определяем тип и читаем данные
            try:
                if backup_path.suffix == '.zip':
                    info['type'] = 'zip'
                    with zipfile.ZipFile(backup_file, 'r') as zipf:
                        if 'database.json' in zipf.namelist():
                            json_data = zipf.read('database.json')
                            data = json.loads(json_data.decode('utf-8'))
                            info['tables'] = data.get('metadata', {}).get('record_counts', {})
                            info['orm_compatible'] = 'orm_schema_hash' in data.get('metadata', {})

                elif backup_path.suffix == '.json':
                    info['type'] = 'json'
                    with open(backup_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        info['tables'] = data.get('metadata', {}).get('record_counts', {})
                        info['orm_compatible'] = 'orm_schema_hash' in data.get('metadata', {})

                elif backup_path.suffix == '.orm':
                    info['type'] = 'orm'
                    with open(backup_file, 'rb') as f:
                        data = pickle.load(f)
                        info['tables'] = {k: len(v) for k, v in data.get('data', {}).items()}
                        info['orm_compatible'] = True

                elif backup_path.suffix in ['.full', '.sql', '.backup', '.db']:
                    info['type'] = 'database'
                    info['orm_compatible'] = True  # Предполагаем совместимость

            except Exception as e:
                print(f"Ошибка чтения информации о бэкапе: {e}")

            # Проверяем целостность
            info['integrity'] = self.verify_backup_integrity(backup_file)

            return info

        except Exception as e:
            print(f"Ошибка получения информации: {e}")
            return None

    def compare_backups(self, backup1, backup2):
        """Сравнение двух резервных копий"""
        try:
            info1 = self.get_backup_info(backup1)
            info2 = self.get_backup_info(backup2)

            if not info1 or not info2:
                return None

            comparison = {
                'backup1': info1,
                'backup2': info2,
                'differences': {},
                'new_tables': [],
                'removed_tables': [],
                'record_changes': {},
                'schema_changed': False
            }

            # Проверяем изменение схемы
            if info1.get('orm_compatible') and info2.get('orm_compatible'):
                # Для ORM бэкапов можно сравнить схемы
                comparison['schema_changed'] = info1.get('orm_schema_hash') != info2.get('orm_schema_hash')

            # Сравниваем таблицы
            tables1 = set(info1.get('tables', {}).keys())
            tables2 = set(info2.get('tables', {}).keys())

            comparison['new_tables'] = list(tables2 - tables1)
            comparison['removed_tables'] = list(tables1 - tables2)

            # Сравниваем количество записей
            common_tables = tables1 & tables2
            for table in common_tables:
                count1 = info1['tables'].get(table, 0)
                count2 = info2['tables'].get(table, 0)
                if count1 != count2:
                    comparison['record_changes'][table] = {
                        'before': count1,
                        'after': count2,
                        'difference': count2 - count1
                    }

            return comparison

        except Exception as e:
            print(f"Ошибка сравнения резервных копий: {e}")
            return None

    def cleanup_old_backups(self, days_to_keep=7):
        """Очистка старых резервных копий"""
        try:
            backup_dir = Path("data/backups")
            if not backup_dir.exists():
                return 0

            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            deleted_count = 0

            for backup_file in backup_dir.glob("*.*"):
                if backup_file.is_file():
                    file_mtime = datetime.fromtimestamp(backup_file.stat().st_mtime)
                    if file_mtime < cutoff_date:
                        try:
                            backup_file.unlink()
                            deleted_count += 1
                        except Exception as e:
                            print(f"Не удалось удалить файл {backup_file}: {e}")

            if deleted_count > 0:
                print(f"Удалено {deleted_count} старых резервных копий")

            return deleted_count

        except Exception as e:
            print(f"Ошибка очистки старых резервных копий: {e}")
            return 0

    def list_backups(self):
        """Получение списка доступных резервных копий с информацией"""
        try:
            backup_dir = Path("data/backups")
            if not backup_dir.exists():
                return []

            backups = []
            for backup_file in backup_dir.glob("*.*"):
                if backup_file.is_file():
                    info = self.get_backup_info(str(backup_file))
                    if info:
                        # Добавляем имя файла для совместимости
                        info['name'] = backup_file.name
                        backups.append(info)

            # Сортируем по дате создания (новые сверху)
            backups.sort(key=lambda x: x['created'] if x['created'] else datetime.min, reverse=True)
            return backups

        except Exception as e:
            print(f"Ошибка получения списка резервных копий: {e}")
            return []


