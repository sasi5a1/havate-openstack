#!/usr/bin/python

from UcsSdk import *
import time

# This script monitor UCS Manager events of Managed Objects where in respective property of Managed object set to a specific value.

ucsm_ip = '10.105.219.23'
user = 'admin'
password = 'Tcs12345'

	
def calbak_SP_UsrLbl_ValueIsSuccess(mce):
	print 'Received Service Profile Event with classId: ' + str(mce.mo.classId)
	print 'New Value of Property USR_LBL: ' + mce.mo.UsrLbl
	print "ChangeList: ", mce.changeList
	print "EventId: ", mce.eventId	

try:
	handle = UcsHandle()
	handle.Login(ucsm_ip,user, password)

	SP = handle.GetManagedObject(None, LsServer.ClassId(), {LsServer.DN:"org-root/ls-ServiceProfileName"})
	
	# Add an event handle to catch the event triggered by "Change in Value of any of the specific Property of the respective Managed Object"
	# eg. Catch the event if specific property of Service Profile i.e. USR_LBL changes to "Success" 
	# NOTE: Once an event is received, event handle will be automatically removed.
	
	eventWatcher_MO_PropertyValue = handle.AddEventHandler(managedObject = SP[0], prop = NamingPropertyId.USR_LBL, successValue=["Success"], callBack=calbak_SP_UsrLbl_ValueIsSuccess)

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
