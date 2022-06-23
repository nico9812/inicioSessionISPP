
class Config:
    SECRET_KEY = 'SAD34254GF45'

class configuracionDesarrollo(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'isppf'
    MYSQL_PORT = 3310

config = {
    'desarrollo' : configuracionDesarrollo
}