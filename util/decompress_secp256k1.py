import json
import rlp
from base64 import b64decode
import binascii


def enr_decode():
    with open('sample_all.json', 'r') as f:
        data = json.load(f)
        for item in data:
            enr_record = data[item]['record']
            enr_record = b64decode(enr_record[4:])  # returns bytes
            print(enr_record)
            rlp_decoded = rlp.decode(bytes(enr_record))
            print(rlp_decoded)
            exit(0)


def decompress_secp256k1_public_key():
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F

    def decompress_pubkey(pk):
        x = int.from_bytes(pk[1:33], byteorder='big')
        y_sq = (pow(x, 3, p) + 7) % p
        y = pow(y_sq, (p + 1) // 4, p)
        if y % 2 != pk[0] % 2:
            y = p - y
        y = y.to_bytes(32, byteorder='big')
        return b'\x04' + pk[1:33] + y

    print(binascii.hexlify(decompress_pubkey(
        binascii.unhexlify('027ec43359d10fbc307281d36c7f948de85c09eb7bf2958ca28fa17d2bd316072b'))).decode())


decompress_secp256k1_public_key()

