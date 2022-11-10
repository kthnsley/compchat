# Create connections when specified, provide functions to wrap around using the messages to make
# outside modules not care about what communicator is being used when trying to send messages
# to and from.

# Declare Core type and import logging
from compchat_server.main import core as CompChatCore
from compchat_shared.utility import projlogging

# Main class. Doesn't actually have much to do, mainly just need a way to track user connections. Run keepalives,
# provide a way for other parts to send messages to clients.
class ConnectionManager():
	Logger = projlogging.Logger("connection_manager")

	def __init__(Self, Core: CompChatCore):
		pass

# Wrapper around the normal client
class __ServerClient():
	from compchat_shared.utility import projlogging
	Logger = projlogging.Logger("client_manager_server_client")

	def __init__(Self, Core: CompChatCore, UserId: int):
		Logger = projlogging.Logger(f"client_manager_server_client_{UserId}")
		pass