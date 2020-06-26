#!/bin/bash

export FLASK_DEBUG=1
#Generate the certificate
#openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
flask run --cert=cert.pem --key=key.pem

