import test_common
import os

# Add SSL keys to environ
OUR_PATH = os.path.dirname(__file__)
print(OUR_PATH)
os.environ["COMPCHAT_SSL_KEY"] = OUR_PATH + "/ssl/example.key"
os.environ["COMPCHAT_SSL_CRT"] = OUR_PATH + "/ssl/example.crt"
os.environ["COMPCHAT_SSL_ENABLED"] = "1"

import run_server