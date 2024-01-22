import os

config = {
    'db_host': os.environ.get('DB_HOST'),
    'db_database': os.environ.get('DB_DATABASE'),
    'db_user': os.environ.get('DB_USER'),
    'db_password': os.environ.get('DB_PASSWORD'),
    'db_port': os.environ.get('DB_PORT'),
    'brevo_api_key': os.environ.get('BREVO_API_KEY'),
    'admin_api_key': os.environ.get('ADMIN_API_KEY'),
}