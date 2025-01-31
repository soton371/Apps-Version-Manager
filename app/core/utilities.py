import random
import string
from passlib.context import CryptContext
import smtplib
from app.core.config import settings
from email.message import EmailMessage
import boto3
import os
from fastapi import UploadFile
from datetime import datetime
import pytz


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def logger(obj):
    if settings.env_mood == "local":
        print(obj)

def hashedPassword(password: str) -> str:
    return pwd_context.hash(password)

def verify(plainPassword: str, hashedPassword: str) -> bool:
    return pwd_context.verify(plainPassword, hashedPassword)


def sendPasswordSmtp(recipientMail: str):
    try:
        password = ''.join(random.choices(string.digits, k=4))
        smtpServer = smtplib.SMTP(settings.smtp_host, settings.smtp_port)
        smtpServer.starttls()
        smtpServer.login(settings.sender_email,settings.send_otp_password)

        msg = EmailMessage()
        msg['Subject'] = 'One Time Password For Apps Version Manager'
        msg['from'] = settings.sender_email
        msg['to'] = recipientMail
        msg.set_content(f"Your one time password is: {password}")
        smtpServer.send_message(msg)
        return password
    except Exception as e:
        print(f"sendPasswordSmtp e: {e}")
        return None
    
def booleanValue(string_value: str | None) -> bool:
    try:
        boolean_mapping = {'true': True, 'false': False}
        boolean_value = boolean_mapping.get(string_value.lower(), None) 
        return boolean_value
    except Exception as error:
        print(f'booleanValue error: {error}')
        return None
    



# AWS S3 Configuration
AWS_S3_BUCKET = settings.aws_s3_bucket
AWS_ACCESS_KEY = settings.aws_access_key
AWS_SECRET_KEY = settings.aws_secret_key

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
)

def uploadToS3(file: UploadFile, folder: str) -> str|None:
    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_number = os.urandom(4).hex()
        extension = os.path.splitext(file.filename)[1]
        file_url = f"{timestamp}-{random_number}{extension}"
        s3_key = f"apps_version_manager/{folder}/{file_url}"

        file_content = file.file.read()


        s3_client.put_object(
            Bucket=AWS_S3_BUCKET,
            Key=s3_key,
            Body=file_content,
            ACL="public-read",
            ContentType=file.content_type,
        )

        # file_url = f"https://{AWS_S3_BUCKET}.s3.amazonaws.com/{s3_key}"
        return file_url

    except Exception as e:
        logger(f"Error uploading to S3: {e}")
        return None
    
    


my_timezone = pytz.timezone('Asia/Dhaka')

