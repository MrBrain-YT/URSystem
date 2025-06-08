from typing import Callable
from ssl import SSLContext, SSLSocket

class SNIRegistrator():

    def __init__(self, ssl_context:SSLContext) -> None:
        self.context = ssl_context

    def get_sni_callback(self) -> Callable:
        def custom_sni_callback(ssl_sock:SSLSocket, server_name:str, ssl_ctx:SSLContext):
            if server_name == "ursystem.local":
                self.context.load_cert_chain('certs\\URSystem.crt','certs\\URSystem.key')
            elif server_name == "localhost":
                self.context.load_cert_chain('certs\\localhost.crt','certs\\localhost.key')
            else:
                print(f'certs\\{ssl_sock.getsockname()[0]}.crt')
                self.context.load_cert_chain(f'certs\\{ssl_sock.getsockname()[0]}.crt',f'certs\\{ssl_sock.getsockname()[0]}.key')
                
        return custom_sni_callback