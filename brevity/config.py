import os

# If the .env file is in the root folder then Flask by default calls load_dotenv()

# If we call load_dotenv() then flask searches for .env file in current directory
# from dotenv import load_dotenv
# load_dotenv()

# basedir = os.path.abspath(os.path.dirname(__file__))
# load_dotenv(os.path.join(basedir, ".env"))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')                   #secrets.token_hex(16)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False                 #supresses warning
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')