#!/bin/bash
path=$PWD

sed -e 's~^#\(d-i mirror/http/proxy string \)none~\1 http://192.168.26.170:8080~' -i $path/FinalCD/preseed/ubuntu-server.seed
sed -e 's/[vs]da/vda/' -i $path/FinalCD/preseed/ubuntu-server.seed
sed -e '/netcfg/d ' -i $path/FinalCD/preseed/ubuntu-server.seed

sed -e '/### Network/a # To pick a particular interface instead: \nd-i netcfg/choose_interface select eth0 \nd-i netcfg/disable_autoconfig boolean true \n# Static network configuration. \nd-i netcfg/get_nameservers string 192.168.26.186 \nd-i netcfg/get_ipaddress string 172.16.0.5 \nd-i netcfg/get_netmask string 255.255.255.0 \nd-i netcfg/get_gateway string 172.16.0.1 \nd-i netcfg/confirm_static boolean true \n# Any hostname and domain names assigned from dhcp take precedence over \nd-i netcfg/get_hostname string staging \nd-i netcfg/get_domain string libvirt.lab' -i $path/FinalCD/preseed/ubuntu-server.seed 

sed -e '/^# Example host profile/i #Add a PXE node \npxe:\n  hostname: "pxe.libvirt.lab"\n  power_address: "172.16.0.9"\n  interfaces:\n    eth0:\n      mac-address: "00:01:01:01:01:01"\n      dns-name: "pxe.libvirt.lab"\n      ip-address: "172.16.0.10"\n      static: "0"\n' -i $path/FinalCD/gui/onboot.sh

echo 'echo up > /var/www/finished' >> $path/FinalCD/gui/onboot.sh

$PWD/cd-iso-recreate.sh

cp $PWD/aio.iso /tmp/staging.iso
