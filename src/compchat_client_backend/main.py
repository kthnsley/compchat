# This module should be the client backend. Likely isn't that large,
# just use shared libraries and such to connect to messages and make
# sockets to connect to.
from compchat_shared.networking import distributor, socket_connection
from compchat_shared.utility import projlogging
from compchat_shared.structure import message, channel

ClientBackendLogger = projlogging.Logger("compchat_client_backend")

# Establish our handler functions
def messageRecieve(Message):
	ClientBackendLogger.Log("Got a messageRecieve, but no handler added.", 3)
	print(Message)

class ClientBackend():
	def __init__(Self, OurClientId: int, TargetServer: tuple[str, str]):
		Self.OurChannels = {}
		Self.Id = OurClientId

		# Establish connection
		ClientBackendLogger.Log(f"Establishing connection. {TargetServer}")
		ClientConnectionSocket = distributor.getSocket(TargetServer[0], TargetServer[1])

		Self.Connection = socket_connection.SocketConnection(ClientConnectionSocket, Self.HandleIncoming)

		# """Authenticate"""
		ClientBackendLogger.Log(f"Logging identity {OurClientId}")
		Self.SendMessage(0, {"Action": "RegisterClient"})

	def CloseConnection(Self):
		pass

	# wrapper around the normal message sender
	def SendMessage(Self, TargetChannel: int, Data: dict):
		ThisMessage = message.Message(Self.Id, TargetChannel, Data)
		Self.Connection.Send(ThisMessage.ToJSON())

	# this is the client "ProcessMessage"
	def HandleIncoming(Self, Data: str):
		ClientBackendLogger.Log(f"Client {Self.Id} - Got message {Data}")

		_, ThisMessage = message.fromJSON(Data)