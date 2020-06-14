from Crypto.Hash import SHA256
from Crypto.Util.number import getStrongPrime, inverse
from Crypto.PublicKey import RSA
import base64

# We start with the hash of the document
with open( 'Diseño_SD_optimizacion_ver1.pdf', 'rb' ) as file:
    fileContent = file.read( )

h = SHA256.new( )
h.update( fileContent )

# Convert byte string to int 
h_aux=int.from_bytes(h.digest(), byteorder='little')

# Generate the keys of the server
private_key = RSA.generate( 2048 )

public_key = private_key.publickey()

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


print("This is the hash of the document\n(int) {}\n(bytes) {}".format(h_aux,h_aux.to_bytes(32,byteorder='little')))

#The hash we want to save it in firebase in base64 string, this is the way
h_base64b=base64.encodestring( h.digest() )
h_base64s=h_base64b.decode('ascii')
print("This is the hash of the document in base64 {}".format(h_base64s))

#To return to byte
h_base64b=str.encode(h_base64s)
print("This is the hash of the document in base64 {}".format(h_base64b))

aux=pow(z,e,n)
print("\nThis is the comprobation that RSA - OPRF z^e mod n is equal to the hash\n(int) {}\n(bytes) {}".format(aux,aux.to_bytes(32,byteorder='little')))
