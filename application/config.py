from Crypto.Random import get_random_bytes

class Config:
    key = get_random_bytes( 16 )
    SECRET_KEY = key.hex()
    