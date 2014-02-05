import sys
import xmlrpclib

cobbler_server='localhost'

# This function is to add a system to the given profile
def addSystem(name, profile_name, mac_address, ip_address):
	try:
		cobbler_user = 'cobbler'
		cobbler_password = ''
		print('addSystem name:%s profile:%s mac:%s ' % (name, profile_name, mac_address))
		cobbler_handle = xmlrpclib.Server("http://"+cobbler_server+"/cobbler_api")#"+cobbler_server+"/cobbler_api")
		ltoken = cobbler_handle.login(cobbler_user, cobbler_password)
		system_id = cobbler_handle.new_system(ltoken)
		cobbler_handle.modify_system(system_id, "name", name, ltoken)
		cobbler_handle.modify_system(system_id,'modify_interface', {
			"macaddress-eth0"	: mac_address,
			"ipaddress-eth0"	: ip_address,
			"dnsname-eth0"		: name}, ltoken)
		cobbler_handle.modify_system(system_id, 'kickstart', "/etc/cobbler/preseed/cisco-preseed.iso", ltoken);
		cobbler_handle.modify_system(system_id, "kopts", "netcfg/get_nameservers=10.1.1.1 netcfg/confirm_static=true netcfg/get_ipaddress={$eth0_ip-address} netcfg/get_gateway=10.1.1.1" 
					"netcfg/disable_autoconfig=true netcfg/dhcp_options=\'Configure network manually\' netcfg/no_default_route=true" 
					"partman-auto/disk=/dev/sda netcfg/get_netmask=255.255.255.0 netcfg/dhcp_failed=true", ltoken)

		cobbler_handle.modify_system(system_id, "profile", profile_name, ltoken)

		cobbler_handle.save_system(system_id, ltoken)
		cobbler_handle.sync(ltoken)
		print('Added/Updated system in cobbler')
	except Exception, err:
		print("4Exception:" + str(err))
	pass
pass


if __name__ == '__main__':
	addSystem('test_final', 'precise-x86_64', '11:22:33:44:55:66', '10.10.10.10')
