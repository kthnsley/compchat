import test_common
import compchat_shared.networking.distributor as distributor
import socket
import threading

import time

def handleIncoming(Socket: socket.SocketType):
	while True:
		Data = Socket.recv(1024)
		print(Data)
		time.sleep(0.1)

def handleSending(Socket: socket.SocketType, SendData):
	Socket.sendall(SendData.encode())

def socketCallback(Socket: socket.SocketType):
	print("we have a socket, send a test to it")
	Socket.settimeout(3600)
	Duplicate = Socket.dup()
	ThreadOne = threading.Thread(target=handleIncoming, args=(Socket))
	ThreadTwo = threading.Thread(target=handleSending, args=(Duplicate))

	ThreadOne.run()
	ThreadTwo.run()
	print("checking if we are alive")
	while ThreadOne.is_alive() and ThreadTwo.is_alive():
		time.sleep(0.1)

	Socket.close()

SocketDistributorTest = distributor.DistributorServer("127.0.0.1", socketCallback)
SocketDistributorTest.Start()

time.sleep(1)

print("making client connections")

# get client connections
for _ in range(5):
	print("making client connection")
	time.sleep(0.1)
	print(f"GOT PORT: {distributor.getSocket()}")

print("stopping")
time.sleep(1)
SocketDistributorTest.Stop()