from decouple import Config

config = Config()
config.read(".env")

host = config.get('HOST')
database = config.get('DATABASE')
user = config.get('USER')
password = config.get('PASSWORD')
port = config.get('PORT')