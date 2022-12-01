import test_common

import time
import compchat_server.main.core as core

TestCore = core.Core()
TestCore.Start()
while TestCore.Running:
		time.sleep(0.5)