def _reset_alphabet(alphabet: dict, alphabet_bitsize: int) -> int:
    alphabet.clear()
    alphabet.update(((n, ), n) for n in range(2 ** alphabet_bitsize))

    alphabet['clean_code'] = 2 ** alphabet_bitsize
    alphabet['end_code'] = 2 ** alphabet_bitsize + 1

    return 2 ** alphabet_bitsize + 2


def _define_stop(start: int, data: tuple[int], alphabet: dict) -> int:
    for stop in range(start + 1, len(data) + 1):
        sample = data[start:stop]
        if not(sample in alphabet):
            return stop - 1
    return len(data)


def lzw(data: tuple[int], datacodes_bitsize: int=2):
    alphabet: dict = {}
    freecode = _reset_alphabet(alphabet, datacodes_bitsize)
    codes_bitlen = datacodes_bitsize + 1

    start, stop = 0, 1

    while stop < len(data):
        stop = _define_stop(start, data, alphabet)

        sample = data[start:stop]
        yield alphabet[sample], codes_bitlen

        alphabet[data[start:stop + 1]] = freecode

        start = stop
        freecode += 1

        if freecode == 2 ** 12:
            freecode = _reset_alphabet(alphabet, datacodes_bitsize)
            codes_bitlen = datacodes_bitsize + 1
            yield alphabet['clean_code'], codes_bitlen
            
        if bin(freecode - 1).count('1') == 1:
            codes_bitlen += 1
            
    yield alphabet['end_code'], codes_bitlen


def packlzw(codes):
    string = ''

    for n, L in codes:
        n = bin(n)[2:]
        n = (L - len(n)) * '0' + n
        string = n + string

        while len(string) >= 8:
            yield int(string[-8:], base=2)
            string = string[:-8]
    if string:
        yield int(string, base=2)


def packbytes(bytestream):
    bytecode = bytearray()

    bytecount = 0
    bytecode.append(0)
    for bytevalue in bytestream:
        if bytecount == 255:
            bytecount = 0
            bytecode[-256] = 255
            bytecode.append(0)
            
        bytecode.append(bytevalue)
        
        bytecount += 1
    bytecode[-(bytecount + 1)] = bytecount
    return bytecode


# Tests
assert tuple(packbytes((2, 44, 55, 66))) == (4, 2, 44, 55, 66)

assert tuple(packlzw(((15, 4), )* 4)) == (255, 255)

_test = 1, 7, 1, 3, 1, 7, 1, 1, 7, 6, 5, 3, 1, 7, 0
assert tuple(lzw(_test, 3)) == (
    (1, 4),
    (7, 4),
    (1, 4),
    (3, 4),
    (10, 4),
    (1, 4),
    (10, 4),
    (6, 5),
    (5, 5),
    (13, 5),
    (7, 5),
    (0, 5),
    (9, 5))













































#
