import socket

from zeroconf import ServiceInfo, Zeroconf

def register_mdns_service(host:str=None, port:int=5000):
    zeroconf = Zeroconf()
    if host is None or host == "0.0.0.0":
        hostname = socket.gethostname()
        host = socket.gethostbyname(hostname)
    
    service_info = ServiceInfo(
        type_="_https._tcp.local.",
        name="Flask HTTPS App._https._tcp.local.",
        port=port,
        addresses=[socket.inet_aton(host)],
        properties={},
        server=f"ursystem.local."
    )
    
    zeroconf.register_service(service_info)
    return zeroconf