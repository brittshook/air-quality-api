import os

config = {
    'database_url': os.environ.get('DATABASE_URL?sslmode=require').replace('postgres://', 'postgresql://'),
    'brevo_api_key': os.environ.get('BREVO_API_KEY'),
    'admin_api_key': os.environ.get('ADMIN_API_KEY'),
}