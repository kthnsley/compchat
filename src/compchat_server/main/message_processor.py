# Take and create message classes based upon information given.
# Route these messages to the clients that need them
# Also create our system channel

"""
{
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

class MessageProcessor():
	Logger = projlogging.Logger("message_processor")
	
	def __init__(Self, Core: CompChatCore):
		Self.Core = Core

	def ProcessMessage(Self, MessageString: str):
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
				else:
					Self.Logger.Log(f"Unhandled system message for action {Message.Data.get('Action')}", 2)
			else:
				Self.Logger.Log("Handling for non-system messages is not implemented.", 3)
				Self.Logger.Log(f"Message data: {Message.Data}")
		except Exception as Excp:
			Self.Logger.Log(f"Failed to handle message {Message.Data} for channel {Message.Channel}.", 3)
			Self.Logger.Log(f"Exception: {traceback.format_exc()}")

		