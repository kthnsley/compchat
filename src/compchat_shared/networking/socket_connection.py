# Dumb wrapper for normal sockets to get and recv info
# Also implements encoding so we know to get everything as JSON and to actually allow packets to be split
import threading
import socket
import traceback

import compchat_shared.utility.projlogging as projlogging
Logger = projlogging.Logger("socket_connection")

def defaultIncomingHandler(Data: str):
	Logger.Log("Default handler called. Did we not pass/set a IncomingHandler to our connection?", 4)
	Logger.Log(f"Data for unhandled call: {Data}")

class SocketConnection():
	def __init__(Self, Socket: socket.SocketType, IncomingHandler=defaultIncomingHandler):
		Logger.Log(f"Making new socket connection for IP {Socket.getsockname()}")
		Self.__Socket = Socket
		# TODO: Wait for alive before starting
		Self.__Alive = True

		Self.IncomingHandler = IncomingHandler
		Self.__IncomingHandlerThread = threading.Thread(target=Self.__HandleIncoming__, args=[Socket])
		Self.__IncomingHandlerThread.start()

	def Send(Self, Data: dict) -> bool:
		Logger.Log(f"Sending data: {Data}")
		Self.__Socket.sendall(Data.encode())
		pass

	def __HandleIncoming__(Self, Socket: socket.SocketType):
		# TODO: Handle large data
		# TODO: Add check for when data was last recv, use check.
		# Chunks = []
		while True:
			try:
				Data = Socket.recv(2048)
				if Data:
					#Chunks.append(Data)
					Logger.Log(f"Incoming data: {Data}")
					#print("\n\n")
					try:
						DecodedData = Data.decode()
						Self.IncomingHandler(DecodedData)
					except Exception as Excp:
						Logger.Log(f"Bad data sent to our socket connection. {Data}", 2)
						Logger.Log(f"Exception Information: {traceback.format_exc()}")
			except Exception as Excp:
				pass
				# Disabled as we don't have a KeepAlive at the moment
				#Logger.Log(f"Error in __HandleIncoming__: {Excp}")

	def CheckAlive(Self, Socket: socket.SocketType) -> bool:
		Logger.Log("CALL RECV FOR STUB CheckAlive", 3)
		pass
	
	def Close():
		Logger.Log("CALL RECV FOR STUB Close", 3)
		pass