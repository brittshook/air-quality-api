from dotenv import load_dotenv
import os

load_dotenv()

config = {
    'db_host': os.getenv('DB_HOST'),
    'db_database': os.getenv('DB_DATABASE'),
    'db_user': os.getenv('DB_USER'),
    'db_password': os.getenv('DB_PASSWORD'),
    'db_port': os.getenv('DB_PORT'),
    'brevo_api_key': os.getenv('BREVO_API_KEY'),
    'admin_api_key': os.getenv('ADMIN_API_KEY'),
}