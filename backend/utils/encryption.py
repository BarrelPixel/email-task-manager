import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class TokenEncryption:
    """Utility class for encrypting/decrypting sensitive tokens"""
    
    def __init__(self):
        self.key = self._get_encryption_key()
        self.cipher = Fernet(self.key)
    
    def _get_encryption_key(self) -> bytes:
        """Generate or retrieve encryption key from environment"""
        # Use a separate encryption key or derive from secret key
        secret_key = os.getenv('SECRET_KEY', 'dev-secret-key').encode()
        salt = os.getenv('ENCRYPTION_SALT', 'email-task-manager-salt').encode()
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(secret_key))
        return key
    
    def encrypt_token(self, token: str) -> str:
        """Encrypt a token string"""
        if not token:
            return None
        return self.cipher.encrypt(token.encode()).decode()
    
    def decrypt_token(self, encrypted_token: str) -> str:
        """Decrypt a token string"""
        if not encrypted_token:
            return None
        try:
            return self.cipher.decrypt(encrypted_token.encode()).decode()
        except Exception:
            return None  # Return None if decryption fails

# Global instance
token_encryption = TokenEncryption()