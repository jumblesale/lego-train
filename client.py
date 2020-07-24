import socket
import trens.server as server

if __name__ == "__main__":
    host, port = "127.0.0.1", 9876

    s = server.listen(host, port)

    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((host, port))
