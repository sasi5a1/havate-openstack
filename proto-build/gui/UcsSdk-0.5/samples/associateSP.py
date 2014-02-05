#!/usr/bin/python
from UcsSdk import *

# This script associates the  respective service profile with the respective blade server.
# Parameters:
# sp 		: Name of the service profile to associate
# bladeDn 	: Dn of the blade server with which to associate the serice profile.
#
# NOTE: Please make sure sp and bladeDn should exist in UCS Manager before executing script.

if __name__ == "__main__":
	try:
		handle = UcsHandle()
		handle.Login("0.0.0.0", "username", "password")

		sp = "sp_name"
		bladeDn = "sys/chassis-1/blade-1"

		handle.StartTransaction()
		orgObj = handle.GetManagedObject(None, OrgOrg.ClassId(), {OrgOrg.DN : "org-root"})
		lsServerObj = handle.GetManagedObject(orgObj, LsServer.ClassId(), {LsServer.NAME : sp})
		if not lsServerObj:
			print "Error: Service Profile <%s> Missing." %(sp)
			handle.Logout()
			sys.exit()
			
		lsServerObj = handle.SetManagedObject(lsServerObj, LsServer.ClassId(), {LsServer.STATUS : Status.MODIFIED})
		lsBindObj = handle.AddManagedObject(lsServerObj, LsBinding.ClassId(), {LsBinding.PN_DN : bladeDn, LsBinding.RESTRICT_MIGRATION: YesOrNo.NO}, YesOrNo.TRUE)
		handle.CompleteTransaction()

		handle.Logout()
	
	except SystemExit, e:
		sys.exit(e)

	except Exception, err:
		handle.Logout()
		print "Exception:", str(err)
		import traceback, sys
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60

