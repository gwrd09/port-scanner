import socket

TARGET = "scanme.nmap.org"

def scan_port(hostname, port):
    address = socket.gethostbyname(hostname)
    s = socket.socket()
    s.settimeout(0.5)
    port_status = s.connect_ex((address, port))
    if not port_status:
        print(f"Port {port} | Status: OPEN")
    else:
        print(f"Port {port} | Status: CLOSED")

for port in range(1, 101):
    scan_port(TARGET, port)