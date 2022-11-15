# Class to be extended for the formatting of information
class Channel():
	def __init__(Self, ChannelId: int):
		Self.ChannelId = ChannelId
		Self.Members = [] # list of strings
		Self.Messages = []
	
	def MessagesToDict(Self):
		MessagesToDict = []
		for Message in Self.Messages:
			MessagesToDict.append(Message.__dict__)