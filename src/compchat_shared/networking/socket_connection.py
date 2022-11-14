# Dumb wrapper for normal sockets to get and recv info
# Also implements encoding so we know to get everything as JSON and to actually allow packets to be split
import threading
import socket
import traceback

import compchat_shared.utility.projlogging as projlogging
Logger = projlogging.Logger("socket_connection")

# Default handler to notify when a socket_connection doesn't provide a function 
def defaultIncomingHandler(Data: str):
	Logger.Log("Default handler called. Did we not pass/set a IncomingHandler to our connection?", 4)
	Logger.Log(f"Data for unhandled call: {Data}")

class SocketConnection():
	# Startup function for a new socket connection
	def __init__(Self, Socket: socket.SocketType, IncomingHandler=defaultIncomingHandler):
		Logger.Log(f"Making new socket connection for IP {Socket.getsockname()}")
		Self.__Socket = Socket
		# TODO: Wait for alive before starting
		Self.__Alive = True

		# Start up a thread to handle incoming messages
		Self.IncomingHandler = IncomingHandler
		Self.__IncomingHandlerThread = threading.Thread(target=Self.__HandleIncoming, args=[Socket])
		Self.__IncomingHandlerThread.start()

	# Function to send data
	def Send(Self, Data: str):
		Logger.Log(f"Sending data: {Data}")
		Self.__Socket.sendall(Data.encode())
		pass

	def __HandleIncoming(Self, Socket: socket.SocketType):
		# TODO: Handle large data. Might just be doable with recv
		# TODO: Add check for when data was last recv, use check.
		# Chunks = []
		while True:
			try:
				# Recv 65536 bytes of data maximum. This is wasteful and ideally we'd want a buffer handler
				Data = Socket.recv(65536)
				if Data:
					#Chunks.append(Data)
					# Log incoming data
					Logger.Log(f"Incoming data: {Data}")
					try:
						# Convert data from bytes to string
						DecodedData = Data.decode()
						# Call the incoming handler to process the data
						Self.IncomingHandler(DecodedData)
					except Exception as Excp:
						Logger.Log(f"Bad data sent to our socket connection. {Data}", 2)
						Logger.Log(f"Exception Information: {traceback.format_exc()}")
			except Exception as Excp:
				pass
				# Disabled as we don't have a KeepAlive at the moment
				#Logger.Log(f"Error in __HandleIncoming__: {Excp}")

	# Check if communication is alive still
	def CheckAlive(Self, Socket: socket.SocketType) -> bool:
		Logger.Log("CALL RECV FOR STUB CheckAlive", 3)
		pass
	
	# Gracefully close the communication
	def Close():
		Logger.Log("CALL RECV FOR STUB Close", 3)
		pass