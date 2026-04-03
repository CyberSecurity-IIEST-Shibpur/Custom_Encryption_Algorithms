import itertools
import datetime
import string

def rotl(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xffffffff

def hasher(x, a=0x12345678, b=0xabcdef12, c=0x89abcdef, d=0x11111111, MEM_SIZE=2000000, sec_seed=0x9e8d7c6b):
    mem = [0] * MEM_SIZE

    seed = a ^ b ^ c ^ d
    for i in range(MEM_SIZE):
        seed = (seed + rotl(seed, 13) ^ sec_seed + i) & 0xffffffff
        mem[i] = seed

    for ch in x:
        val = ord(ch)

        v1 = val
        v2 = rotl(val, 8)
        v3 = rotl(val, 16)
        v4 = rotl(val, 24)

        for _ in range(4):
            a = (a + (b ^ v1) + rotl(c, 5)) ^ d
            b = (b + (c ^ v2) + rotl(d, 7)) ^ a
            c = (c + (d ^ v3) + rotl(a, 9)) ^ b
            d = (d + (a ^ v4) + rotl(b, 13)) ^ c

            a &= 0xffffffff
            b &= 0xffffffff
            c &= 0xffffffff
            d &= 0xffffffff

            idx1 = (a ^ b ^ c ^ d) % MEM_SIZE
            val1 = mem[idx1]

            idx2 = (val1 ^ rotl(a, 7) ^ b) % MEM_SIZE
            val2 = mem[idx2]

            a = (a + val1) ^ rotl(val2, 5)
            b = (b ^ val2) + rotl(val1, 7)
            c = (c + val1 ^ val2) + rotl(a, 9)
            d = (d ^ val1) + rotl(b, 13)

            a &= 0xffffffff
            b &= 0xffffffff
            c &= 0xffffffff
            d &= 0xffffffff

            mem[idx1] = (val2 ^ a ^ b) & 0xffffffff
            mem[idx2] = (val1 ^ c ^ d) & 0xffffffff

    for _ in range(12):
        idx = (a ^ rotl(b, 11) ^ c ^ d) % MEM_SIZE
        m = mem[idx]

        a = (a + rotl(b, 11) + m) ^ c
        b = (b + rotl(c, 7) + m) ^ d
        c = (c + rotl(d, 13) + m) ^ a
        d = (d + rotl(a, 17) + m) ^ b

        a &= 0xffffffff
        b &= 0xffffffff
        c &= 0xffffffff
        d &= 0xffffffff

        mem[idx] = (m ^ a ^ b ^ c ^ d) & 0xffffffff

    return (a << 96) | (b << 64) | (c << 32) | d

def brute_force(target_hash, max_len=10):
    start = datetime.datetime.now()

    hasher_local = hasher
    charset = string.ascii_lowercase
    base = 26

    for length in range(1, max_len + 1):
        arr = [0] * length

        while True:
            s = ''.join(charset[i] for i in arr)

            if hasher_local(s) == target_hash:
                return [s, datetime.datetime.now() - start]

            i = 0
            while i < length:
                arr[i] += 1
                if arr[i] < base:
                    break
                arr[i] = 0
                i += 1
            else:
                break
            
    return [-1, datetime.datetime.now() - start]