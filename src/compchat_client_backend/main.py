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
		Self.SendMessage(0, {"Action": "ClientDisconnect"})
		
		Self.Connection.Close()

	# wrapper around the normal message sender
	def SendMessage(Self, TargetChannel: int, Data: dict):
		ThisMessage = message.Message(Self.Id, TargetChannel, Data)
		Self.Connection.Send(ThisMessage.ToJSON())

	# this is the client "ProcessMessage"
	def HandleIncoming(Self, Data: str):
		#ClientBackendLogger.Log(f"Client {Self.Id} - Got message {Data}")

		_, ThisMessage = message.fromJSON(Data)

		# tmp but functional, only thing server -> client is the messaging
		if ThisMessage.Channel == 0:
			TargetAction = ThisMessage.Data.get("Action")
			if TargetAction == "ReplicateChannelList":
				# unpack channels
				ClientBackendLogger.Log(f"Client {Self.Id} - Unpacking channel list")
				for Channel in ThisMessage.Data.get("Channels"):
					NewChannel = channel.Channel(Channel.ChannelId)
					NewChannel.Members = Channel.Members
					NewChannel.Messages = Channel.Messages
					Self.OurChannels[Channel.ChannelId] = NewChannel
			elif TargetAction == "ReplicateChannel":
				# jank, but we don't update messages with ReplicateChannel if the channel already
				# exists
				NewData = ThisMessage.Data.get("Channel")
				CurrentChannel = Self.OurChannels.get(NewData.get("ChannelId"))
				if CurrentChannel != None:
					ClientBackendLogger.Log(f"Client {Self.Id} - Updating channel member list")
					CurrentChannel.Members = NewData.get("Members")
				else:
					ClientBackendLogger.Log(f"Client {Self.Id} - Responding to get of new channel. New channel ID is {NewData.get('ChannelId')}")
					NewChannel = channel.Channel(NewData.get("ChannelId"))
					NewChannel.Members = NewData.get("Members")
					NewChannel.Messages = NewData.get("Messages")
					Self.OurChannels[NewData.get("ChannelId")] = NewChannel

		else:
			TargetChannel = Self.OurChannels[ThisMessage.Channel]
			# In the future, add some event based handler here.
			TargetChannel.Messages.append({
				"SourceId": ThisMessage.SourceId,
				"Text": ThisMessage.Data.get("Text")
			})