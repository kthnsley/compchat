# Ensures standard format of info
import json

# fromJSON should be used unless if we are constructing a new message, and we know the new message is being made properly.
class Message():
	def __init__(Self, Channel: int, Data: dict):
		if type(Channel) != "int":
			raise

		if type(Data) != "dict":
			raise

		Self.Channel = Channel
		Self.Data = Data

	def ToJSON(Self):
		return json.dumps({
			"Channel": Self.Channel,
			"Data": Self.Data
		})


# Returns a success bool message string as a message object. 
# If not successful, second ret is error, third ret is raw error.
def fromJSON(Message: str) -> tuple[bool, Message | str]:
	try:
		Message = json.loads(Message)
		MessageObject = Message(Message.Channel, Message.Data)
		return True, MessageObject, None

	except Exception as Excp:
		return False, Excp