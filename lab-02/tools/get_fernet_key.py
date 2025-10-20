from cryptography.fernet import Fernet
from configs import ENCRYPTION_KEY

# Only do this once and save it securely
if __name__ == "__main__":
    if not ENCRYPTION_KEY:
        key = Fernet.generate_key()
        print(key)
    else:
        print("You already had an encryption key.")
