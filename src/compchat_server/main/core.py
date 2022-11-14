# Using dependency injection to pass functions that are needed from core to submodules
import importlib.util
import glob
import time

# Import our own submodules
from compchat_server.main import database, connection_manager, message_processor, server_channel
from compchat_shared.utility import projlogging
import compchat_server.communicators

class Core:
	def __init__(Self):
		# PHASE 0 LOADING
		Self.CoreLogger = projlogging.Logger("server_core")
		Self.Running = False

	def Start(Self):
		Self.CoreLogger.Log("Starting compchat server.", 4)
		Self.Running = True

		# PHASE 1 LOADING
		# Load DB
		Self.Database = database.Database()

		# Initialize our ServerChannel class
		Self.ServerChannel = server_channel.ServerChannel(Self)

		# PHASE 2 LOADING
		# Connection Manager, Message Processor
		Self.ConnectionManager = connection_manager.ConnectionManager(Self)
		Self.MessageProcessor = message_processor.MessageProcessor(Self)

		# PHASE 3 LOADING
		# Communicators
		Self.CommunicatorClasses = {}
		Self.CommunicatorConnectors = {}
		# Get all files in the Communicators directory with .py
		for ModulePath in (glob.glob(f"{compchat_server.communicators.__path__[0]}/*.py")):
			# Get file name
			ModuleName = ModulePath.split("/")[-1][:-3]

			# Don't load the packaging file
			if ModuleName != "__init__":
				Self.CoreLogger.Log(f"Importing and initing communicator {ModuleName}")

				# importlib magic to load the module
				CommunicatorModuleSpec = importlib.util.spec_from_file_location(ModuleName, ModulePath)
				CommunicatorModule = importlib.util.module_from_spec(CommunicatorModuleSpec)
				# exec module, running the code inside
				CommunicatorModuleSpec.loader.exec_module(CommunicatorModule)
				
				Self.CommunicatorClasses[ModuleName] = CommunicatorModule.CommunicatorClass()

				Self.CommunicatorConnectors[ModuleName] = CommunicatorModule.CommunicatorConnection

				# Call the start func to start the communicator
				Self.CommunicatorClasses[ModuleName].Start(Self)
				Self.CoreLogger.Log(f"Loaded Communicator module {ModuleName}")

	def Stop(Self):
		# Right now, simply call all the communicator stop functions
		for CommunicatorClass in Self.CommunicatorClasses.values():
			CommunicatorClass.Stop()

		Self.Running = False

if __name__ == "__main__":
	MainCore = Core()
	MainCore.Start()

	while MainCore.Running:
		time.sleep(0.5)