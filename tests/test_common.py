# Imports files from the src directory for testing
import sys
import os

RootDir = (os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
 
sys.path.insert(0, RootDir + "/src")

import compchat_shared.utility.projlogging as projlogging

# Increase verbosity of logging to max
projlogging.Logger.FileVerbosity = 5
projlogging.Logger.PrintVerbosity = 5