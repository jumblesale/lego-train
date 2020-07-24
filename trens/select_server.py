import select
import socket
import time


def listen(ip, port):
    print("connecting...")
    local_ip = socket.gethostbyname(socket.gethostname())
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind((ip, port))
        s.listen()
        print(f"socket server listening on {local_ip}:{port}")
        return s
    except socket.error as err:
        print(f"socket creation failed with error {err}")
    except KeyboardInterrupt:
        print("received SIGINT, exiting...")
        _close(s)


def _close(_):
    print("closing connection")


server_socket = listen('', 9876)

read_list = [server_socket]


def loop():
    readable, writable, errored = select.select(read_list, [], [], 0)
    for s in readable:
        if s is server_socket:
            client_socket, (address, number) = server_socket.accept()
            read_list.append(client_socket)
            print(f"Connection from {address}, {number}")
        else:
            data = s.recv(1)
            if data:
                print(data)
                s.send(data)
            else:
                s.close()
                read_list.remove(s)
    time.sleep(0.001)
    yield


if __name__ == "__main__":
    while True:
        loop().__next__()
