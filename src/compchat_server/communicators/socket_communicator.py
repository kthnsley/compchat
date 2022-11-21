import socket

import os
import ssl

# Declare Core type and import logging
from compchat_server.main import core as CompChatCore
from compchat_shared.utility import projlogging
from compchat_shared.networking import distributor, socket_connection

# This class defines the actual connection rather than the "service"
class CommunicatorConnection():
	Logger = projlogging.Logger("socket_communicator_connection")

	def __init__(Self, Core: CompChatCore, Socket: socket.SocketType):
		Self.Core = Core
		Self.ThisConnection = socket_connection.SocketConnection(Socket, Self.__ReceiveData)

	def Check(Self) -> bool:
		# placeholder
		return True
	
	def Destroy(Self):
		# Fully close the connection
		Self.ThisConnection.Close()

	def Replicate(Self, Message: str):
		Self.ThisConnection.Send(Message)

	def __ReceiveData(Self, Data):
		CommunicatorConnection.Logger.Log(f"Processing data in CommunicatorConnection, len {len(Data)}")
		# make sure this isn't a stop message
		# Process message when we get it
		Self.Core.MessageProcessor.ProcessMessage(Data, Self)

class CommunicatorClass():
	# Main class for the connection, 
	MainLogger = projlogging.Logger("socket_communicator_main")

	# Attempt to get SSL information
	SSL_ENABLED = False
	if (SSL_KEY := os.environ.get("COMPCHAT_SSL_KEY")) and (SSL_CRT := os.environ.get("COMPCHAT_SSL_CRT")):
		SSL_ENABLED = True

		MainLogger.Log("SSL is enabled.", 4)
		MainLogger.Log(f"SSL pub identity: {SSL_CRT}")

		SSL_CONTEXT = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
		SSL_CONTEXT.load_cert_chain(SSL_CRT, SSL_KEY)

	def Start(Self, Core: CompChatCore):
		Self.Core = Core

		# Create our SocketDistributor
		Self.MainLogger.Log("Creating distributor.")
		Self.SocketDistributor = distributor.DistributorServer(Callback=Self.HandleNewConnection)
		if Self.SSL_ENABLED:
			Self.SocketDistributor.Start(Port=33826, SSLContext=Self.SSL_CONTEXT)
		else:
			Self.SocketDistributor.Start(Port=33826)

	def Stop(Self):
		Self.SocketDistributor.Stop()

	def HandleNewConnection(Self, Socket: socket.SocketType):
		CommunicatorClass.MainLogger.Log(f"Got a new connection from {Socket.getsockname()}")
		# Do SSL wrapping
		if Self.SSL_ENABLED:
			Socket = Self.SSL_CONTEXT.wrap_socket(Socket, server_side=True)

		NewConnection = CommunicatorConnection(Self.Core, Socket)
			
		