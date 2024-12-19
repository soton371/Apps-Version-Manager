from datetime import datetime, timedelta
from random import random
import string
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashedPassword(password: str) -> str:
    return pwd_context.hash(password)

def verify(plainPassword: str, hashedPassword: str) -> bool:
    return pwd_context.verify(plainPassword, hashedPassword)


def generate_otp(length: int = 6) -> str:
    return ''.join(random.choices(string.digits, k=length))

def otp_expiry_time(minutes: int = 3) -> datetime:
    return datetime.utcnow() + timedelta(minutes=minutes)
