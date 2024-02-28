from OpenSSL import crypto

key = crypto.PKey()
key.generate_key(crypto.TYPE_RSA, 2048)

cert = crypto.X509()
cert.set_serial_number(1000)
cert.get_subject().C = 'Ru'
cert.get_subject().L = 'Tver'
cert.get_subject().O = 'Organization'
cert.get_subject().CN = 'localhost:8000'
cert.set_issuer(cert.get_subject())

cert.gmtime_adj_notBefore(0)
cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)
cert.set_pubkey(key)
cert.sign(key, 'sha256')

with open('certificate.crt', 'wb') as cert_file:
    cert_file.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

with open('private_key', 'wb') as key_file:
    key_file.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))

