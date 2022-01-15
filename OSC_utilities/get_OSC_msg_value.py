def get_OSC_msg_value(sock):
    data, _ = sock.recvfrom(4096)
    value  = data[-1]
    return value
    