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

# Also uses way too many dicts when we should just have one dict with helper funcs, but 2lazy
class ServerClient():
	def __init__(Self, Core: CompChatCore, ConnectionManager, SourceId: int):
		Self.Core = Core
		Self.ConnectionManager = ConnectionManager
		Self.SourceId = SourceId
		Self.ClientChannels = [] #WIP: Pull from database
		Self.Logger = projlogging.Logger(f"connection_manager_client_{SourceId}")
		
	def Replicate(Self, Message: message.Message):
		Message = Message.ToJSON()
		for UserConnection in Self.ConnectionManager.GetClientConnectionsById(Self.SourceId):
			UserConnection.Replicate(Message)


# Main class Mainly just need a way to track Client connections. Run keepalives,
# provide a way for other parts to send messages to clients.
class ConnectionManager():
	Logger = projlogging.Logger("connection_manager")

	ConnectionTimeoutTime = 10 # how long a connection needs to be dead before we close it

	# Add a connection to their table
	def AddConnection(Self, Connection, SourceId: int):
		Self.Logger.Log(f"Adding connection for SourceId {SourceId}")
		Self.GetClientConnectionsById(SourceId).append(Connection)
		#print(Self.CurrentConnections)

		if Self.ConnectedClients.get(SourceId) == None:
			Self.ConnectedClients[SourceId] = ServerClient(Self.Core, Self, SourceId)

		Self.ConnectionToClient[Connection] = Self.ConnectedClients[SourceId]

	# Remove a connection from their table
	def RemoveConnection(Self, Connection, SourceId: int):
		if SourceId == None:
			SourceId = Self.GetClientByConnection(Connection).SourceId

		ThisClient = Self.GetClientById(SourceId)
		ThisClientConnections = Self.GetClientConnectionsById(SourceId)

		try:
			ThisClientConnections.remove(Connection)
		except Exception as Excp:
			Self.Logger.Log(f"Failed to remove connection for Client {SourceId}", 3)
			Self.Logger.Log(f"Exception: {traceback.format_exc()}")

		if Self.ConnectionTimeouts.get(Connection):
			Self.ConnectionTimeouts.pop(Connection)

		if len(ThisClientConnections) == 0 and Self.ConnectedClients.get(SourceId):
			# remove client from all of their channel tables
			del Self.ConnectedClients[SourceId]

		if ThisClient:
			Self.ConnectionToClient.pop(Connection)
			# also cleanup table
			for Channel in ThisClient.ClientChannels:
				Channel.RemoveClient(ThisClient)


		Connection.Destroy()

	def GetClientConnectionsById(Self, SourceId: int) -> list:
		ClientConnections = Self.CurrentConnections.get(SourceId)
		if ClientConnections:
			Self.Logger.Log(f"Got Client connections for {SourceId}: {len(ClientConnections)}")
		else:
			Self.Logger.Log(f"No old client connections found for {SourceId}. Making new table.")
			Self.CurrentConnections[SourceId] = []
			return Self.CurrentConnections[SourceId]

		return ClientConnections

	def GetClientById(Self, SourceId: int):
		ThisClient = Self.ConnectedClients.get(SourceId)
		if ThisClient:
			return ThisClient
		else:
			Self.Logger.Log(f"Client {SourceId} is not connected, not returning.")

	def GetClientByConnection(Self, Connection):
		if Self.ConnectionToClient.get(Connection):
			return Self.ConnectionToClient[Connection]

	def __ConnectionCleanup(Self):
		while Self.Core.Running:
			time.sleep(1)
			for SourceId, ClientConnections in Self.CurrentConnections.items():
				for ClientConnection in ClientConnections:
					if ClientConnection.Check():
						Self.ConnectionTimeouts[ClientConnection] = 0
					else:
						CurrentTimeout = Self.ConnectionTimeouts.get(ClientConnection, 0)
						if CurrentTimeout + 1 >= Self.ConnectionTimeoutTime:
							Self.RemoveConnection(ClientConnection, SourceId)
						else:
							Self.ConnectionTimeouts[ClientConnection] = CurrentTimeout + 1

	def __init__(Self, Core: CompChatCore):
		Self.Core = Core
		Self.CurrentConnections = {}
		Self.ConnectionTimeouts = {} # hold connections
		Self.ConnectedClients = {}
		Self.ConnectionToClient = {}

		threading.Thread(target=Self.__ConnectionCleanup).start()