# Create connections when specified, provide functions to wrap around using the messages to make
# outside modules not care about what communicator is being used when trying to send messages
# to and from.

# Declare Core type and import logging
from compchat_server.main import core as CompChatCore
from compchat_shared.utility import projlogging

class ConnectionManager():
	Logger = projlogging.Logger("connection_manager")

	def __init__(Self, Core: CompChatCore):
		pass

class __Connection():
	def __init__(Self, Core: CompChatCore, ConnectionManager: ConnectionManager):
		#Logger = projlogging.Logger("message_processor")
		pass