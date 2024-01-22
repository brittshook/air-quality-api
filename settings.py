import os

config = {
    'database_url': os.environ.get('DB_URL'),
    'brevo_api_key': os.environ.get('BREVO_API_KEY'),
    'admin_api_key': os.environ.get('ADMIN_API_KEY'),
}