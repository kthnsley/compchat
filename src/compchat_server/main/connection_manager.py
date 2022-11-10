# Create connections when specified, provide functions to wrap around using the messages to make
# outside modules not care about what communicator is being used when trying to send messages
# to and from.

# Declare Core type and import logging
from compchat_server.main import core as CompChatCore
from compchat_shared.utility import projlogging
from compchat_shared.structure import message

import threading
import time
import traceback

# Defines a client and data about the client.
# This isn't very intuitive, but this only provides data. All actual methods should be sent through
# the ConnectionManager. I would refactor this to make more sense, but it shouldn't be too 
# hard to understand and should work fine.
class __ServerClient():
	Logger = projlogging.Logger("client_manager_server_client")

	def __init__(Self, Core: CompChatCore.Core, ConnectionManager, ClientId: int):
		Self.Core = Core
		Self.ConnectionManager = ConnectionManager
		Self.ClientId = ClientId
		Self.ClientChannels = {}
		
	def Replicate(Self, Message: message.Message):
		Message = Message.ToJSON()
		for UserConnection in ConnectionManager.GetConnectionsByClient(Self.ClientId):
			UserConnection.Replicate(Message)


# Main class Mainly just need a way to track Client connections. Run keepalives,
# provide a way for other parts to send messages to clients.
class ConnectionManager():
	Logger = projlogging.Logger("connection_manager")

	ConnectionTimeoutTime = 10 # how long a connection needs to be dead before we close it

	# Add a connection to their table
	def AddConnection(Self, Connection, ClientId: int):
		Self.GetConnectionsByClient(ClientId).append(Connection)

		if Self.ConnectedClients.get(ClientId) == None:
			Self.ConnectedClients[ClientId] = __ServerClient(Self, Self.Core, ClientId)

	# Remove a connection from their table
	def RemoveConnection(Self, Connection, ClientId: int):
		ThisClientConnections = Self.GetConnectionsByClient(ClientId)
		try:
			ThisClientConnections.remove(Connection)
		except Exception as Excp:
			Self.Logger.Log(f"Failed to remove connection for Client {ClientId}", 3)
			Self.Logger.Log(f"Exception: {traceback.format_exc()}")

		if Self.ConnectionTimeouts.get(Connection):
			del Self.ConnectionTimeouts[Connection]

		ThisClient = Self.ConnectedClients.get(ClientId)

		if len(ThisClientConnections) == 0 and ThisClient:
			del Self.ConnectedClients[ThisClient]

		Connection.Destroy()

	def GetClientConnectionsById(Self, ClientId: int) -> list:
		ClientConnections = Self.CurrentConnections.get(str(ClientId), [])
		Self.Logger.Log(f"Got Client connections for {ClientId}: {ClientConnections}")

	def ReplicateMessageToClientById(Self, ClientId: int, Message: message.Message):
		ThisClient = Self.ConnectedClients.get(ClientId)
		if ThisClient:
			ThisClient.Replicate(Message)
		else:
			Self.Logger.Log(f"Client {ClientId} is not connected, not replicating.")

	def __ConnectionCleanup(Self):
		while Self.Core.Running:
			time.sleep(1)
			for ClientId, ClientConnections in Self.CurrentConnections.items():
				for ClientConnection in ClientConnections:
					if ClientConnection.Check():
						Self.ConnectionTimeouts[ClientConnection] = 0
					else:
						CurrentTimeout = Self.ConnectionTimeouts.get(ClientConnection, 0)
						if CurrentTimeout + 1 >= Self.ConnectionTimeoutTime:
							Self.RemoveConnection(ClientConnection, ClientId)
						else:
							Self.ConnectionTimeouts[ClientConnection] = CurrentTimeout + 1

	def __init__(Self, Core: CompChatCore.Core):
		Self.Core = Core
		Self.CurrentConnections = {}
		Self.ConnectionTimeouts = {} # hold connections
		Self.ConnectedClients = {}

		threading.Thread(target=Self.__ConnectionCleanup).start()