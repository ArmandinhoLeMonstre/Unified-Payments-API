def encrypt_data(to_encrypt, fernet):
    data_in_bytes = to_encrypt.encode("utf-8")
    token = fernet.encrypt(data_in_bytes)

    return(token)

def decrypt_data(to_decrypt, fernet):
    key_in_bytes = fernet.decrypt(to_decrypt)
    key_in_str = key_in_bytes.decode("utf-8")

    return(key_in_str)