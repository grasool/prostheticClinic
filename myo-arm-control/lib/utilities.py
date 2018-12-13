import struct

def pack(fmt, *args):
        out = '<' + fmt
        return struct.pack(out, *args)

def unpack(fmt, *args):
        return struct.unpack('<' + fmt, *args)

def multichr(values):
        return str.encode(''.join(map(chr, values)))

def multiord(values):
        return map(ord, values)
