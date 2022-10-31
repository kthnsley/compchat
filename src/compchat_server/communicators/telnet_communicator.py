# Declare Core type and import logging
from compchat_server.main import core as CompChatCore
from compchat_shared.utility import projlogging

class Communicator():
	Logger = projlogging.Logger("telnet_communicator_connection")

	def __init__(Self, Core: CompChatCore):
		pass

	def Check(Self):
		pass
	
	def Destroy(Self):
		pass

	def Replicate(self):
		pass

def init(Core: CompChatCore):
	Logger = projlogging.Logger("telnet_communicator_main")
	pass