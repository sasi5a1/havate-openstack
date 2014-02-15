#!/bin/bash
set -x

if [ -d /etc/puppet/data ]; then 
  path_root=/etc/puppet
else
  path_root=/root/puppet_openstack_builder
fi

host_name=`hostname`
ipaddress=`ifconfig eth0 | grep 'inet ' | tr ':' ' ' | awk -F' ' '{print $3}'`
netmask=`ifconfig eth0 | grep 'inet ' | tr ':' ' ' | awk -F' ' '{print $7}'`
network=`ifconfig eth0 | grep 'inet ' | tr ':' ' ' | awk -F' ' '{print $5}' | awk -F'.' '{print $1 "." $2 "." $3 ".0"}'`
gateway=`netstat -r | grep 0.0.0.0 | awk -F' '  '{print $2}'`
dns_server=`cat /etc/resolv.conf | grep nameserver | head -1 | awk -F' ' '{print $2}'`
domain_name=`cat /etc/resolv.conf | grep search | head -1 | awk -F' ' '{print $2}'`
if [ -z ${domain_name} ] ; then
  domain_name='domain.name'
fi
mac_address=`ifconfig eth0 | grep HWaddr | awk -F' ' '{print $5}'`

cat > ${path_root}/data/scenarios/all_in_one.yaml <<EOF
#
# scenario for all_one
#
roles:
  all_in_one:
    classes:
      - cinder::setup_test_volume
      - openstack::swift::proxy
      - openstack::swift::storage-node
    class_groups:
      - build
      - controller
      - compute
      - network_controller
      - test_file
  compute:
    classes:
      - cinder::setup_test_volume
    class_groups:
      - compute
EOF

cat > ${path_root}/data/class_groups/build.yaml <<EOF
classes:
  - apache
  - apache::mod::proxy
  - apache::mod::wsgi
  - apache::mod::proxy_http
  - coi::profiles::cobbler_server
  - coi::profiles::cache_server
  - coi::profiles::puppet::master
EOF

cat >> ${path_root}/data/role_mappings.yaml <<EOF
${host_name}: all_in_one
EOF


cat > ${path_root}/data/hiera_data/hostname/${host_name}.yaml <<EOF
apache::purge_configs: false
puppet_master_address: "%{fqdn}"
cobbler_node_ip: "${ipaddress}"
node_subnet: "${network}"
node_netmask: "${netmask}"
node_gateway: "${gateway}"
admin_user: localadmin
password_crypted: '\$6\$UfgWxrIv\$k4KfzAEMqMg.fppmSOTd0usI4j6gfjs0962.JXsoJRWa5wMz8yQk4SfInn4.WZ3L/MCt5u.62tHDGB36EhiKF1'
autostart_puppet: true
ucsm_port: 443
install_drive: /dev/sda
ipv6_ra: 1
interface_bonding: 'true'
EOF

cat > ${path_root}/data/cobbler/cobbler.yaml <<EOF
preseed:
  repo: "http://openstack-repo.cisco.com/openstack/cisco havana main"

profile:
  name: "precise"
  arch: "x86_64"
  kopts: "log_port=514 \\
priority=critical \\
local=en_US \\
log_host=${ipaddress} \\
netcfg/choose_interface=auto"

node-global:
  profile: "precise-x86_64"
  netboot_enabled: "1"
  power_type: "ipmitool"
  power_user: "admin"
  power_pass: "password"
  kickstart: "/etc/cobbler/preseed/cisco-preseed.iso"
  kopts: "netcfg/get_nameservers=${dns_server} \\
netcfg/confirm_static=true \\
netcfg/get_ipaddress={\$eth0_ip-address} \\
netcfg/get_gateway=${gateway} \\
netcfg/disable_autoconfig=true \\
netcfg/dhcp_options=\\"Configure network manually\\" \\
netcfg/no_default_route=true \\
partman-auto/disk=/dev/sda \\
netcfg/get_netmask=${netmask} \\
netcfg/dhcp_failed=true"

# Example host profile
#${host_name}:
#  hostname: "${host_name}.${domain_name}" 
#  power_address: "${ipaddress}"
#  interfaces:
#    eth0:
#      mac-address: "${mac_address}"
#      dns-name: "${host_name}.${domain_name}"
#      ip-address: "${ipaddress}"
#      static: "0"
#
EOF

mkdir -p /etc/cobbler/preseed
cat >/etc/cobbler/preseed/cisco-preseed.iso <<EOF
d-i mirror/country string manual
d-i mirror/http/hostname string \$http_server
d-i mirror/http/directory string /ubuntu
d-i partman/early_command string vgs --separator=: --noheadings | cut -f1 -d: | while read vg ; do vgchange -an \$vg ; done ; pvs --separator=: --noheadings | cut -f1 -d: | while read pv ; do pvremove -ff -y \$pv ; done

