import struct


class IPv4:
    def __init__(self, raw_data):
        header_length = raw_data[0]
        self.version = header_length >> 4
        self.header_length = (header_length & 15) * 4
        self.ttl, self.proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', raw_data[:20])
        self.src = self.getAddr(src)
        self.target = self.getAddr(target)
        self.data = raw_data[self.header_length:]

    def getAddr(self, addr):
        return '.'.join(map(str, addr))