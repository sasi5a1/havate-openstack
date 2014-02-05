#!/usr/bin/python
from UcsSdk import *

# This script shows how to create and use the filter in UCS Manager method "ConfigResolveClass".

if __name__ == "__main__":
    try:
        handle = UcsHandle()
        handle.Login("0.0.0.0", "username", "password")
        
        inFilter = FilterFilter()
        
        andFilter0 = AndFilter()
        andFilter1 = AndFilter()
        
        eqFilter = EqFilter()
        eqFilter.Class = "lsServer"
        eqFilter.Property = "name"
        eqFilter.Value = "sp_name"
        andFilter1.AddChild(eqFilter)
        
        eqFilter = EqFilter()
        eqFilter.Class = "lsServer"
        eqFilter.Property = "type"
        eqFilter.Value = "instance"
        andFilter1.AddChild(eqFilter)
        
        wcardFilter = WcardFilter()
        wcardFilter.Class = "lsServer"
        wcardFilter.Property = "owner"
        wcardFilter.Value = "^[mM][aA][nN].*$"
        andFilter1.AddChild(wcardFilter)
        
        anybitFilter = AnybitFilter()
        anybitFilter.Class = "lsServer"
        anybitFilter.Property = "dn"
        anybitFilter.Value = "org-B"
        andFilter1.AddChild(anybitFilter)
        
        andFilter0.AddChild(andFilter1)
        inFilter.AddChild(andFilter0)
        
        crc = handle.ConfigResolveClass("lsServer", inFilter, YesOrNo.FALSE, YesOrNo.TRUE)
        WriteObject(crc)
        handle.Logout()

    except Exception, err:
        print "Exception:", str(err)
        import traceback, sys
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60

