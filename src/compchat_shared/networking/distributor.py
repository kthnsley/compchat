# This module is responsible for creating a socket that our processes can listen to to get a socket to use.
# This can be used for either local connections or remote connections.
# Port 33825 is the default socket_distributor port. socket_communicator uses 33826.
# Server uses 33825 for the shutdown scripts

# Possible todo: 
# Make an anti-abuse that prevents denial of service by spamming the socket

import socket
import compchat_shared.utility.projlogging as projlogging
import threading
import time

Logger = projlogging.Logger("socket_distributor")

def defaultCallback(Socket: socket.SocketType):
	Logger.Log("Default callback called. Did we not pass a Callback to DistributorServer?")

# Takes a callback function and server address. Adds a .start and .stop can be called to start and stop the server.
class DistributorServer:
	# We have to do this to prevent GC from closing our sockets.
	ActiveSockets = []

	def __init__(Self, Host="0.0.0.0", Callback=defaultCallback):
		Self.__Host = Host # where we listen to
		Self.__Status = "STOPPED" # Valid statuses are "AVAILABLE", "STOPPED"
		Self.__Socket: socket.SocketType = None
		Self.__Callback = Callback
		Self.__HandlerThread: threading.Thread = None

	def Start(Self, Port=33825):
		if Self.__Status == "AVAILABLE":
			Logger.Log("Failing attempt to start already running Socket Distributor", 3)
			return

		Logger.Log(f"Starting SocketDistributor for {Port}")

		Self.__Status = "AVAILABLE"
		Self.__Socket = socket.create_server((Self.__Host, Port), backlog=9)
		Self.__Port = Port
		Self.__HandlerThread = threading.Thread(target=Self.__HandleIncomingConnections)
		Self.__HandlerThread.start()

	def Stop(Self):
		if Self.__Status == "STOPPED":
			Logger.Log("Failing attempt to stop already stopped Socket Distributor", 3)
			return
		
		Logger.Log(f"Stopping SocketDistributor for {Self.__Socket.getsockname()}")

		Self.__Status = "STOPPED"

		# Connect to ourself to stop thread
		TerminateThread = socket.create_connection(("127.0.0.1", Self.__Port))
		time.sleep(1)
		TerminateThread.close()

		#Self.__Socket.close()

	def __CreateListener(Self, Socket: socket.SocketType):
		# Do this to work around weird behavior
		AvailablePortSock = socket.socket()
		AvailablePortSock.bind((Self.__Host, 0))
		AvailablePort = AvailablePortSock.getsockname()[1]
		AvailablePortSock.close()

		# Make our real server
		NewSocket = socket.create_server((Self.__Host, AvailablePort), backlog=9)
		
		Socket.sendall(str(AvailablePort).encode())
	
		Logger.Log(f"Sent port {AvailablePort} to client.")

		# Wait for client connection
		# POSSIBLE TODO: This is prone to DDoS by just spamming and never actually connecting, probably.
		NewSocket.listen(9)
		NewSocket, _ = NewSocket.accept()
		# POSSIBLE TODO: Make sure addresses line up, doesn't matter as much as above though

		threading.Thread(target=Self.__Callback, args=[NewSocket]).start()

		Self.ActiveSockets.append(NewSocket)

		Socket.close()

	def __HandleIncomingConnections(Self):
		Logger.Log(f"Socket preparing to handle connections")
		Self.__Socket.listen()
		while Self.__Status == "AVAILABLE":
			Socket, Address = Self.__Socket.accept()
			Logger.Log(f"Got connection from {Address} for listener running at {Self.__Socket.getsockname()}")

			if Self.__Status != "AVAILABLE":
				return

			CreateListenerThread = threading.Thread(target=Self.__CreateListener, args=[Socket])
			CreateListenerThread.start()

# Helper that provides one function to make code cleaner
def getSocket(Host="127.0.0.1", Port=33825) -> socket.SocketType:
	GetSocket = socket.create_connection((Host, Port))
	while True:
		Data = GetSocket.recv(16)
		if Data:
			try:
				Data = int(Data)
				break
			except:
				pass

	# We have our port
	Logger.Log(f"Attempting connection from getSocket call to {Host, Data}")
	NewSocket = socket.create_connection((Host, Data), timeout=10)
	# Return new socket
	return NewSocket
