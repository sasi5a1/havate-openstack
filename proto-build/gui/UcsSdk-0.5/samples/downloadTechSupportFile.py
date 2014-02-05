#!/usr/bin/python
from UcsSdk import *

# This script downloads the Tech Support file from UCS Manager.
# Note : File extension must be ".tar".
# Please refer Quick Start Guide for other parameter sets.

if __name__ == "__main__":
	try:
		handle = UcsHandle()
		handle.Login("0.0.0.0", "username", "password")
		
		techSuppfilepath = r"C:\techsupp_ucsm.tar"
		handle.GetTechSupport(pathPattern= techSuppfilepath , ucsManager=True)

		handle.Logout()

	except Exception, err:
		handle.Logout()
		print "Exception:", str(err)
		import traceback, sys
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60

