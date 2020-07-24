import time
import socket


def listen(ip, port):
    print("connecting...")
    local_ip = socket.gethostbyname(socket.gethostname())
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind((ip, port))
        s.listen(5)
        print(f"trains server listening on {local_ip}:{port}")
        connection = _accept_connection(s)
        _handler(connection)
    except socket.error as err:
        print(f"socket creation failed with error {err}")
    except KeyboardInterrupt:
        print("received SIGINT, exiting...")
        _close(s)
    finally:
        _close(s)
        print("that's it I'm done goodbye x")


def _handler(connection):
    while True:
        time.sleep(0.1)
        # try:
        #     msg = _receive(connection)
        # except socket.error as err:
        #     print(f"something went wrong with the connection, closing\n{err}")
        print(f"what would you like to send?")
        message = input()
        _send_message(connection, message)


def _send_message(connection, message):
    connection.sendall(message.encode())


def _receive(connection):
    return connection.recv(4).rstrip().lower()


def _perform_handshake(connection):
    _send_message(connection, "hello?")
    response = connection.recv(6).rstrip().lower()
    print(f"received message \"{response}\"")
    if b"hello" != response:
        print("handshake failed, sorry :( got %s" % response)
        _send_message(connection, "you must respond with 'hello' "
                                  "to use this service")
        connection.close()
        return False
    print("handshake successful, creating connection")
    return True


def _accept_connection(s):
    connection, address = s.accept()
    print(f"received a connection from {address[0]} connection, performing handshake")
    if not _perform_handshake(connection):
        ...
    print(f"creating connection...")
    return connection


def _close(connection):
    print("closing connection")
