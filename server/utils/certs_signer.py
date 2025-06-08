import os
import socket
from datetime import datetime, timedelta
from pathlib import Path

from OpenSSL import crypto

def create_self_signed_cert(cert_dir:str, ip_address:str):
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 1024)   #  размер может быть 2048, 4196

    #  Создание сертификата
    cert = crypto.X509()
    cert.get_subject().C = "RU"
    cert.get_subject().ST = "Tatarstan"
    cert.get_subject().L = "Naberezhnye Chelny"
    cert.get_subject().O = "URSystem Widgets Ltd"
    cert.get_subject().OU = "URSecurity"
    cert.get_subject().CN = ip_address
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    expire_date = (datetime.utcnow() + timedelta(days=100*365)).strftime("%Y%m%d%H%M%SZ")
    cert.set_notAfter(expire_date.encode())
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha1')
    
    crt_dir = os.path.join(cert_dir, f"{ip_address}.crt")
    key_dir = os.path.join(cert_dir, f"{ip_address}.key")
    if not os.path.exists(crt_dir) or not os.path.exists(key_dir):
        Path(crt_dir).unlink(missing_ok=True)
        Path(key_dir).unlink(missing_ok=True)
    
        with open(crt_dir, "wb") as f:
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        with open(key_dir, "wb") as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
        
def get_my_ip_adresses() -> list:
    hosts = ["127.0.0.1"]
    hostname = socket.gethostname()
    ips = socket.gethostbyname_ex(hostname)[2]
    hosts.extend(ips)
    return hosts

def create_certs() -> None:
    # check multicast dns certificate
    if not os.path.exists("certs/URSystem.crt") or not os.path.exists("certs/URSystem.key"):
        Path('certs/URSystem.crt').unlink(missing_ok=True)
        Path('certs/URSystem.key').unlink(missing_ok=True)
        create_self_signed_cert("certs", "ursystem.local")
    # check localhost certificate
    if not os.path.exists("certs/localhost.crt") or not os.path.exists("certs/localhost.key"):
        Path('certs/localhost.crt').unlink(missing_ok=True)
        Path('certs/localhost.key').unlink(missing_ok=True)
        create_self_signed_cert("certs", "localhost")
    # check other ip adresses certificates
    for ip in get_my_ip_adresses():
        create_self_signed_cert("certs", ip)

if __name__ == "__main__":
    for ip in get_my_ip_adresses():
        create_self_signed_cert(".", ip)