### Partitioning
#d-i partman-auto/init_automatically_partition select biggest_free
#d-i partman/alignment string cylinder
d-i partman-auto/method string lvm
#d-i partman-auto/disk string /dev/sda
d-i partman-auto/purge_lvm_from_device boolean true
d-i partman-lvm/device_remove_lvm boolean true
d-i partman-md/device_remove_md boolean true
d-i partman-md/confirm boolean true
d-i partman-lvm/confirm_nooverwrite boolean true
d-i partman-lvm/confirm boolean true
d-i partman/confirm_write_new_label boolean true
d-i partman-auto/choose_recipe select atomic
d-i partman/default_filesystem string ext4
#d-i partman-auto-lvm/guided_size string max
d-i partman-partitioning/confirm_write_new_label boolean true
d-i partman/choose_partition select Finish partitioning and write changes to disk
d-i partman/choose_partition select Finish
d-i partman/confirm_nooverwrite boolean true
d-i partman/confirm boolean true


d-i clock-setup/utc boolean true

d-i time/zone string UTC
d-i passwd/user-fullname string Admin Adminson
d-i passwd/username string localadmin
d-i passwd/user-password-crypted password \$6\$UfgWxrIv\$k4KfzAEMqMg.fppmSOTd0usI4j6gfjs0962.JXsoJRWa5wMz8yQk4SfInn4.WZ3L/MCt5u.62tHDGB36EhiKF1
d-i user-setup/encrypt-home boolean false
d-i grub-installer/only_debian boolean true
d-i finish-install/reboot_in_progress note
d-i pkgsel/update-policy select none
d-i pkgsel/include string openssh-server puppet git acpid
d-i preseed/early_command string wget -O /dev/null http://\$http_server:\$http_port/cblr/svc/op/trig/mode/pre/system/\$system_name 
d-i preseed/late_command string \\
in-target /usr/bin/apt-get update;\\
sed -e 's/START=no/START=yes/' -i /target/etc/default/puppet ; \\
sed -e "/logdir/ a pluginsync=true" -i /target/etc/puppet/puppet.conf ; \\
sed -e "/logdir/ a server=$host_name.$domain_name" -i /target/etc/puppet/puppet.conf ; \\
in-target puppet agent --test --waitforcert 0 || true; \\
/sbin/lvremove -f cinder-volumes/hack; rmdir /tmp/hack ; \\
mkdir -p /target/var/www/ubuntu ; \\
wget -O /target/var/www/mirror.tar http://$http_server/mirror.tar ; \\
tar xf /target/var/www/mirror.tar -C /target/var/www/ubuntu ; \\
echo 'deb file:/var/www/ubuntu precise main' > /target/etc/apt/sources.list ; \\
in-target /usr/bin/apt-get update; \\
in-target cp /var/www/ubuntu/gui/onboot.sh /root/onboot.sh ; \\
in-target chmod +x /root/onboot.sh ; \\
in-target cp -R /var/www/ubuntu/puppet_openstack_builder /root/puppet_openstack_builder ; \\
in-target find /root -name '*sh' -exec chmod +x \\{} \\; \\
in-target cp -R /var/www/ubuntu/gui /gui ; \\
in-target find /gui -name '*sh' -exec chmod +x \\{} \\; \\
sed -e 's/\\(%sudo.*\\)ALL$/\1NOPASSWD: ALL/' -i /target/etc/sudoers ; \\
sed -e '/^exit 0/i /root/onboot.sh | tee /var/log/build_install.log' -i /target/etc/rc.local ; \\
wget -O /dev/null http://\$http_server:\$http_port/cblr/svc/op/nopxe/system/\$system_name ; \\
wget -O /dev/null http://\$http_server:\$http_port/cblr/svc/op/trig/mode/post/system/\$system_name ; \\
true
EOF

if [ -d /cdrom]; then
  cd /cdrom
  tar cf /var/www/cdrom.tar *
else
  cd /var/www/ubuntu
  tar xf /var/www/cdrom.tar
fi 

cobbler import --path=/cdrom --name=precise --arch=x86_64

if [ ! -d /etc/puppet/data ]; then
  cd /root/puppet_openstack_builder/install-scripts
  export scenario=all_in_one
  export vendor=cisco
  bash ./install.sh |& tee /var/log/openstack_install.log
fi

puppet apply -v /etc/puppet/manifests/site.pp |& tee /var/log/openstack_puppet.log

if [ $? == 0 ] ; then
  sed -e '/.*onboot.sh.*/d' -i /etc/rc.local
fi

# re-build the initrd to make sure the proper gpg key exists.
/gui/update_initrd.sh |& tee /var/log/update_initrd.log

cp /gui/openstack_installer/static-raw/scripts/iplist.yaml /etc/puppet/manifests/
chmod 775 /etc/puppet/manifests/iplist.yaml
chown root:www-data /etc/puppet/manifests/iplist.yaml
chmod 775 /etc/puppet/data/cobbler/cobbler.yaml
chown root:www-data /etc/puppet/data/cobbler/cobbler.yaml
chmod 775 /etc/puppet/data/role_mappings.yaml
chown root:www-data /etc/puppet/data/role_mappings.yaml
