"""
Cryptography Utilities for RPattern
Creator: Rahul Chaube 🚀
"""

import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


class RPatternCrypto:
    """Handles encryption and decryption for RPattern data."""
    
    def __init__(self, key: str = "RPattern_Rahul_2025"):
        """Initialize with a default key (in production, use secure key management)."""
        # Generate a 256-bit key from the provided string
        self.key = hashlib.sha256(key.encode()).digest()
        
    def encrypt(self, data: str) -> bytes:
        """
        Encrypt string data using AES encryption.
        
        Args:
            data: String data to encrypt
            
        Returns:
            Encrypted bytes including IV
        """
        # Convert string to bytes
        data_bytes = data.encode('utf-8')
        
        # Generate random IV
        iv = get_random_bytes(16)
        
        # Create cipher
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        
        # Pad data to be multiple of 16 bytes
        padded_data = pad(data_bytes, AES.block_size)
        
        # Encrypt
        encrypted_data = cipher.encrypt(padded_data)
        
        # Combine IV + encrypted data
        return iv + encrypted_data
    
    def decrypt(self, encrypted_data: bytes) -> str:
        """
        Decrypt encrypted bytes back to string.
        
        Args:
            encrypted_data: Encrypted bytes including IV
            
        Returns:
            Decrypted string data
        """
        # Extract IV (first 16 bytes)
        iv = encrypted_data[:16]
        
        # Extract encrypted data
        cipher_data = encrypted_data[16:]
        
        # Create cipher
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        
        # Decrypt
        decrypted_padded = cipher.decrypt(cipher_data)
        
        # Remove padding
        decrypted_data = unpad(decrypted_padded, AES.block_size)
        
        # Convert back to string
        return decrypted_data.decode('utf-8')


# Global crypto instance
_crypto = RPatternCrypto()


def encrypt_data(data: str) -> bytes:
    """Encrypt string data using AES encryption."""
    return _crypto.encrypt(data)


def decrypt_data(encrypted_data: bytes) -> str:
    """Decrypt encrypted bytes back to string."""
    return _crypto.decrypt(encrypted_data)


def encode_base64(data: str) -> str:
    """Encode string data to base64 (simple encoding, not encryption)."""
    return base64.b64encode(data.encode('utf-8')).decode('utf-8')


def decode_base64(encoded_data: str) -> str:
    """Decode base64 encoded string."""
    return base64.b64decode(encoded_data.encode('utf-8')).decode('utf-8')


def generate_hash(data: str) -> str:
    """Generate SHA-256 hash of the data for integrity checking."""
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


if __name__ == "__main__":
    # Test encryption/decryption
    test_data = "Hello RPattern by Rahul Chaube!"
    
    print("🔐 Crypto Utils Test")
    print(f"Original: {test_data}")
    
    # Test AES encryption
    encrypted = encrypt_data(test_data)
    print(f"Encrypted (bytes): {len(encrypted)} bytes")
    
    decrypted = decrypt_data(encrypted)
    print(f"Decrypted: {decrypted}")
    
    # Test base64 encoding
    encoded = encode_base64(test_data)
    print(f"Base64 encoded: {encoded}")
    
    decoded = decode_base64(encoded)
    print(f"Base64 decoded: {decoded}")
    
    # Test hash
    hash_value = generate_hash(test_data)
    print(f"SHA-256 hash: {hash_value}")
    
    if decrypted == test_data and decoded == test_data:
        print("✅ Crypto tests passed!")
    else:
        print("❌ Crypto tests failed!")
