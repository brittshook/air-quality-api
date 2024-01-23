import os

config = {
    'database_url': os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql+psycopg2://', 1),
    'brevo_api_key': os.environ.get('BREVO_API_KEY'),
    'admin_api_key': os.environ.get('ADMIN_API_KEY'),
}