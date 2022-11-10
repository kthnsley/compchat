# Ensures standard format of info
import json
import traceback

import compchat_shared.utility.projlogging as projlogging

Logger = projlogging.Logger("message_class")

# fromJSON should be used unless if we are constructing a new message, and we know the new message is being made properly.
class Message():
	# Create the message with the passed data
	def __init__(Self, SourceId: int, Channel: int, Data: dict):
		if type(SourceId) != int:
			Logger.Log(f"SourceId {SourceId} was passed, which is not an int. Type is {type(SourceId)}", 2)
			raise

		if type(Channel) != int:
			Logger.Log(f"Channel {Channel} was passed, which is not an int. Type is {type(Channel)}", 2)
			raise

		if type(Data) != dict:
			Logger.Log(f"Data {Data} was passed, which is not an dict. Type is {type(Data)}", 2)
			raise

		Self.SourceId = SourceId
		Self.Channel = Channel
		Self.Data = Data

	# Convert the message object to JSON
	def ToJSON(Self):
		return json.dumps({
			"SourceId": Self.SourceId,
			"Channel": Self.Channel,
			"Data": Self.Data
		})


# Returns a success bool message string as a message object. 
# If not successful, second ret is error, third ret is raw error.
def fromJSON(ThisMessageStr: str) -> tuple[bool, Message | str]:
	try:
		# Load JSON string to dict
		ThisMessage = json.loads(ThisMessageStr)
		# Get data
		MessageObject = Message(ThisMessage.get("SourceId"), ThisMessage.get("Channel"), ThisMessage.get("Data"))
		return True, MessageObject

	# If we error, log and report failure.
	except Exception as Excp:
		Logger.Log(f"Failed to convert message to JSON. {ThisMessageStr}", 3)
		Logger.Log(f"Exception: {traceback.format_exc()}")
		return False, Excp