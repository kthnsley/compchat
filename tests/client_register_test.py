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

import time
import random

import compchat_server.main.core as core
import compchat_shared.networking.distributor as distributor
import compchat_shared.networking.socket_connection as socket_connection
import compchat_shared.structure.message as message

# Start the server
ServerCore = core.Core()
ServerCore.Start()

# Get a socket for the new client connection
ClientConnectionSocket = distributor.getSocket("localhost", "33826")
OurConnection = socket_connection.SocketConnection(ClientConnectionSocket)
ThisSourceId = random.randint(10000000000, 99999999999)

time.sleep(2)
print("[TEST] [client_register_test]: Registering to client.")
TestData = message.Message(
	ThisSourceId,
	0,
	{
		"Action": "RegisterClient",
	}
)
OurConnection.Send(TestData.ToJSON())

