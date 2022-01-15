def get_socket(transport):
    sock = transport._sock
    sock.setblocking(True)
    return sock