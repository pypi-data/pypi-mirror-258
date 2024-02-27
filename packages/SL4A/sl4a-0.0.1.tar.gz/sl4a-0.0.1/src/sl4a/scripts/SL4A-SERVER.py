#!/bin/python3
import os, json
d={
  "AP_PORT":os.environ["AP_PORT"],
  "AP_HOST":os.environ["AP_HOST"],
  "AP_HANDSHAKE":os.environ["AP_HANDSHAKE"],
  }
with open("/sdcard/sl4a/server.json","w") as f:
  json.dump(d,f,indent=2)
print("SL4A server is running")
input("Press Enter to stop the server")
