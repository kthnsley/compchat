# Just for fun, dumb JSON implementation of persistent message storage.

import json
import os

from compchat_shared.utility import projlogging

# Main database class
class Database():
	# Startup function
	def __init__(Self, DatabasePath: str = "/tmp/compchat-db.json"):
		# Make our logger
		Self.DatabaseLogger = projlogging.Logger("server_database")

		# Do path stuff to make sure the path exists, and make the file
		DatabasePathRootSplit = DatabasePath.split("/")
		DatabasePathRoot = "/".join(DatabasePathRootSplit[:len(DatabasePathRootSplit) - 1])

		if not os.path.exists(DatabasePathRoot):
			Self.DatabaseLogger.Log("Path to DatabasePath doesn't exist! Erroring.", 1)
			Self.DatabaseLogger.Log(f"Target path: {DatabasePathRoot}")
			raise FileNotFoundError

		# read database so we can modify it
		Self.DatabasePath = DatabasePath

		# If the database file already exists, load it.
		if os.path.exists(DatabasePath):
			try:
				DatabaseFile = open(DatabasePath, "r")
				Self.Data = json.load(DatabaseFile)
				DatabaseFile.close()
			except:
				Self.DatabaseLogger.Log("Failed to load JSON, but file exists. Erroring.", 1)
				raise
			
		# If the database file doesn't exist, make a new one.
		else:
			Self.DatabaseLogger.Log("No database information found. Writing new DB.", 3)
			Self.Data = {
				"Clients": {},
				"Channels": {},
			}
			# Write a new database file
			Self.__Write()

	def __Write(Self):
		# Write to database, simply open file, write text, close file.
		Self.DatabaseLogger.Log("Writing to database.")
		Self.DatabaseLogger.Log(str(Self.Data), 5)
		DatabaseFile = open(Self.DatabasePath, "w")
		json.dump(Self.Data, DatabaseFile)
		DatabaseFile.close()
	
	# channel info
	def GetChannelInfo(Self):
		pass

	def WriteChannelInfo(Self):
		pass

	# channel messages
	def GetChannelMessages(Self):
		pass

	def AppendChannelMessages(Self):
		pass
	
	# client info
	def GetClientInfo(Self):
		pass

	def AddClientInfo(Self):
		pass