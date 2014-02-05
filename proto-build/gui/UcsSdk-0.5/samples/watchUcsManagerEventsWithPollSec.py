#!/usr/bin/python

from UcsSdk import *
import time

# This script monitors the UCS Manager events after every PollSec.

ucsm_ip = '0.0.0.0'
user = 'username'
password = 'password'

	
def calback_pollSec(mce):
	print 'Received Service Profile Event of classId: ' + str(mce.mo.classId)
	print 'Value of Property USR_LBL: ' + mce.mo.UsrLbl
	print "ChangeList: ", mce.changeList

try:
	handle = UcsHandle()
	handle.Login(ucsm_ip,user, password)

	SP = handle.GetManagedObject(None, LsServer.ClassId(), {LsServer.DN:"org-root/ls-ServiceProfileName"})
	
	# Add an event handle to catch the event triggered by "Change in Value of any of the specific Property of the respective Managed Object"
	# Using PollSec, will poll for specifc event after every pollSec.
	
	# NOTE: Once an event is received, event handle will be automatically removed.
	ev_pollSec= handle.AddEventHandler(managedObject = SP[0], prop = NamingPropertyId.USR_LBL, successValue=["Success"], pollSec=20, callBack=calback_pollSec)
	
	# loop that keeps the script running for us to get events/callbacks
	# User needs to manually exit the script here.
	while True:
		time.sleep(5)
	
	handle.Logout()

except Exception, err:
	print "Exception:", str(err)
	import traceback, sys
	print '-'*60
	traceback.print_exc(file=sys.stdout)
	print '-'*60
	handle.Logout()
