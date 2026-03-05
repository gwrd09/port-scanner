import socket
import sqlite3
import datetime

def scan_port(hostname, port):
    address = socket.gethostbyname(hostname)
    s = socket.socket()
    s.settimeout(1)
    port_status = s.connect_ex((address, port))
    if not port_status:
        print(f"Port {port} | Status: OPEN")
        port_status = "OPEN"
    else:
        print(f"Port {port} | Status: CLOSED")
        port_status = "CLOSED"
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    con.execute("INSERT INTO scanner (ip, port, status, date) VALUES (?, ?, ?, ?)", (address, port, port_status, time))

TARGET = "scanme.nmap.org"

con = sqlite3.connect("scanner.db")
con.execute("""
    CREATE TABLE IF NOT EXISTS scanner(
        id INTEGER PRIMARY KEY,
        ip TEXT, 
        port INTEGER, 
        status TEXT, 
        date TEXT
    );
""")

for port in range(1, 101):
    scan_port(TARGET, port)
con.commit()