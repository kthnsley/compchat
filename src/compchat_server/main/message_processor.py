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
				if Message.Data.get("Action") == "RegisterClient":
					ThisSourceId = Message.SourceId

					# Register this client
					Self.Logger.Log(f"Registering client for id {ThisSourceId}")
					Self.Core.ConnectionManager.AddConnection(CommunicatorConnection, ThisSourceId)
					
					# Send this client the channels they are in
					ThisClientObject = Self.Core.ConnectionManager.GetClientById(ThisSourceId)
					ThisClientObject.Replicate(message.Message(
						0,
						0,
						{
							"Action": "ReplicateChannelList",
							"Channels": ThisClientObject.ClientChannels
						}
					))

					Self.Logger.Log(f"Registering client finished. Client Connections:")
					Self.Logger.Log(f"{Self.Core.ConnectionManager.GetClientConnectionsById(ThisSourceId)}")

				else:
					Self.Logger.Log(f"Unhandled system message for action {Message.Data.get('Action')}", 2)
			else:
				Self.Logger.Log("Handling for non-system messages is not implemented.", 3)
				Self.Logger.Log(f"Message data: {Message.Data}")
		except Exception as Excp:
			Self.Logger.Log(f"Failed to handle message {Message.Data} for channel {Message.Channel}.", 3)
			Self.Logger.Log(f"Exception: {traceback.format_exc()}")

		