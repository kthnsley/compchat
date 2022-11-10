# Take and create message classes based upon information given.
# Route these messages to the clients that need them
# Also create our system channel

"""
{
	ClientId: 1234
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

# Main class for Core to initialize from
class MessageProcessor():
	Logger = projlogging.Logger("message_processor")
	
	def __init__(Self, Core: CompChatCore.Core):
		# Init function, only need to provide variables.
		Self.Core = Core

	# Take a message string, process it, perform system actions, handle replication.
	def ProcessMessage(Self, MessageString: str):
		Success, Message = message.fromJSON(MessageString)

		if not Success:
			Self.Logger.Log(f"Bad message string {MessageString} sent. Message not processed.", 3)
			Self.Logger.Log(f"Error message: {Message}")
			return

		# We now know this message was good externally

		# Make sure the SourceId is valid
		# 0 is a temporary testing SourceId, shouldn't be a real user.
		if Message.SourceId != 0:
			# add code to make sure this is an actual client that's connected here

			# also make sure that the client is properly connected
			pass

		try:
			# Handle system messages
			if Message.Channel == 0:
				if Message.Data.get("Action") == "TestMessage":
					Self.Logger.Log(f"TestMessage channel command sent: {Message.Data.get('Text')}", 4)
				else:
					Self.Logger.Log(f"Unhandled system message for action {Message.Data.get('Action')}", 2)
			else:
				Self.Logger.Log("Handling for non-system messages is not implemented.", 3)
				Self.Logger.Log(f"Message data: {Message.Data}")
		except Exception as Excp:
			Self.Logger.Log(f"Failed to handle message {Message.Data} for channel {Message.Channel}.", 3)
			Self.Logger.Log(f"Exception: {traceback.format_exc()}")

		