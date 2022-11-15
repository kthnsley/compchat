import test_common
import compchat_shared.utility.projlogging as projlogging

projlogging.Logger.PrintVerbosity = 3

import compchat_client_cli.main as cli
cli.main()