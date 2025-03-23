  __  __                                     _____                         ______                             
 |  \/  |                                   |  __ \                       |  ____|                            
 | \  / |   ___    _ __     __ _    ___     | |__) |   __ _  __      __   | |__     _ __    _   _   _ __ ___  
 | |\/| |  / _ \  | '_ \   / _` |  / _ \    |  _  /   / _` | \ \ /\ / /   |  __|   | '_ \  | | | | | '_ ` _ \ 
 | |  | | | (_) | | | | | | (_| | | (_) |   | | \ \  | (_| |  \ V  V /    | |____  | | | | | |_| | | | | | | |
 |_|  |_|  \___/  |_| |_|  \__, |  \___/    |_|  \_\  \__,_|   \_/\_/     |______| |_| |_|  \__,_| |_| |_| |_|
                            __/ |                                                                             
                           |___/                                                                              

  #  MongoDB BSON Protocol Enumerator

This script is a **minimal, low-level MongoDB enumeration tool** that connects directly to a MongoDB server and communicates using the **raw wire protocol** over sockets and **BSON-encoded queries** — without using pymongo or official drivers.

It was built to:
- Explore unauthenticated MongoDB instances
- Understand how MongoDB’s internal protocol works
- Extract data from databases like `sensitive_information` when no client tools are available

>  Intended for **educational and authorized security research** only.

---

## Features

- Raw TCP socket connection to MongoDB server
- Manual BSON construction for:
  - `isMaster`
  - `listDatabases`
  - `listCollections`
  - `find`
- Enumerates all databases
- Attempts to list collections in each database
- Attempts to retrieve documents from each collection
- Dependency-light (only uses `bson`)
- Easy to customize target IP and DB
---

##  Requirements

- Python 3.6+
- `bson` module (install via `pip install pymongo` or `pip install bson`)

---

##  Usage

```bash
python3 minimal_mongo_enum.py
