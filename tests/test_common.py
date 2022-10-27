# Imports files from the src directory for testing
import sys
import os

RootDir = (os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
 
sys.path.insert(0, RootDir + "/src")