class DevelopmentConfig:
    DEBUG=True
    MYSQL_HOST='localhost'
    MYSQL_USER='Gael'
    MYSQL_PASSWORD='mega117HOLA'
    MYSQL_DB='api_utl'
    MYSQL_CURSORCLASS='Cursor'

config = {
    'development': DevelopmentConfig,
}