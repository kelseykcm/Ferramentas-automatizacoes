import codecs
import string

def hexdump(data: bytes, width: int = 16):
    for i in range(0, len(data), width):
        chunk = data[i:i+width]
        hex_part = " ".join(f"{b:02x}" for b in chunk)
        ascii_part = "".join(chr(b) if 32 <= b <= 126 else "." for b in chunk)
        print(f"{i:08x}  {hex_part:<{width*3}}  {ascii_part}")

def try_decode(data: bytes):
    encodings = ["utf-8", "latin-1", "cp1252"]
    for enc in encodings:
        try:
            text = data.decode(enc)
            print(f"\n[+] Decodificado com {enc}:")
            print(text)
        except UnicodeDecodeError:
            print(f"\n[-] Não foi possível decodificar com {enc}")

def is_mostly_printable(data: bytes, threshold: float = 0.85) -> bool:
    if not data:
        return True
    printable = sum(
        1 for b in data
        if chr(b) in string.printable or b in (9, 10, 13)
    )
    return (printable / len(data)) >= threshold

def parse_escaped_string(s: str) -> bytes:
    # Interpreta escapes como \xNN, \n, \t, \, etc.
    unescaped = codecs.decode(s, "unicode_escape")
    # Converte o resultado para bytes preservando valores 0-255
    return unescaped.encode("latin-1", errors="replace")

if __name__ == "__main__":
    s = r"import codecs"
import string

def hexdump(data: bytes, width: int = 16):
    for i in range(0, len(data), width):
        chunk = data[i:i+width]
        hex_part = " ".join(f"{b:02x}" for b in chunk)
        ascii_part = "".join(chr(b) if 32 <= b <= 126 else "." for b in chunk)
        print(f"{i:08x}  {hex_part:<{width*3}}  {ascii_part}")

def try_decode(data: bytes):
    encodings = ["utf-8", "latin-1", "cp1252"]
    for enc in encodings:
        try:
            text = data.decode(enc)
            print(f"\n[+] Decodificado com {enc}:")
            print(text)
        except UnicodeDecodeError:
            print(f"\n[-] Não foi possível decodificar com {enc}")

def is_mostly_printable(data: bytes, threshold: float = 0.85) -> bool:
    if not data:
        return True
    printable = sum(
        1 for b in data
        if chr(b) in string.printable or b in (9, 10, 13)
    )
    return (printable / len(data)) >= threshold

def parse_escaped_string(s: str) -> bytes:
    # Interpreta escapes como \xNN, \n, \t, \, etc.
    unescaped = codecs.decode(s, "unicode_escape")
    # Converte o resultado para bytes preservando valores 0-255
    return unescaped.encode("latin-1", errors="replace")

if __name__ == "__main__":
    s = r"""L\x01\x82\xa5\xbbẃ8\x7f\x81\xa1\xbbuͱ\x82(\x87.\xe4!1\xdd\x08e\xb5\xc0\x0f\xd6.3e\xd6\x0c\x9eJ\xa60\xe2\xdcv\x91\xb2\xc2J,\xf3\xe2\xb0N\x90\x1b\xf9x\xc0\xb31\x0e\xd72\x96\xd0\xfdz\xb3De\x97\xfcBPj\xc9U\x9e\xb8\'ۈf\x8c\x87\x8d\xb9\x90Op\xa6T\xbe}\x97\xd0\xeb\x1d\xce\xe3\x8d\xe89\xbb`\xbbp\xc8\x1d,^T\xc0\\xca\xe7<K\xb6\xa6&\x97\xe7]˹\x1e\x8fa\x15\xaa\xadq\x81<\x80W\x1dx\x0f\xa95\x9a\x90":\x83\xba3A\xa0.7\x07L<\xa54\xac\x93"\xf4\xbb\x90\x94Ĥ\xdc|\xeb\xb60ܧ\xf7\x87\xe5fBϩ\xe4Bz\x93g>\xf0\xdcS\x19H@\xb9\xe7z\xa8\xff5\x84\x175 \x80\xb0DZԀ\x02\xb8\x1c\xb27\xfd\xdc\xebj\xdf\xc5\'t\xb5_b\xd5ʪ\x00\xe24\xf7\xdd\x10\xc0\xbb\xcd\xe5\xeb\xfa3"W\xb5\xf6\r\x96\xa9\xe6\xaa\xc1oIL]\xf9u@N\xa2\xf2?\x9f\x1c\x95\t\xdd"""
    
    data = parse_escaped_string(s)

    print(f"[+] Total de bytes: {len(data)}")
    print(f"[+] Parece texto? {'sim' if is_mostly_printable(data) else 'não'}")

    print("\n[+] Hexdump:")
    hexdump(data)

    print("\n[+] Tentativas de decodificação:")
    try_decode(data)

    with open("saida.bin", "wb") as f:
        f.write(data)

    print("\n[+] Bytes salvos em saida.bin")
    
    data = parse_escaped_string(s)

    print(f"[+] Total de bytes: {len(data)}")
    print(f"[+] Parece texto? {'sim' if is_mostly_printable(data) else 'não'}")

    print("\n[+] Hexdump:")
    hexdump(data)

    print("\n[+] Tentativas de decodificação:")
    try_decode(data)

    with open("saida.bin", "wb") as f:
        f.write(data)

    print("\n[+] Bytes salvos em saida.bin")