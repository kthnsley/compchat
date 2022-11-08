# Ensures standard format of info
import json
import traceback

import compchat_shared.utility.projlogging as projlogging

Logger = projlogging.Logger("message_class")

# fromJSON should be used unless if we are constructing a new message, and we know the new message is being made properly.
class Message():
	def __init__(Self, Channel: int, Data: dict):
		if type(Channel) != int:
			Logger.Log(f"Channel {Channel} was passed, which is not an int. Type is {type(Channel)}", 2)
			raise

		if type(Data) != dict:
			Logger.Log(f"Data {Data} was passed, which is not an dict. Type is {type(Data)}", 2)
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
def fromJSON(ThisMessageStr: str) -> tuple[bool, Message | str]:
	try:
		ThisMessage = json.loads(ThisMessageStr)
		MessageObject = Message(ThisMessage.get("Channel"), ThisMessage.get("Data"))
		return True, MessageObject

	except Exception as Excp:
		Logger.Log(f"Failed to convert message to JSON. {ThisMessageStr}", 3)
		Logger.Log(f"Exception: {traceback.format_exc()}")
		return False, Excp