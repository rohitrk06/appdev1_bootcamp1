class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'secret_key'

# class Config:
#     DEBUG = True
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///data.sqlite3'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False