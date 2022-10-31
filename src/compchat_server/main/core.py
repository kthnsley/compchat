# Using dependency injection to pass functions that are needed from core to submodules
import importlib.util
import glob

# Import our own submodules
from compchat_server.main import database, client_manager, connection_manager, message_processor, server_channel
from compchat_shared.utility import projlogging
import compchat_server.communicators

class Core:
	def __init__(Self):
		# PHASE 0 LOADING
		Self.CoreLogger = projlogging.Logger("server_core")
		Self.CoreLogger.Log("Starting compchat server.", 4)

		# PHASE 1 LOADING
		# Load DB
		Core.Database = database.Database()

		# Initialize our ServerChannel class
		Core.ServerChannel = server_channel.ServerChannel

		# PHASE 2 LOADING
		# Connection Manager, Message Processor
		Core.ConnectionManager = connection_manager.ConnectionManager(Self)
		Core.MessageProcessor = message_processor.MessageProcessor(Self)

		# PHASE 3 LOADING
		# Client Manager
		Core.ClientManager = client_manager.ClientManager(Self)

		# PHASE 4 LOADING
		# Communicators
		CommunicatorModules = {}
		for ModulePath in (glob.glob(f"{compchat_server.communicators.__path__[0]}/*.py")):
			ModuleName = ModulePath.split("/")[-1][:-3]

			if ModuleName != "__init__":
				Self.CoreLogger.Log(f"Importing and initing communicator {ModuleName}")

				# importlib magic
				CommunicatorModuleSpec = importlib.util.spec_from_file_location(ModuleName, ModulePath)
				print(CommunicatorModuleSpec)
				CommunicatorModule = importlib.util.module_from_spec(CommunicatorModuleSpec)
				# exec module
				CommunicatorModuleSpec.loader.exec_module(CommunicatorModule)
				
				CommunicatorModules[ModuleName] = CommunicatorModule.Communicator
				# Call the init
				CommunicatorModule.init(Self)


if __name__ == "__main__":
	Core()