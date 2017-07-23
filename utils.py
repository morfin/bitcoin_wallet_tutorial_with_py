import pybitcointools
import hashlib
import base58
from io import BytesIO
from pybitcoin import BitcoinPrivateKey


def wif_private_key(private_key_with_version):

    # Hash the private_key_with_version value using the cryptographic hash function SHA256.
    # This Secure Hash Algorithm generates a 256-bit (32-byte) signature which cannot be decrypted back
    # to the original value (it is a one-way cryptographic function).
    # The hash_a1 value is always 32 bytes or 64 characters long.
    hash_a1 = pybitcointools.sha256(private_key_with_version.decode('hex'))

    # Hash the hash_a1 value using the same cryptographic hash function SHA256.
    # The hash_a2 value is always 32 bytes or 64 characters long.
    hash_a2 = pybitcointools.sha256(hash_a1.decode('hex'))

    # Get the first 4 bytes (or first 8 characters) of the hash_a2 value.
    # These 4 bytes is the checksum value which will be used to validate the address.
    # The checksum_a value is always 4 bytes or 8 characters long.
    checksum_a = BytesIO(hash_a2.decode('hex')).read(4).encode('hex')

    # Append the checksum_a value at the end of the private_key_with_version value.
    # The private_key_checksum value is always (33+4=) 37 bytes or 74 characters long.
    private_key_checksum = private_key_with_version + checksum_a

    # The Private Key Wallet Import Format (WIF) for uncompressed public key is the private_key_checksum
    # value encoded into a Base58 value. The private_key_wif_uncompressed value must be kept secret and
    # can be converted into QR codes and can be printed on paper wallets.
    #
    # If your software uses the private_key_wif_uncompressed value, it also means you are the using the
    # and uncompressed Public Key.
    #
    # It is recommended to always to use the compressed public key (public_address_compressed) and the compressed
    # private key (private_key_wif_for_compressed). If your software does not support the compressed keys you can use
    # the uncompressed public key (public_address_uncompressed) and the
    # corresponding WIF (private_key_wif_for_uncompressed).
    return base58.b58encode(private_key_checksum.decode('hex'))


def public_address(public_key_version):

    # Hash the public_key_version value using the cryptographic hash function SHA256.
    # This Secure Hash Algorithm generates a 256-bit (32-byte) signature which cannot be decrypted back
    # to the original value (it is a one-way cryptographic function).
    # The hash_c1 value is always 32 bytes or 64 characters long.
    hash_c1 = pybitcointools.sha256(public_key_version.decode('hex'))

    # Hash the hash_c1 value using the cryptographic hash function RIPEMD160.
    # The RIPEMD160 (RACE Integrity Primitives Evaluation Message Digest) generates a 160-bit (20-byte) signature
    # which cannot be decrypted back to the original value (it is a one-way cryptographic function).
    # The hash_c2 value is always 20 bytes or 40 characters long.
    hash_c2 = hashlib.new('ripemd160', hash_c1.decode('hex')).hexdigest()

    # Each cryptocurrency Public Key has their own prefix version number (Bitcoin= 0x00, Litecoin=0x30, etc).
    # Prepend this version number in front of the hash_c2 value.
    # The prefix version number is always 1 byte in size and the hash_c2 is 20 bytes.
    # The public_key_version_hash_c value is always (1+20=) 21 bytes or 42 characters long.
    public_key_version_hash_c = '00' + hash_c2

    # Hash the public_key_version_hash_c value using the cryptographic hash function SHA256.
    # This Secure Hash Algorithm generates a 256-bit (32-byte) signature which cannot be decrypted back
    # to the original value (it is a one-way cryptographic function).
    # The hash_c3 value is always 32 bytes or 64 characters long.
    hash_c3 = pybitcointools.sha256(public_key_version_hash_c.decode('hex'))

    # Hash the hash_c3 value using the cryptographic hash function SHA256.
    # This Secure Hash Algorithm generates a 256-bit (32-byte) signature which cannot be decrypted back
    # to the original value (it is a one-way cryptographic function).
    # The hash_c4 value is always 32 bytes or 64 characters long.
    hash_c4 = pybitcointools.sha256(hash_c3.decode('hex'))

    # Get the first 4 bytes (or first 8 characters) of the hash_c4 value.
    # These 4 bytes is the checksum value which will be used to validate the address.
    # The checksum_c value is always 4 bytes or 8 characters long.
    checksum_c = BytesIO(hash_c4.decode('hex')).read(4).encode('hex')

    # Append the checksum_c value at the end of the public_key_version_hash_c value.
    # The public_key_checksum_c value is always (21+4=) 25 bytes or 50 characters long.
    public_key_checksum_c = public_key_version_hash_c + checksum_c

    # The Public Address uncompressed is the public_key_checksum_c value encoded into a
    # Base58 value. The generated value can be made public and can be converted into QR codes
    # for sharing it easily via wallet apps.
    #
    # It is recommended to always to use a compressed Public Key/Public Address and the corresponding
    # WIF. If your software does not support the compressed format you can still use
    # the uncompressed keypair, although not recommended.
    return base58.b58encode(public_key_checksum_c.decode('hex'))


def validate_public_against_py_bitcoin(private_key_hex, public_address_uncompressed, compressed=True):
    private_key_pybitcoin = BitcoinPrivateKey(private_key_hex, compressed)
    if private_key_pybitcoin.public_key().address() == public_address_uncompressed:
        return True
