# Take and create message classes based upon information given.
# Route these messages to the clients that need them
# Also create our system channel

"""
{
	SourceId: 1234 # client -> server only
	Channel: 0
	Data: {
		Action: string, ("TestMessage")
		Text = "something"
	}
}
"""
import traceback

from compchat_server.main import core as CompChatCore
from compchat_shared.utility import projlogging
from compchat_shared.structure import message

import socket

# Main class for Core to initialize from
class MessageProcessor():
	Logger = projlogging.Logger("message_processor")
	
	def __init__(Self, Core: CompChatCore):
		# Init function, only need to provide variables.
		Self.Core = Core

	# Take a message string, process it, perform system actions, handle replication.
	def ProcessMessage(Self, MessageString: str, CommunicatorConnection):
		Success, Message = message.fromJSON(MessageString)

		if not Success:
			Self.Logger.Log(f"Bad message string {MessageString} sent. Message not processed.", 3)
			Self.Logger.Log(f"Error message: {Message}")
			return

		# We now know this message was good externally

		try:
			# Handle system messages
			if Message.Channel == 0:
				if Message.Data.get("Action") == "TestMessage":
					Self.Logger.Log(f"TestMessage channel command sent: {Message.Data.get('Text')}", 4)
					return

				if Message.Data.get("Action") == "RegisterClient":
					# Register this client
					Self.Logger.Log(f"Registering client for id {Message.SourceId}")
					Self.Core.ConnectionManager.AddConnection(CommunicatorConnection, Message.SourceId)
					
					ThisClientObject = Self.Core.ConnectionManager.GetClientById(Message.SourceId)
					# Construct the list of dicts
					ListOfChannels = {}
					for Channel in ThisClientObject.ClientChannels:
						ListOfChannels[Channel.ChannelId] = Channel.ToDict()

					# Send this client the channels they are in
					ThisClientObject.Replicate(message.Message(
						0,
						0,
						{
							"Action": "ReplicateChannelList",
							"Channels": ListOfChannels
						}
					))

					Self.Logger.Log(f"Registering client finished. Client Connections:")
					Self.Logger.Log(f"{len(Self.Core.ConnectionManager.GetClientConnectionsById(Message.SourceId))}")
					return

				# If we are at this point, this should be a real client.
				ThisClientObject = None
				try:
					ThisClientObject = Self.Core.ConnectionManager.GetClientById(Message.SourceId)
				except:
					Self.Logger.Log(f"Got SourceId {ThisClientObject}, but client not found.")

				if Message.Data.get("Action") == "GetChannel":
					RequestedChannelId = Message.Data.get("ChannelId")
					# log
					Self.Logger.Log(f"Client {Message.SourceId} is requesting to join channel {RequestedChannelId}.")

					RequestedChannel = Self.Core.ServerChannel.GetChannel(RequestedChannelId, True)
					RequestedChannel.AddClient(ThisClientObject)
					
					if not (RequestedChannel in ThisClientObject.ClientChannels):
						ThisClientObject.ClientChannels.append(RequestedChannel)

					# Now update all other clients
					for Client in RequestedChannel.Clients:
						Client.Replicate(message.Message(
						0,
						0,
						{
							"Action": "ReplicateChannel",
							"Channel": RequestedChannel.ToDict()
						}
					))

					return
				elif Message.Data.get("Action") == "ClientDisconnect":
					Self.Core.ConnectionManager.RemoveConnection(CommunicatorConnection, Message.SourceId)
					
				else:
					Self.Logger.Log(f"Unhandled system message for action {Message.Data.get('Action')}", 2)
			else:
				# Get the channel we are sending the message to
				TargetChannel = Self.Core.ServerChannel.GetChannel(Message.Channel)
				if not TargetChannel:
					Self.Logger.Log(f"Bad channel sent with message {Message.Channel}")
					return

				TargetChannel.Messages.append({
					"SourceId": Message.SourceId,
					"Text": Message.Data.get("Text")
				})

				# Replicate the message to everyone including the sending client
				for Client in TargetChannel.Clients:
					Client.Replicate(Message)

		except Exception as Excp:
			Self.Logger.Log(f"Failed to handle message {Message.Data} for channel {Message.Channel}.", 3)
			Self.Logger.Log(f"Exception: {traceback.format_exc()}")

		