# Dumb wrapper for normal sockets to get and recv info
# Also implements encoding so we know to get everything as JSON and to actually allow packets to be split
import threading
import socket

class SocketConnection():
	def __init__(Self, Socket: socket.SocketType):
		Self.__Socket = Socket
		Self.__Alive = True

	def Send(Self, Socket: socket.SocketType) -> bool:
		pass

	def __HandleIncoming__(Self, Socket: socket.SocketType):
		# TODO: Handle large data
		# Chunks = []
		while True:
			Data = Socket.recv(2048)
			if Data:
				Chunks.append(Data)
				print(Data)
				print("\n\n")

	def CheckAlive(Self, Socket: socket.SocketType) -> bool:
		pass

	