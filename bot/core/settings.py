import os

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


TOKEN = os.getenv('TELEGRAM_TOKEN')
BACKEND_URL = os.getenv('BACKEND_URL')
DEBUG = os.getenv('DEBUG', 'false').lower() in ('true',)
CELERY_BROKER = os.getenv('CELERY_BROKER')
API_TOKEN = os.getenv('API_TOKEN')
# Максимальное время для проверки оплаты (секунды)
MAX_CHECK_PAYMENT_TIME = int(os.getenv('MAX_CHECK_PAYMENT_TIME', 1800))
# Интервал проверки оплаты (секунды)
INTERVAL_CHECK_PAYMENT = int(os.getenv('INTERVAL_CHECK_PAYMENT', 30))
# Максимальный срок оплаты
ORDER_MAX_LIFE_TIME = int(os.getenv('EXPIRATION_DATE', 1200))
