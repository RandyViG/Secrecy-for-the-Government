from Crypto.Hash import SHA256
from Crypto.Util.number import getStrongPrime, inverse
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
import base64
import binascii

# Obtenermos el hash del archivo
with open( 'Diseño_SD_optimizacion_ver1.pdf', 'rb' ) as file:
    fileContent = file.read( )

h = SHA256.new( )
h.update( fileContent ) #Esto regresa get hash

#Lo mandamos a RSA-OPRF
print(h.digest())
# Convert byte string to int 
h_aux=int.from_bytes(h.digest(), byteorder='little')

private_key = RSA.import_key( open('privateServer.pem').read() )
public_key = RSA.import_key( open('publicServer.pem').read() )

# Public exponent
e=public_key.e
# Product of p*q (numbers primes)
n=public_key.n

# Private exponent
d=private_key.d

# We obtain a random int, but the random int have to be coprime of N (bc of the inverse)
r=getStrongPrime(512,n)

r_inverse=inverse(r,n)

aux=pow(r, e, n)
x=(h_aux*aux)%n

aux=pow(x, d, n)
y=aux%n

z=(y*r_inverse)%n


h = SHA256.new( )
h.update( z.to_bytes(256,byteorder='little') ) #Esto regresa get hash
Gz=h.digest()


#Cifrado
cipher = AES.new( Gz , AES.MODE_CTR )
nonce = cipher.nonce
ciphertext = cipher.encrypt( fileContent )

#Hexadecimal , esto es lo que se guarda en la base de datos
encryptFile_hexa = binascii.hexlify( ciphertext )
y = str( encryptFile_hexa,'ascii' )
#print(encryptFile_hexa)
#print(type(y))


#Vamos a cifrar el hash firmado con la llave publica del cliente
public_key = RSA.import_key( open('0001.pem').read() )
cipher = PKCS1_OAEP.new( public_key )
cipher_key = cipher.encrypt( Gz )
print(Gz)
print(nonce)
#print(cipher_key)
#todo lo anterior es el proceso de cifrado del archivo y de llaves

#Descifrado
#primero deciframos la llave (hash firmado)
# Decrypt
private_key = RSA.import_key( open('privateKey.pem').read() )
decipher = PKCS1_OAEP.new( private_key )
file_content = decipher.decrypt( cipher_key )

#print(file_content)
#regresamos a bytes el mensaje cifrado
h_base64b=str.encode(y)
#print(y)
h_base64b=binascii.unhexlify(h_base64b)
#print(h_base64b)

decipher = AES.new(file_content, AES.MODE_CTR, nonce=nonce)
aux = decipher.decrypt( h_base64b )

with open( 'decrypt.pdf' , 'wb' ) as f:
    f.write( aux )
