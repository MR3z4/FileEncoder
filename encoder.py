import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
import io
import os

class AESCipher(object):

    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode("ISO-8859-1")))

    def encrypt_file(self, file_path, save_file=False):
        raw = io.FileIO(file_path).read().decode("ISO-8859-1")
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        if save_file:
            with open(os.path.splitext(file_path)[0]+'.enc', 'wb') as f:
                f.write(base64.b64encode(iv + cipher.encrypt(raw.encode("ISO-8859-1"))))
            return None
        return base64.b64encode(iv + cipher.encrypt(raw.encode("ISO-8859-1")))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode("ISO-8859-1")

    def decrypt_file(self, file_path):
        with open(file_path, 'rb') as f:
            enc = f.read()
            enc = base64.b64decode(enc)
            iv = enc[:AES.block_size]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return self._unpad(cipher.decrypt(enc[AES.block_size:]))

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]