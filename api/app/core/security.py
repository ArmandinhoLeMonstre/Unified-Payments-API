from cryptography.fernet import Fernet
from app.core.settings import settings

def try_encryption_key():
    key = settings.encryption_key
    try:
        f = Fernet(key)
    except ValueError as e:
        print(f"{e}")
        raise 

    return(0)