# Declare Core type and import logging
from compchat_server.main import core as CompChatCore
from compchat_shared.utility import projlogging

class CommunicatorConnection():
	Logger = projlogging.Logger("telnet_communicator_connection")

	def __init__(Self, Core: CompChatCore):
		pass

	def Check(Self) -> bool:
		# Report back a bool if the connection is alive or not
		# This is optional for now
		return True
	
	def Destroy(Self):
		# Close the connection gracefully
		pass

	def Replicate(self):
		# Send a message to the client
		pass

class CommunicatorClass:
	MainLogger = projlogging.Logger("telnet_communicator_main")

	# Basically start up our "server" for the connection
	def Start(Self, Core: CompChatCore):
		Self.Core = Core

	# Define how we stop our "server," basically just cleanup
	def Stop(Self):
		# May not be implemented, to be decided
		pass