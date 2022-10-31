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

VerbosityStrings = ["NONE", "CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]

class Logger():
	LogPath = f"{tempfile.gettempdir()}/comp3825-messager-logs/{str(int(time.time()))}.log"
	FileVerbosity = 5
	PrintVerbosity = 1

	def __init__(Self, Source="UNKNOWN SOURCE", LogPath=LogPath):
		Self.Source = Source
		Self.LogPath = LogPath
		if InternalLogger:
			InternalLogger.Log(f"Made logger for {Source} to {LogPath}")
		else:
			Self.Log(f"Made logger for {Source} to {LogPath}")

	# Main function
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

# DEBUG CODE, remove before done:
Logger.PrintVerbosity = 5