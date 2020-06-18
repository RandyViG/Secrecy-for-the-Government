from Crypto.Hash import SHA256
from Crypto.Util.number import getStrongPrime, inverse
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP
import base64

def getHash(f):
    h = SHA256.new( )
    h.update( f )
    return h

def rsaOPRF(h):
    h_aux=int.from_bytes(h.digest(), byteorder='little')
    #Llave Servidor
    private_key = RSA.import_key( open('pk.pub').read() )
    public_key = RSA.import_key( open('puk.pub').read() )
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
    aux=pow(z,e,n)%n
    if aux != h_aux:
        return None
    return getHash(z.to_bytes(256,byteorder='little'))

def aes256(h,f):
    #Cifrado
    cipher = AES.new( h , AES.MODE_CTR )
    nonce = cipher.nonce
    ciphertext = cipher.encrypt( f )
    #Descifrado
    decipher = AES.new(h, AES.MODE_CTR, nonce=nonce)
    aux = decipher.decrypt( ciphertext )

def rsaOAEP(h,key):
    # Encrypt
    cipher = PKCS1_OAEP.new( key.publickey() )
    cipher_file = cipher.encrypt( h )
    print("Cifrado:",base64.urlsafe_b64encode( cipher_file ).decode('ascii'),"\n")
    # Decrypt
    decipher = PKCS1_OAEP.new( key )
    file_content = decipher.decrypt( cipher_file )
    print("Después:",base64.urlsafe_b64encode( file_content ).decode('ascii'),"\n")

def generate_keys():
    pk = RSA.generate( 2048 )
    with open('pk','wb') as f:
        f.write( pk.export_key('PEM') )
    f.close
    puk = pk.publickey()
    with open('puk.pub',"wb") as f:
        f.write( puk.export_key('PEM') )

"""
f = "Soy una prueba de laboratorio."
h = rsaOPRF(getHash(f.encode()))
hfb = h.digest()
aes256(hfb,f.encode())
private_key = RSA.generate( 2048 )
print("Antes:",base64.urlsafe_b64encode( hfb ).decode('ascii'),"\n")
rsaOAEP(hfb,private_key)
"""
