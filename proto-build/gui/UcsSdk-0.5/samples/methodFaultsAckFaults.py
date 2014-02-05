#!/usr/bin/python

import sys
import os
from UcsSdk import *

# This script acknowledge all the existing UCSM faults via UCS Manager method "FaultAckFaults".

ucsm_ip = '0.0.0.0'
user = 'username'
password = 'password'

try:
	handle = UcsHandle()
	handle.Login(ucsm_ip,user, password)

	idSet = IdSet()

	getRsp = handle.GetManagedObject(None, FaultInst.ClassId())
	for mo in getRsp:
		id = Id()
		id.Value = mo.Id
		idSet.AddChild(id)

	handle.FaultAckFaults(idSet)
	handle.Logout()

except Exception, err:
	print "Exception:", str(err)
	import traceback, sys
	print '-'*60
	traceback.print_exc(file=sys.stdout)
	print '-'*60

