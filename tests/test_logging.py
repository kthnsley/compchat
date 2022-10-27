import test_common
import compchat_shared.utility.projlogging as projlogger

Logger = projlogger.Logger("LoggingTest")
Logger.Log("TestLog1")
Logger.Log("TestLog2")
Logger.Log("TestCriticalLog", 1)