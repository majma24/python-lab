#!/usr/bin/env python
#----------------------------------------------------------------------------------------#
#                                                                                        #
# Use sys to write a script that prints command line only when run from the command line.#
#----------------------------------------------------------------------------------------#

import os
import sys
import getopt
cmd_argument = sys.argv
command = cmd_argument[1:]
print (command)
print(f"OS Platform version is ", sys.platform)
    

