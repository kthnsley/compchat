# Take and create message classes based upon information given.
# Route these messages to the clients that need them
# Also create our system channel

from compchat_server.main import core as CompChatCore
from compchat_shared.utility import projlogging

class MessageProcessor():
	Logger = projlogging.Logger("message_processor")
	
	def __init__(Self, Core: CompChatCore):
		Self.Core = Core

	def ProcessMessage(Self, MessageString: str):
		# WIP
		print(MessageString)