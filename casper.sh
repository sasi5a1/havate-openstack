#!/bin/bash

cd FinalCD/casper
unsquashfs filesystem.squashfs
cp /etc/resolv.conf squashfs-root/etc/
cp /etc/hosts squashfs-root/etc/
mount --bind /dev/ squashfs-root/dev
chroot squashfs-root <<EOF
mount -t proc none /proc
mount -t sysfs none /sys
mount -t devpts none /dev/pts
export HOME=/root
export LC_ALL=C
dbus-uuidgen > /var/lib/dbus/machine-id
dpkg-divert --local --rename --add /sbin/initctl
ln -s /bin/true /sbin/initctl
echo 'deb http://localhost/ubuntu precise main' > /etc/apt/sources.list
apt-get install ubuntu-keyring -y
apt-get install cobbler puppet git -y --force-yes

git clone https://github.com/CiscoSystems/puppet_openstack_builder -b havana /root/puppet_openstack_builder
cd /root/puppet_openstack_builder/install-scritps
./install.sh

apt-get clean
rm -rf /tmp/* ~/.bash_history
rm /etc/hosts
rm /etc/resolv.conf
rm /var/lib/dbus/machine-id
rm /sbin/initctl
dpkg-divert --rename --remove /sbin/initctl

umount /proc || umount -lf /proc
umount /sys
umount /dev/pts
exit
EOF
umount squashfs-root/dev
chmod +w filesystem.manifest
chroot squashfs-root dpkg-query -W --showformat='${Package} ${Version}\n' > filesystem.manifest
cp filesystem.manifest{,-desktop}
sed -i '/ubiquity/d' filesystem.manifest-desktop
sed -i '/casper/d' filesystem.manifest-desktop
rm filesystem.squashfs
mksquashfs squashfs-root/ filesystem.squashfs -comp lzo
printf $(sudo du -sx --block-size=1 squashfs-root | cut -f1) > filesystem.size
um.txt
find -type f -print0 | sudo xargs -0 md5sum | grep -v isolinux/boot.cat | sudo tee md5sum.txt
