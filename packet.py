def create_header(data):
    # Pad data to ensure its a factor of 16 bits
    padding_length = (16 - (len(data) % 16)) % 16
    data += '0' * padding_length

    total = 0
    for i in range(0, len(data), 16):
        value = int(data[i:i+16], 2)
        total += value

    ones_complement = ~total & 0xFFFF
    header = format(ones_complement, '016b')

    return header

def verify_header(data, header):
    return create_header(data) == header

def create_packet(data):
    header = create_header(data)
    return header + data

def extract_packet(packet):
    header = packet[:16]
    data = packet[16:]
    if verify_header(data, header):
        return data
    else:
        raise ValueError("Header verification failed")
