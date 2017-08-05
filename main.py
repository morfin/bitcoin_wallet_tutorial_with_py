import pybitcointools
import utils


# EVERYTHING STARTS HERE: THE PRIVATE KEY AND DERIVED WIFs
#
# A private key is just a 256-bit (32 bytes) random number, usually represented as hexadecimal value,
# that is, as a 64 hexadecimal characters long.
#
# A valid Private Key must be in the interval [1, n - 1], where:
# n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
# In plain english that would be a number
# from 1 to 115792089237316195423570985008687907852837564279074904382605163141518161494336
#
# This huge number is used to create the Private Key Wallet Import Format (WIF).
# Think of the WIF as the private key with metadata (this metadata indicates if WIF is a bitcoin wallet
# and if it's linked with a compressed or uncompressed public key. It also includes a checksum).
#
# This WIF format allows portability, allowing wallet apps to know how deal with it.
#
# REMEMBER that the private key is not compressed or uncompressed, it's just a big number encoded
# with hex. The compression can only applied to the public key. Good explanation here:
# https://www.reddit.com/r/Bitcoin/comments/2u0tin/why_are_private_keys_called_compressed_if_theyre/
#
# We are now generating a random private key with pybitcointools library.
# IMPORTANT: I CANNOT GUARANTEE THAT THE FOLLOWING GENERATED RANDOM KEY IS SECURE. I CAN ASSUME THOUGH.
#
# PLEASE USE IT ONLY FOR THIS DEMO. FOR YOUR REAL LIFE BITCOIN WALLETS, USE A PROPER
# OFFLINE WALLET APP.
#
private_key_hex = pybitcointools.random_key()

# Each cryptocurrency Private Key has their own prefix version number (Bitcoin= 0x80, Litecoin=0xB0, etc).
# Prepend this version number in front of the private_key_hex value.
# The prefix version number is always 1 byte in size and the private_key_hex is 32 bytes.
# The private_key_with_version value is always (1+32=) 33 bytes or 66 characters long.
private_key_with_version = '80' + private_key_hex

# WIF ADDRESS FOR UNCOMPRESSED PUBLIC KEY
#
# The Private Key Wallet Import Format (WIF) is just the Private Key
# with metadata and encoded with Base58 (check generate_addresses.wif_private_key
# function for details).
#
# Sometimes The WIF key is referred as "compressed or uncompressed WIF". This is confusing because
# the actual private key or derived WIF is never compressed. When people mention "compressed or uncompressed WIF"
# they're just referring to a WIF that corresponds to a compressed or uncompressed
# ECDSA public key/Bitcoin public address.
#
# The private_key_wif_for_uncompressed value must be kept secret. It can be converted into QR codes
# for paper wallets. The WIF private key (compressed or uncompressed) is the format used by wallet apps.
# old versions of wallet apps don't support compressed wif.
# This WIF type starts with  a "5".
#
# The WIF
private_key_wif_for_uncompressed = utils.wif_private_key(private_key_with_version)

# COMPRESSED WIF ADDRESS
# Append the value 0x01 to indicate that the public key linked with this private key is compressed.
# Again, this does not mean the private key is compressed, it just indicates that the public
# key generated with this public key is compressed.
# The prefix version number and compression flag is always 1 byte in size and the private_key_hex
# is 32 bytes.
# The private_key_with_version_comp value is always (1+32+1=) 34 bytes or 68 characters long.
#
# NOTICE that the prefix '80' is also needed, that is why we are concatenating private_key_with_version.
private_key_with_version_comp = private_key_with_version + '01'

# The private_key_wif_for_compressed value must be kept secret. It can be converted into QR codes
# for paper wallets. The WIF private key (compressed or uncompressed) is the one used by wallet apps.
# old versions of wallet apps don't support compressed wif.
# This WIF type starts with  a "K" or "L".

# The WIF
private_key_wif_for_compressed = utils.wif_private_key(private_key_with_version_comp)

