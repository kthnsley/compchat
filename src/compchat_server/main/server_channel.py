# WIP. Wrapper for Channel that provides our server functions (add a user, etc.)
from compchat_server.main import core as CompChatCore
from compchat_shared.utility import projlogging
from compchat_shared.structure import channel

class ServerChannelObject(channel.Channel):
	def __init__(Self, Core: CompChatCore, ChannelId: int):
		# init our parent class
		super().__init__(ChannelId)

		Self.Core = Core
		Self.Clients = []
		Self.Logger = projlogging.Logger(f"server_channel_{ChannelId}")

	def AddClient(Self, Client):
		if not (Client in Self.Clients):
			Self.Logger.Log("Client does not exist in channel. Adding to table.")
			Self.Clients.append(Client)

		if not (Client.SourceId in Self.Members):
			Self.Logger.Log("Member does not exist in channel. Adding to member table.")
			Self.Members.append(Client.SourceId)

		if len(Self.Clients) != len(Self.Members):
			Self.Logger.Log("Number of clients and members is not equal. Something is wrong.")

	# Only removes the Client object, should be used when cleaning up.
	def RemoveClient(Self, Client):
		try:
			Self.Clients.remove(Client)
		except Exception as Excp:
			Self.Logger.Log("Failed to remove a client from RemoveClient.", 3)
			Self.Logger.Log(f"Exception:\n {Excp}")

	def ToDict(Self):
		return {
			"ChannelId": Self.ChannelId,
			"Members": Self.Members,
			"Messages": Self.Messages
		}

# manager class
class ServerChannel():
	Logger = projlogging.Logger("server_channel")

	def __init__(Self, Core: CompChatCore):
		Self.CurrentChannels = {}
		Self.Core = Core

	def GetChannel(Self, ChannelId: int, Create=False):
		CurrentChannel = Self.CurrentChannels.get(ChannelId)
		if CurrentChannel == None:
			if Create:
				Self.Logger.Log(f"Could not find channel {ChannelId}, making it now.")
				CurrentChannel = ServerChannelObject(Self.Core, ChannelId)
				Self.CurrentChannels[ChannelId] = CurrentChannel
			else:
				Self.Logger.Log(f"Could not find channel {ChannelId}.")

		return CurrentChannel