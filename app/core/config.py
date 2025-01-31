
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    env_mood: str
    database_hostname: str 
    database_port: str 
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    sender_email: str 
    send_otp_password: str
    smtp_host: str 
    smtp_port: int 
    aws_s3_bucket: str
    aws_access_key: str
    aws_secret_key: str

    class Config:
        env_file = ".env"



settings = Settings()
