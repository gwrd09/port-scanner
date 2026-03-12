import socket, sqlite3, datetime, threading

port_data = []

def scan_port(address, port):
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

def start_threads(address):
    active_threads = []
    for port in range(1, 65536):
        thread = threading.Thread(target=scan_port, args=(address, port))
        active_threads.append(thread)
    for thread in active_threads:
        thread.start()
    for thread in active_threads:
        thread.join()

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

address = socket.gethostbyname(TARGET)
start_threads(address)
upload_data(port_data)