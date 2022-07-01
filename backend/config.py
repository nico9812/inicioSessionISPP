class Config:
    SECRET_KEY = 'SAD34254GF45'
    DEBUG = True


class configuracionDesarrollo(Config):
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'isppf'
    MYSQL_PORT = 3308


config = {
    'desarrollo': configuracionDesarrollo
}
