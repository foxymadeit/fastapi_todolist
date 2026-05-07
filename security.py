from authx import AuthX, AuthXConfig
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
load_dotenv()

ACCES_TOKEN_NAME = os.getenv("JWT_ACCESS_TOKEN")
SECRET_KEY = os.getenv("SECRET_KEY")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")




config = AuthXConfig()
config.JWT_SECRET_KEY = SECRET_KEY
config.JWT_ACCESS_COOKIE_NAME = ACCES_TOKEN_NAME
config.JWT_TOKEN_LOCATION = ['headers']
security = AuthX(config=config)