# AND NOW THE PUBLIC KEY / PUBLIC ADDRESS, YES, THE ONE THAT YOU SHARE TO GET YOUR BITCOINS.
#
# There are two types of Public Keys, the compressed and uncompressed.
# "04" prefixed in Public Key value indicates that the Public Key is uncompressed.
# The prefix value is always 1 byte in size and the Public Key is 64 bytes.
# The public_key_version value is always (1+64=) 65 bytes or 130 characters long.
#
# The public keys are either 33 bytes (Public Key Compressed: public_key_versionComp) or 65 bytes long
# (Public Key Uncompressed: public_key_version). Compressed keys only specify the x coordinate plus an 1 byte
# flag indicating which side of the symmetrical curve the point is on, which allows y to be derived.
# Uncompressed keys is represented by two coordinates (x, y) and there is a 1 byte prefix added.
#
# Bitcoin originally only used uncompressed public keys, but since v0.6 compressed are now used.
#
# It is highly recommended to use the compressed public keys (public_key_versionComp) because they are smaller,
# resulting in smaller transactions on the network, saving block chain size for everyone.
#
# Some people say compressed keys are more secure, this is not true. It's all about optimization.
# It requires less computation and less space in the blockchain.

# THE UNCOMPRESSED KEY
#
# Although the private key in this demonstration was statically defined, we will generate
# the public key on the fly. We'll use pybitcointools library by Vitalik.
#
# Sorry guys but we won't discuss in this demo how Elliptic Curve Cryptography works, nor
# how to generate an ECDSA public key. Although, you are invited to take a look at how
# pybitcointools generates it.
#
# The following is the uncompressed 65 bytes public key, in hex encoding
# Why 65 bytes? The actual ECDSA public key is 64 bytes, but bitcoin protocol adds a prefix
# to indicate if its uncompressed or compressed. In this case a "04" prefix.
# That extra "04" is 1 byte.
public_key_version = pybitcointools.privkey_to_pubkey(private_key_hex)

# This will generate the hashed uncompressed public key,
# that is, the "bitcoin address" that you share with others.
# Again, the uncompressed format is not recommended anymore.
#
# The sharable bitcoin address:
public_address_uncompressed = utils.public_address(public_key_version)

# THE COMPRESSED KEY
# Compressed keys only specify the x coordinate plus an 1 byte
# flag indicating which side of the symmetrical curve the point is on, which allows y to be derived.
# In order to indicate that key is compressed, "02" or "03" prefix is added to the encoded hex value.
# The "02" and "03" is determined based on the the elliptic curve equation result.
#
# Public key with compression (32 bytes + 1 byte prefix = 33 bytes), in hex encoding
public_key_version_comp = pybitcointools.compress(public_key_version)

# This will generate the compressed public key,
# that is, the "bitcoin address" that you share with others.
# This is the modern and recommended format.
#
# The sharable bitcoin address (hashed public key for P2PKH script format, starts with 1).
# There is a newer P2SH format, so addresses for transactions using this script format start
# with number 3.
public_address_compressed = utils.public_address(public_key_version_comp)

# WE ARE DONE.
# Let's now print the WIF's and their corresponding Bitcoin public addresses.
# We are also going to verify that our public keys were correctly generated, comparing
# our public addresses with those generated by pybitcoin library:
# https://github.com/blockstack/pybitcoin

# Uncompressed Wallet
print("WIF corresponding to an UNCOMPRESSED public key:")
print(private_key_wif_for_uncompressed)


if utils.validate_public_against_py_bitcoin(private_key_hex, public_address_uncompressed, False):
    print("Verified Uncompressed Public Address:")
    print(public_address_uncompressed)
else:
    print("Ops!, Uncompressed Public Address does not match with the one generated by pybitcoin library.")

# Compressed Wallet

print("\nWIF corresponding to a COMPRESSED public key:")
print(private_key_wif_for_compressed)

if utils.validate_public_against_py_bitcoin(private_key_hex, public_address_compressed, True):
    print("Verified Compressed Public Address:")
    print(public_address_compressed)
else:
    print("Ops!, Compressed Public Address does not match with the one generated by pybitcoin library.")


# SUMMARY
# I hope this procedural approach helped you understand the steps for generating bitcoin
# wallets.
#
# Keep in mind that wallet apps sign transactions with the Private Key (not the WIF!), so
# they need to "unwrap" the WIF to get the actual PK.
