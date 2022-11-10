# Logging module, gives us a way to control verbosity and such.
"""
VERBOSITY LEVELS:
0 = None (silent)
1 = Critical
2 = Error
3 = Warning
4 = Info
5 = Debug
"""
import string
import tempfile
import time
import os

# Make sure default log dir exists, jank but fine
try:
	os.mkdir(f"{tempfile.gettempdir()}/comp3825-messager-logs/")
except:
	pass

InternalLogger = None

# Used internally to convert a number to the string
VerbosityStrings = ["NONE", "CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]

# Logger class, init this to get a logger (projlogging.Logger())
class Logger():
	LogPath = f"{tempfile.gettempdir()}/comp3825-messager-logs/{str(int(time.time()))}.log"
	FileVerbosity = 5
	PrintVerbosity = 1

	# Define source variable, and a custom log path if needed.
	def __init__(Self, Source="UNKNOWN SOURCE", LogPath=LogPath):
		Self.Source = Source
		Self.LogPath = LogPath
		if InternalLogger:
			InternalLogger.Log(f"Made logger for {Source} to {LogPath}")
		else:
			Self.Log(f"Made logger for {Source} to {LogPath}")

	# Main function, pass a string and optionally a verbosity so that its logged
	def Log(Self, Message: string, Verbosity=5):
		if Verbosity <= 0:
			return

		ThisLog = f"[{VerbosityStrings[Verbosity]}] [{Self.Source}]: {Message}"

		# Handle file verbosity
		if Verbosity <= Logger.FileVerbosity:
			OpenedLog = open(Self.LogPath, "a+")
			OpenedLog.write(f"{ThisLog}\n")

		# Handle printing verbosity
		# May want to make a way to let processes listen in on this later
		if Verbosity <= Logger.PrintVerbosity:
			print(ThisLog)

# Make our internal logger for logger log messages
InternalLogger = Logger("projlogging")