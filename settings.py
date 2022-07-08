from email.policy import default
from decouple import config

class Config:
    auth_key = config("auth_token", default = None)

