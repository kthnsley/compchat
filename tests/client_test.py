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
ClientOne = client_backend.ClientBackend(1, ["localhost", "33826"])
# Start our second client
ClientTwo = client_backend.ClientBackend(2, ["localhost", "33826"])

time.sleep(1)

# Have both clients get the same channel
print(">>> CLIENT ONE GETTING CHANNEL")
ClientOne.SendMessage(0, {"Action": "GetChannel", "ChannelId": 100})
time.sleep(1)
print(">>> CLIENT TWO GETTING CHANNEL")
ClientTwo.SendMessage(0, {"Action": "GetChannel", "ChannelId": 100})
time.sleep(1)
print(">>> CLIENT ONE GETTING CHANNEL")
ClientOne.SendMessage(0, {"Action": "GetChannel", "ChannelId": 200})
time.sleep(1)
print(">>> CLIENT TWO GETTING CHANNEL")
ClientTwo.SendMessage(0, {"Action": "GetChannel", "ChannelId": 200})

# Generate 10 more clients because I want to see if I can
for i in range(2):
	time.sleep(0.1)
	ThisClient = client_backend.ClientBackend(3 + i, ["localhost", "33826"])
	time.sleep(0.1)
	ThisClient.SendMessage(0, {"Action": "GetChannel", "ChannelId": 100})

time.sleep(3)

print(">>> CLIENT ONE SENDING MESSAGE TO CHANNEL")
ClientOne.SendMessage(100, {"Text": "Hi everyone! How are you doing?"})

time.sleep(3)

print(">>> CLIENT ONE SENDING MESSAGE TO CHANNEL")
ClientOne.SendMessage(200, {"Text": "This is for just me and ClientTwo"})