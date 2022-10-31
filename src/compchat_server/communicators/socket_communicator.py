import socket

# Declare Core type and import logging
from compchat_server.main import core as CompChatCore
from compchat_shared.utility import projlogging
from compchat_shared.networking import distributor

class Communicator():
	Logger = projlogging.Logger("socket_communicator_connection")

	def __init__(Self, Core: CompChatCore):
		pass

	def Check(Self):
		pass
	
	def Destroy(Self):
		pass

	def Replicate(self):
		pass

def connectionInit():
	pass

def handlePortRequest(Socket: socket.SocketType):
	pass

class CommunicatorClass:
	def __init__(Self, Core: CompChatCore):
		MainLogger = projlogging.Logger("socket_communicator_main")

		# Create our SocketDistributor
		MainLogger.Log("Creating distributor.")
		Self.SocketDistributor = distributor.DistributorServer(Callback=handlePortRequest)
		Self.SocketDistributor.Start(Port=33826)

	def Stop(Self):
		Self.SocketDistributor.Stop()