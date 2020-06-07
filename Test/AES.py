from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

with open( 'Diseño_SD_optimizacion_ver1.pdf', 'rb' ) as file:
    fileContent = file.read()

key = get_random_bytes( 32 )
cipher = AES.new( key , AES.MODE_CTR )

nonce = cipher.nonce
ciphertext = cipher.encrypt( fileContent )

with open( 'encrypt.pdf' , 'wb' ) as f:
    f.write( ciphertext )

with open( 'encrypt.pdf' , 'rb' ) as fi:
    dec = fi.read()

decipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
aux = decipher.decrypt( dec )

with open( 'recuperando.pdf' , 'wb' ) as f:
    f.write( aux )