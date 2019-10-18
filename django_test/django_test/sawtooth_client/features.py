import secp256k1



def gen_random_key_str():
    key_handler = secp256k1.PrivateKey()
    private_key_str = key_handler.private_key.hex()
    return private_key_str



if __name__ == '__main__':
    print(gen_random_key_str())
