import socket
import threading

# Declare Core type and import logging
from compchat_server.main import core as CompChatCore
from compchat_shared.utility import projlogging
from compchat_shared.networking import distributor

class CommunicatorConnection():
	Logger = projlogging.Logger("socket_communicator_connection")

	def __init__(Self, Core: CompChatCore):
		pass

	def Check(Self):
		pass
	
	def Destroy(Self):
		pass

	def Replicate(self):
		pass

class CommunicatorClass:
	MainLogger = projlogging.Logger("socket_communicator_main")

	def Start(Self, Core: CompChatCore):
		Self.Core = Core

		# Create our SocketDistributor
		Self.MainLogger.Log("Creating distributor.")
		Self.SocketDistributor = distributor.DistributorServer(Callback=Self.HandleNewConnection)
		Self.SocketDistributor.Start(Port=33826)

	def Stop(Self):
		Self.SocketDistributor.Stop()

	def HandleNewConnection(Self, Socket: socket.SocketType):
		# at this point, we are on a random port with the connection
		print("Socket communicator got a new socket")
		
		Chunks = []
		while True:
			Data = Socket.recv(2048)
			if Data:
				Chunks.append(Data)
				print(Data)
		
		print("passed")