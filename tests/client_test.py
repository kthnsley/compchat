import test_common
import random
import time

import compchat_server.main.core as core
import compchat_client_backend.main as client_backend

# Generate needed data
BaseId = random.randint(10000000000, 99999999999)

# Start the server
ServerCore = core.Core()
ServerCore.Start()

# Start our first client
ClientOne = client_backend.ClientBackend(BaseId, ["localhost", "33826"])
# Start our second client
ClientTwo = client_backend.ClientBackend(BaseId * 2, ["localhost", "33826"])

time.sleep(1)

# Have both clients get the same channel
print(">>> CLIENT ONE GETTING CHANNEL")
ClientOne.SendMessage(0, {"Action": "GetChannel", "ChannelId": BaseId * 4})
time.sleep(1)
print(">>> CLIENT TWO GETTING CHANNEL")
ClientTwo.SendMessage(0, {"Action": "GetChannel", "ChannelId": BaseId * 4})