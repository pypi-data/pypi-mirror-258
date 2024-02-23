import hashlib
import os
from datetime import datetime

class Licenses:
    def __init__(self, path_folder):
        self.path_folder = path_folder
        if not os.path.exists(self.path_folder):
            os.makedirs(self.path_folder)


    def convert_sha256(self, texto):
        sha256 = hashlib.sha256()
        sha256.update(texto.encode('utf-8'))
        hash_resultado = sha256.hexdigest()
        return hash_resultado

    def create_license(self, license_key:str, expiration_date:str) -> None:
        license_hash = self.convert_sha256(license_key)
        with open(f'{self.path_folder}/{license_hash}.lic', 'w') as file:
            file.write(expiration_date)
            file.close()

    def check_license(self, license_key:str) -> bool:
        license_hash = self.convert_sha256(license_key)
        if os.path.exists(f'{self.path_folder}/{license_hash}.lic'):
            with open(f'{self.path_folder}/{license_hash}.lic', 'r') as file:
                expiration_date = file.read()
                expiration_date = datetime.strptime(expiration_date, '%Y-%m-%d')
                if expiration_date > datetime.now():
                    return True
        return False
    
    def delete_license(self, license_key:str) -> None:
        license_hash = self.convert_sha256(license_key)
        if os.path.exists(f'{self.path_folder}/{license_hash}.lic'):
            os.remove(f'{self.path_folder}/{license_hash}.lic')