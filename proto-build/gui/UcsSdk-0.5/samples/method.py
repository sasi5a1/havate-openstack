#!/usr/bin/python
from UcsSdk import *

# This script shows the use of UCS Manager methos "ConfigResolveClass" and "ConfigResolveDns"

if __name__ == "__main__":
	try:
		handle = UcsHandle()
		handle.Login("0.0.0.0","username","password")
	
		crDns = handle.ConfigResolveClass(ComputeBlade.ClassId(), inFilter=None, inHierarchical=YesOrNo.FALSE, dumpXml=None)
		if (crDns.errorCode == 0):
			for mo in crDns.OutConfigs.GetChild():
				print mo.Dn
				pass
		else:
			WriteUcsWarning('[Error]: configResolveDns [Code]:' + crDns.errorCode + ' [Description]:' + crDns.errorDescr)

		dnSet = DnSet()
		dn = Dn()
		dn.setattr("Value","org-root")
		dnSet.AddChild(dn)
		crDns = handle.ConfigResolveDns(dnSet)
		if (crDns.errorCode == 0):
			WriteObject(crDns.OutConfigs.GetChild())
		else:
			WriteUcsWarning('[Error]: configResolveDns [Code]:' + crDns.errorCode + ' [Description]:' + crDns.errorDescr)

		handle.Logout()

	except Exception, err:
		print "Exception:", str(err)
		import traceback, sys
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60
