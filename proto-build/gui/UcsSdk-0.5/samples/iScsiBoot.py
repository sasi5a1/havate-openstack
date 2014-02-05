#!/usr/bin/python
from UcsSdk import *

# This script creates a service profile and configure it to boot from an iSCSI.

if __name__ == "__main__":

	try:
		handle = UcsHandle()

		handle.Login("0.0.0.0","username","password")

		handle.StartTransaction()

		getRsp = handle.GetManagedObject(None, None,{OrgOrg.DN:"org-root"})
		sp = handle.AddManagedObject(getRsp, LsServer.ClassId(), {LsServer.TYPE:"instance", LsServer.NAME:"sp_name"})
		vnic = handle.AddManagedObject(sp, VnicEther.ClassId(), {VnicEther.NAME:"enic1", VnicEther.SWITCH_ID:"A", VnicEther.ADDR:"00:00:00:22:22:27"})
		vlan611 = handle.AddManagedObject(vnic, VnicEtherIf.ClassId(), {VnicEtherIf.NAME:"vlan611", VnicEtherIf.DEFAULT_NET:"yes"})

		enic = handle.AddManagedObject(sp, VnicIScsi.ClassId(), {VnicIScsi.NAME:"iscsienic1", VnicIScsi.INITIATOR_NAME:"iqn.1995-05.com.broadcom.iscsiboot2", VnicIScsi.VNIC_NAME:"enic1"})
		vlan = handle.AddManagedObject(enic, VnicVlan.ClassId(), {VnicVlan.VLAN_NAME:"vlan611"})
		ipv4if = handle.AddManagedObject(vlan, VnicIPv4If.ClassId())
		ipv4iscsi = handle.AddManagedObject(ipv4if, VnicIPv4IscsiAddr.ClassId(), {VnicIPv4IscsiAddr.ADDR:"10.10.10.10"})

		primaryTarget = handle.AddManagedObject(vlan, VnicIScsiStaticTargetIf.ClassId(), {VnicIScsiStaticTargetIf.IP_ADDRESS:"10.10.10.11", VnicIScsiStaticTargetIf.NAME:"iqn.1992-08.com.netapp:sn.135037408", VnicIScsiStaticTargetIf.PRIORITY:"1"})
		primaryLun = handle.AddManagedObject(primaryTarget, VnicLun.ClassId(), {VnicLun.ID:"2"})

		bootPolicy = handle.AddManagedObject(sp, LsbootDef.ClassId())

		vmedia = handle.AddManagedObject(bootPolicy, LsbootVirtualMedia.ClassId(), {LsbootVirtualMedia.ACCESS:"read-only", LsbootVirtualMedia.ORDER:"1"})

		iscsiBoot = handle.AddManagedObject(bootPolicy, LsbootIScsi.ClassId(), {LsbootIScsi.ORDER:"2"})
		iscsiBootImagePath = handle.AddManagedObject(iscsiBoot, LsbootIScsiImagePath.ClassId(), {LsbootIScsiImagePath.TYPE:"primary", LsbootIScsiImagePath.I_S_C_S_I_VNIC_NAME:"iscsienic1"})

		handle.CompleteTransaction()

		handle.Logout()

	except Exception, err:
		print "Exception:", str(err)
		import traceback, sys
		print '-'*60
		traceback.print_exc(file=sys.stdout)
		print '-'*60
