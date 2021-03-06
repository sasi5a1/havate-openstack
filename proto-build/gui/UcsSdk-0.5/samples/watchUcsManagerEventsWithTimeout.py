#!/usr/bin/python

from UcsSdk import *
import time

# This script monitors UCS Manager events within a stipulated time<timeoutSec>

ucsm_ip = '0.0.0.0'
user = 'username'
password = 'password'

def callback_timeout(mce):
	print 'Received a New Event within a timeoutsec of ClassId:  ' + str(mce.mo.classId)
	print "ChangeList: ", mce.changeList
	print "EventId: ", mce.eventId

try:
	handle = UcsHandle()
	handle.Login(ucsm_ip,user, password)

	# Add an event handle "ev_all" to montitor the events generated by UCS for any of the ClassIds within in a stipulated Time <timeoutSec>.
	ev_all = handle.AddEventHandler(timeoutSec = 30, callBack = callback_timeout)
	
	# keep the script running for us to get events/callbacks
	time.sleep(60)
		
	handle.Logout()

except Exception, err:
	print "Exception:", str(err)
	import traceback, sys
	print '-'*60
	traceback.print_exc(file=sys.stdout)
	print '-'*60
	handle.Logout()
