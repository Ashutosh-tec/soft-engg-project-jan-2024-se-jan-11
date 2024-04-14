import os
basedir = os.path.abspath(os.path.dirname(__file__))
# from application.env_keys import mg_api_key, alg_api_key
from dotenv import load_dotenv
load_dotenv()

class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SECRET_KEY= "ash ah secet"
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
    DISCOURSE_API_USERNAME = os.getenv("DISCOURSE_API_USERNAME")
    DISCOURSE_API_KEY = os.getenv("DISCOURSE_API_KEY")

class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "testdb.sqlite3")
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    SECRET_KEY =  "ash ah secet"
    SECURITY_PASSWORD_HASH = "bcrypt"    
    SECURITY_PASSWORD_SALT = "really super secret" # Read from ENV in your case
    SECURITY_REGISTERABLE = True
    SECURITY_CONFIRMABLE = False
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = None
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
    WTF_CSRF_ENABLED = False
    WTF_CSRF_CHECK_DEFAULT = False
    # Check csrf for session and http auth (but not token)
    SECURITY_CSRF_PROTECT_MECHANISMS = ["session", "basic"]
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    try:
        MAILGUN_API_KEY = os.environ.get('MG_API_KEY')
        SEARCH_API_KEY = os.environ.get('SEARCH_API_KEY')
    except: 
        MAILGUN_API_KEY = 'ABCD'
        SEARCH_API_KEY = 'ABCD'
    

class CeleryTesting(LocalDevelopmentConfig):
    SQLITE_DB_DIR = os.path.join(basedir, "../test/db_instances")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "testingdb.sqlite3")