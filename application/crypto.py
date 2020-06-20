from Crypto.Hash import SHA256
from Crypto.Util.number import getStrongPrime, inverse
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP
from os.path import isfile
import base64

def getHash(f):
    h = SHA256.new( )
    h.update( f )
    return h

def rsaOPRF(h):
    h_aux=int.from_bytes(h.digest(), byteorder='little')
    #Llave Servidor
    private_key = RSA.import_key( open('./application/server/privateServer.pem').read() )
    public_key = RSA.import_key( open('./application/server/publicServer.pem').read() )
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
    private = './application/server/privateServer.pem'
    public = './application/server/publicServer.pem'
    
    if isfile(private) and isfile( public):
        return
    pk = RSA.generate( 2048 )
    with open('./application/server/privateServer.pem','wb') as f:
        f.write( pk.export_key('PEM') )
    f.close()
    puk = pk.publickey()
    with open('./application/server/publicServer.pem',"wb") as f:
        f.write( puk.export_key('PEM') )
    f.close()
