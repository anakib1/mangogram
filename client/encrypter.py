from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64


def int_to_fixed_length_hex(value, length=32):
    # Convert the integer to a hexadecimal string (without the '0x' prefix)
    hex_string = hex(value)[2:]
    # Ensure the hexadecimal string is exactly the desired length
    if len(hex_string) > length:
        # Truncate if necessary
        hex_string = hex_string[:length]
    else:
        # Pad with leading zeros if necessary
        hex_string = hex_string.zfill(length)
    return hex_string


class AESCipher:
    def __init__(self, key):
        self.key = int_to_fixed_length_hex(key).encode('UTF-8')
        self.block_size = AES.block_size

    def encrypt(self, plaintext):
        plaintext_bytes = plaintext.encode('utf-8')
        padded_plaintext = pad(plaintext_bytes, self.block_size)
        iv = get_random_bytes(self.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        ciphertext_bytes = cipher.encrypt(padded_plaintext)
        iv_and_ciphertext = iv + ciphertext_bytes
        iv_and_ciphertext_b64 = base64.b64encode(iv_and_ciphertext).decode('utf-8')
        return iv_and_ciphertext_b64

    def decrypt(self, iv_and_ciphertext_b64):
        iv_and_ciphertext = base64.b64decode(iv_and_ciphertext_b64)
        iv = iv_and_ciphertext[:self.block_size]
        ciphertext = iv_and_ciphertext[self.block_size:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        padded_plaintext = cipher.decrypt(ciphertext)
        plaintext_bytes = unpad(padded_plaintext, self.block_size)
        plaintext = plaintext_bytes.decode('utf-8')
        return plaintext


if __name__ == '__main__':
    key = '12345678'
    cipher = AESCipher(key)

    encrypted = cipher.encrypt('temp message')
    print('Encrypted:', encrypted)

    decrypted = cipher.decrypt(encrypted)
    print('Decrypted:', decrypted)
