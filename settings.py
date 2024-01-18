from dotenv import load_dotenv
import os

load_dotenv()

config = {
    'db_host': os.getenv('DB_HOST'),
    'db_database': os.getenv('DB_DATABASE'),
    'db_user': os.getenv('DB_USER'),
    'db_password': os.getenv('DB_PASSWORD'),
    'db_port': os.getenv('DB_PORT'),
    'smtp_email': os.getenv('SMTP_EMAIL'),
    'smtp_password': os.getenv('SMTP_PASSWORD'),
    'smtp_server': os.getenv('SMTP_SERVER'),
    'smtp_port': os.getenv('SMTP_PORT')
}