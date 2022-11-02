## Process:
# Init server
# Connect with single client (manual)
# Send test message with single client
# Disconnect

### IN THE FUTURE: 
## Process:
# Init server
# Init client backend
# Connect with multiple clients (C1, C2, C3)
# Create channels for (C1, C2), (C1, C3), (C1, C2, C3)
# Have all users send a message in all channels
# Verify message recv
# Have C3 disconnect and reconnect, check if C3 can see messages.
# Disconnect all users
# Shutdown C1, C2 client backends
# Shutdown server
# Shutdown C3 client backend
import test_common

import json
import time

import compchat_server.main.core as core

import compchat_shared.networking.distributor as distributor

# Start the server
ServerCore = core.Core()
ServerCore.Start()

# Get a socket for the new client connection
ClientConnectionSocket = distributor.getSocket("localhost", "33826")

TestData = {
	"Channel": 0,
	"Data": {
		"Action": "TestMessage",
		"Text": "This is an example of a packet a client would send to the server."
	}
}

time.sleep(2)
print("Sending data.")
ClientConnectionSocket.sendall(json.dumps(TestData).encode())

TestData2 = {
	"Channel": 0,
	"Data": {
		"Action": "TestMessage",
		"Text": "This is a second example, similar to above."
	}

}

print("Sending more data.")
ClientConnectionSocket.sendall(json.dumps(TestData2).encode())