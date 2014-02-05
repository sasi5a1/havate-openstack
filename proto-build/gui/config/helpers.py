import os
from django.conf import settings
from config.models import OpenstackSettings, NodeSettings
import subprocess

def construct_conf_file(config):
    base_conf_path = os.path.join(settings.PROJECT_PATH, 'static-raw', 'scripts', 'ucs_conf_template.conf.orig_base')
    conf_path = os.path.join(settings.PROJECT_PATH, 'static-raw', 'scripts', 'ucs_conf_template.conf')
    conf_text = ""
    mac_add = config.mac_pool
    mac_add_size = config.mac_pool_size
    pool_ip = config.kvm_ip_pool
    pool_ip_size = config.kvm_ip_pool_size
    server_qualifier_processed = False
    aio_node = None
    try:
        aio_node = NodeSettings.objects.get(aio=True)
    except NodeSettings.DoesNotExist, e:
        pass
    network_node = None
    try:
        network_node = NodeSettings.objects.get(network=True)
    except NodeSettings.DoesNotExist, e:
        pass
    compute_node_count = NodeSettings.objects.filter(compute=True).count()
    swift_node_count = NodeSettings.objects.filter(swift=True).count()
    cinder_node_count = NodeSettings.objects.filter(cinder=True).count()

    int_mac = int(mac_add.replace(':', ''), 16) + int(mac_add_size)
    new_mac_ar = []
    for x in range(6):
        new_mac_ar.append(int_mac%(16**((x+1)*2))/(16**(x*2)))
    new_mac = "%02X:%02X:%02X:%02X:%02X:%02X" % (new_mac_ar[5], new_mac_ar[4], new_mac_ar[3], new_mac_ar[2], new_mac_ar[1], new_mac_ar[0])

    ip_ar = pool_ip.split('.')
    int_pool = (int(ip_ar[0], 10)*(255**3) + int(ip_ar[1], 10)*(255**2)  + int(ip_ar[2], 10)*(255**1)  + int(ip_ar[3], 10)*(255**0)) + int(pool_ip_size)
    new_ip_ar = []
    for x in range(4):
        new_ip_ar.append(int_pool%(255**(x+1))/(255**x))
    new_pool = "%d.%d.%d.%d" % (new_ip_ar[3], new_ip_ar[2], new_ip_ar[1], new_ip_ar[0])
    print new_pool
    

    with open(base_conf_path, 'r') as content_file:
        for line in content_file:
            proc_line = line

            if line.lower().find('macpool') ==0 and line.lower().find('aio-nics') >=0:
                proc_line = "MacPool {{'Name':'aio-nics', 'From':'{0}', 'To':'{1}'}}\n".format(mac_add, new_mac)

            if line.lower().find('ippool') ==0 and line.lower().find('ext-mgmt') >=0:
                proc_line = "IpPool {{'Name':'ext-mgmt', 'From':'{0}', 'To':'{1}', 'DefGw':'{2}', 'PrimDns':'{3}', 'SecDns':'172.29.74.155', 'Subnet':'{4}'}}\n".format(pool_ip, new_pool, config.default_gateway, config.dns, config.subnet_mask)

            elif line.lower().find('vlan') ==0 and line.lower().find('mgmt') >=0:
                proc_line = "Vlan {{ 'Name':'Mgmt', 'SwitchId':'dual', 'Id': '{0}', 'Sharing':'none', 'DefaultNet':'no'}}\n".format(config.mgmt_vlan)

            elif line.lower().find('vlan') ==0 and line.lower().find('pxe') >=0:
                proc_line = "Vlan {{ 'Name':'Pxe', 'SwitchId':'dual', 'Id': '{0}', 'Sharing':'none', 'DefaultNet':'no'}}\n".format(config.pxe_vlan)

            elif line.lower().find('serverqualifier') == 0 and (line.lower().find('aio-pool') >=0 or line.lower().find('compute-pool') >=0):
                if not server_qualifier_processed:
                    try:
                        server_qualifier_processed = True
                        proc_line = "#" + line
                        proc_line = proc_line + "ServerQualifier {{'Name':'aio-pool', 'MinId':'{0}', 'MaxId':'{0}', 'SlotMinId':'{1}', 'SlotMaxId':'{1}'}}\n".format(aio_node.chassis_number, aio_node.blade_number)
                        for node in NodeSettings.objects.filter(compute=True):
                            proc_line = proc_line + "ServerQualifier {{'Name':'compute-pool', 'MinId':'{0}', 'MaxId':'{0}', 'SlotMinId':'{1}', 'SlotMaxId':'{1}'}}\n".format(node.chassis_number, node.blade_number)
                    except Exception, e:
                        pass
                else:
                    proc_line = "#" + line

            elif line.lower().find('serviceprofileinstance') ==0 and line.lower().find('compute-node') >=0:
                proc_line = "ServiceProfileInstance {{'SrcTempl':'compute-node', 'NamePrefix':'{0}', 'NumberOf':'{1}', 'TargetOrg':'org-root/org-Production'}}\n".format(config.hostname_prefix_compute_nodes, compute_node_count)
            conf_text = conf_text + proc_line

    config_file = open(conf_path, 'w')
    config_file.write(conf_text)
    config_file.close()
    script_path = os.path.join(settings.PROJECT_PATH, 'static-raw', 'scripts', 'ucs_integration.py')
    try:
        subprocess.call(['python', script_path , '-f', conf_path, '-i' , config.ucsm_hostname , '-u' , config.username , '-p', config.password])
    except Exception, e:
        print e
        print script_path
        pass
    pass

