from Crypto.Hash import SHA256
from Crypto.Util.number import getStrongPrime, inverse
from Crypto.PublicKey.RSA import construct
from Crypto.PublicKey import RSA
import numpy

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

aux=pow(z,e,n)
print("\nThis is the comprobation of de RSA - OPRF z^e mod n is equal to the hash\n(int) {}\n(bytes) {}".format(aux,aux.to_bytes(32,byteorder='little')))
