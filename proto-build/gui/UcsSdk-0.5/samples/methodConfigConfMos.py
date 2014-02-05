#!/usr/bin/python

import sys
import os
from UcsSdk import *

# This script shows the use of UCS Manager method "ConfigConfMos"

ucsm_ip = '0.0.0.0'
user = 'username'
password = 'password'

try:
	handle = UcsHandle()
	handle.Login(ucsm_ip,user, password)

	obj = LsServer()
	obj.setattr(LsServer.DN, "org-root/ls-new_sp")
	obj.setattr(LsServer.NAME, "new_sp")
	obj.setattr(LsServer.STATUS, Status.CREATED)

	pair = Pair()
	pair.Key = obj.Dn
	pair.AddChild(obj)

	configMap = ConfigMap()
	configMap.AddChild(pair)

	ccm = handle.ConfigConfMos(configMap)
	if ccm.errorCode == 0:
		moList = []
		for child in ccm.OutConfigs.GetChild():
			if (isinstance(child, Pair) == True):
				for mo in child.GetChild():
					moList.append(mo)
			elif (isinstance(child, ManagedObject) == True):
				moList.append(child)
		WriteObject(moList)
	else:
		WriteUcsWarning('[Error]: [Code]:' + ccm.errorCode + ' [Description]:' + ccm.errorDescr)

	handle.Logout()

except Exception, err:
	print "Exception:", str(err)
	import traceback, sys
	print '-'*60
	traceback.print_exc(file=sys.stdout)
	print '-'*60

