import itertools
import datetime
import string

def rotl(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xffffffff

def hasher(x):
    a = 0x12345678
    b = 0xabcdef12
    c = 0x89abcdef
    d = 0x11111111

    for ch in x:
        val = ord(ch)
        for _ in range(4):
            a = (a ^ val) + rotl(b, 5) ^ (c & d)
            b = (b + a) ^ rotl(c, 7) + (a | d)
            c = (c ^ b) + rotl(d, 9) ^ (a & b)
            d = (d + c) ^ rotl(a, 13) + (b | c)

            a &= 0xffffffff
            b &= 0xffffffff
            c &= 0xffffffff
            d &= 0xffffffff

    for _ in range(12):
        a ^= rotl(b, 11)
        b += rotl(c, 7)
        c ^= rotl(d, 13)
        d += rotl(a, 17)

        a &= 0xffffffff
        b &= 0xffffffff
        c &= 0xffffffff
        d &= 0xffffffff

    return (a << 96) | (b << 64) | (c << 32) | d

def brute_force(target_hash, max_len=10):
    
    d=datetime.datetime.now()
    charset = string.ascii_lowercase

    for length in range(1, max_len + 1):
        for candidate in itertools.product(charset, repeat=length):
            s = ''.join(candidate)
            if hasher(s) == target_hash:
                e = datetime.datetime.now()-d
                return [s, e]
    e = datetime.datetime.now()-d
    return [-1, e]