# This CLI client will be the reference implementation.
import argparse
import random

import compchat_client_backend.main as client_backend

# info that we need: OurClientId, TargetIp, TargetPort
def getParser():
	Parser = argparse.ArgumentParser()
	Parser.add_argument("--id", help="The client ID that we will use for our session.", default=random.randint(1, 999999999))
	Parser.add_argument("--ip", help="The target-ip that we will connect to.", default="localhost")
	Parser.add_argument("--port", help="The port that we will connect to.", default="33826")
	Parser.add_argument("--verbosity", help="Verbosity level of the code", default="2")
	return Parser

def help():
	print("""Usage:
help - Display this message
sendmessage [channel id] [message] - Send a message to the specified channel, that you are a member of.
showmessages [channel id] - Show the messages in a channel
getchannel [channel id] - Join and become a member of the channel
listchannels - Print the list of all channels you are a member of
exit - Cleanly exit and disconnect from the server""")

def main():
	Arguments = getParser().parse_args()
	Session = client_backend.ClientBackend(int(Arguments.id), (Arguments.ip, Arguments.port))
	print("Welcome! Type help to get a list of commands!")
	while True:
		UserInput = input("> ")
		UserInputSplit = UserInput.split(" ")

		# jank but quick and good enough ;tm;
		try:
			if UserInputSplit[0] == "sendmessage":
				TargetChannel = int(UserInputSplit[1])
				Session.SendMessage(TargetChannel, {"Text": " ".join(UserInputSplit[2:])})

			elif UserInputSplit[0] == "showmessages":
				TargetChannel = Session.OurChannels[int(UserInputSplit[1])]
				for Message in TargetChannel.Messages:
					print(f"FROM {Message.get('SourceId')} : {Message.get('Text')}")
				
			elif UserInputSplit[0] == "getchannel":
				TargetChannel = int(UserInputSplit[1])
				Session.SendMessage(0, {"Action": "GetChannel", "ChannelId": TargetChannel})

			elif UserInputSplit[0] == "listchannels":
				for Channel, Info in Session.OurChannels.items():
					print(f"{Channel} - Members: [{Info.Members}]")

			elif UserInputSplit[0] == "exit":
				Session.CloseConnection()	
				break

			else:
				help()
		except Exception as Excp:
			print(Excp)
			help()