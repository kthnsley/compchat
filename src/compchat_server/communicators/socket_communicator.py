import socket

# Declare Core type and import logging
from compchat_server.main import core as CompChatCore
from compchat_shared.utility import projlogging
from compchat_shared.networking import distributor, socket_connection

# This class defines the actual connection rather than the "service"
class CommunicatorConnection:
	Logger = projlogging.Logger("socket_communicator_connection")

	def __init__(Self, Core: CompChatCore.Core, Socket: socket.SocketType):
		Self.Core = Core
		Self.ThisConnection = socket_connection.SocketConnection(Socket, Self.__ReceiveData)

	def Check(Self) -> bool:
		# placeholder
		return True
	
	def Destroy(Self):
		pass

	def Replicate(Self, Message: str):
		Self.ThisConnection.Send(Message)

	def __ReceiveData(Self, Data):
		CommunicatorConnection.Logger.Log(f"Processing data in CommunicatorConnection, len {len(Data)}")
		# Process message when we get it
		Self.Core.MessageProcessor.ProcessMessage(Data)

class CommunicatorClass:
	# Main class for the connection, 
	MainLogger = projlogging.Logger("socket_communicator_main")

	def Start(Self, Core: CompChatCore.Core):
		Self.Core = Core

		# Create our SocketDistributor
		Self.MainLogger.Log("Creating distributor.")
		Self.SocketDistributor = distributor.DistributorServer(Callback=Self.HandleNewConnection)
		Self.SocketDistributor.Start(Port=33826)

	def Stop(Self):
		Self.SocketDistributor.Stop()

	def HandleNewConnection(Self, Socket: socket.SocketType):
		CommunicatorClass.MainLogger.Log(f"Got a new connection from {Socket.getsockname()}")
		NewConnection = CommunicatorConnection(Self.Core, Socket)
		# WIP: Do something with the connection to log it with the rest of the code
		