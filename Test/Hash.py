from Crypto.Hash import SHA256

with open( 'Diseño_SD_optimizacion_ver1.pdf', 'rb' ) as file:
    fileContent = file.read( )

h = SHA256.new( )
h.update( fileContent )

print ('Hash of the file: {}'.format(h.hexdigest()))