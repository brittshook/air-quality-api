import os

config = {
    'db_url': os.environ.get('DATABASE_URL'),
    'brevo_api_key': os.environ.get('BREVO_API_KEY'),
    'admin_api_key': os.environ.get('ADMIN_API_KEY'),
}