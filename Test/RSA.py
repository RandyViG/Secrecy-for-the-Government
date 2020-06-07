from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256

with open( 'Diseño_SD_optimizacion_ver1.pdf', 'rb' ) as file:
    file_content = file.read( )
h = SHA256.new( )
h.update( file_content )
print( 'Original Hash:\n{}'.format( h.digest() ) )

# Generate the keys
private_key = RSA.generate( 2048 )
with open('mykey','wb') as f:
    f.write( private_key.export_key('PEM') )
f.close

public_key = private_key.publickey()
with open('mykey.pub',"wb") as f:
    f.write( public_key.export_key('PEM') )
f.close

# Encrypt
public_key = RSA.import_key( open('mykey.pub').read() )
cipher = PKCS1_OAEP.new( public_key )
cipher_file = cipher.encrypt( h.digest() )

# Decrypt
private_key = RSA.import_key( open('mykey').read() )
decipher = PKCS1_OAEP.new( private_key )
file_content = decipher.decrypt( cipher_file )

print( '\nHash:\n{}'.format( file_content ) )