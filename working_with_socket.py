import socket
port = 900
host = "127.0.0.1"
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("connecting")
    s.bind((host, port))
    s.listen()
    print("listening")
    conn, addr = s.accept()
    print("connection accepted")
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024).decode()
            direction, symbol = data.split("|")
            if direction == "upper":
                print("a signal to place an upper trade received")  
                conn.send("upper trade".encode());
            elif direction == "lower":
                print("a signal to place a low trade received")  
                conn.send("Low trade".encode());
            
            else:
                break

# sock.connect(('127.0.0.1', port))

# while True :
#     print(sock.recv(1024).decode())
# receive data from the server and decoding to get the string.
