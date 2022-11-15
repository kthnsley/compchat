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

	def AddClient(Self, Client):
		if not (Client in Self.Clients):
			Self.Clients.append(Client)

		if not(Client.SourceId in Self.Members):
			Self.Members.append(Client.SourceId)

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