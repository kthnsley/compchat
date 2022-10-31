# Manage clients, make a client class, hold connections and such

# Declare Core type
from compchat_server.main import core as CompChatCore
from compchat_shared.utility import projlogging

class ClientManager():
	Logger = projlogging.Logger("client_manager")

	def __init__(Self, Core: CompChatCore):
		pass

class __ServerClient():
	from compchat_shared.utility import projlogging
	Logger = projlogging.Logger("client_manager_server_client")

	def __init__(Self, Core: CompChatCore, ClientManager: ClientManager, UserId: int):
		Logger = projlogging.Logger(f"client_manager_server_client_{UserId}")
		pass