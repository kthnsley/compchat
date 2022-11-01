# Declare Core type and import logging
from compchat_server.main import core as CompChatCore
from compchat_shared.utility import projlogging

class CommunicatorConnection():
	Logger = projlogging.Logger("telnet_communicator_connection")

	def __init__(Self, Core: CompChatCore):
		pass

	def Check(Self):
		pass
	
	def Destroy(Self):
		pass

	def Replicate(self):
		pass

class CommunicatorClass:
	MainLogger = projlogging.Logger("telnet_communicator_main")

	def Start(Self, Core: CompChatCore):
		Self.Core = Core

	def Stop(Self):
		# May not be implemented, to be decided
		pass