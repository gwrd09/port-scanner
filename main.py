import socket
import sqlite3
import datetime

port_data = []

def scan_port(hostname, port):
    address = socket.gethostbyname(hostname)
    s = socket.socket()
    s.settimeout(0.5)
    port_status = s.connect_ex((address, port))
    if not port_status:
        print(f"Port {port} | Status: OPEN")
        port_status = "OPEN"
    else:
        print(f"Port {port} | Status: CLOSED")
        port_status = "CLOSED"
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    port_data.append([address, port, port_status, time])

def upload_data(data_dict):
    global port_data
    for record in data_dict:
        con.execute("INSERT INTO scanner (ip, port, status, date) VALUES (?, ?, ?, ?)", (record[0], record[1], record[2], record[3]))
    con.commit()
    port_data = []

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

TARGET = "scanme.nmap.org"

for port in range(1, 101):
    scan_port(TARGET, port)
upload_data(port_data)