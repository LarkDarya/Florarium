import threading
import time
from datetime import datetime, timedelta
import schedule
import logging

class BackupScheduler:
    """Планировщик автоматического резервного копирования"""

    def __init__(self, backup_manager):
        self.backup_manager = backup_manager
        self.running = False
        self.scheduler_thread = None
        self.logger = logging.getLogger(__name__)

    def start(self):
        """Запуск планировщика"""
        if self.running:
            return

        self.running = True
        self.scheduler_thread = threading.Thread(target=self._run_scheduler)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()

        self.logger.info("Планировщик резервного копирования запущен")

        # Немедленно запускаем если включено
        if self.backup_manager.backup_config.get('enabled', False):
            self._check_and_run_backup()

    def stop(self):
        """Остановка планировщика"""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)

        self.logger.info("Планировщик резервного копирования остановлен")

    def _run_scheduler(self):
        """Основной цикл планировщика"""
        while self.running:
            try:
                self._check_and_run_backup()
                time.sleep(60)  # Проверяем каждую минуту
            except Exception as e:
                self.logger.error(f"Ошибка в планировщике: {e}")
                time.sleep(300)  # Ждем 5 минут при ошибке

    def _check_and_run_backup(self):
        """Проверка и запуск резервного копирования"""
        try:
            config = self.backup_manager.backup_config

            if not config.get('enabled', False):
                return

            now = datetime.now()

            # Проверяем время
            scheduled_time = config.get('time', '02:00')
            frequency = config.get('frequency', 'daily')

            # Парсим время
            hour, minute = map(int, scheduled_time.split(':'))

            should_run = False

            if frequency == 'daily':
                # Ежедневно
                should_run = (now.hour == hour and now.minute == minute)

            elif frequency == 'weekly' and now.weekday() == 0:  # Понедельник
                # Еженедельно по понедельникам
                should_run = (now.hour == hour and now.minute == minute)

            elif frequency == 'monthly' and now.day == 1:
                # Ежемесячно 1-го числа
                should_run = (now.hour == hour and now.minute == minute)

            if should_run:
                self.logger.info(f"Запуск автоматического резервного копирования: {now}")
                self._run_backup_task()

        except Exception as e:
            self.logger.error(f"Ошибка проверки расписания: {e}")

    def _run_backup_task(self):
        """Задача резервного копирования"""
        try:
            # Создаем резервную копию
            backup_format = self.backup_manager.backup_config.get('backup_format', 'zip')
            backup_file = self.backup_manager.create_backup(backup_format)

            if backup_file:
                # Копируем в удаленные цели
                remote_targets = self.backup_manager.backup_config.get('remote_targets', [])
                for target in remote_targets:
                    try:
                        self.backup_manager.backup_to_network(backup_file, target)
                    except Exception as e:
                        self.logger.error(f"Ошибка копирования в {target.get('name')}: {e}")

                self.logger.info(f"Автоматическое резервное копирование завершено: {backup_file}")
            else:
                self.logger.error("Не удалось создать резервную копию")

        except Exception as e:
            self.logger.error(f"Ошибка автоматического резервного копирования: {e}")
