#!/bin/bash

#mkdir initrd
#cd initrd
#gunzip -c /cdrom/install/netboot/ubuntu-installer/amd64/initrd.gz | cpio -imvd --no-absolute-filenames
#cp /usr/share/keyrings/ubuntu-archive-keyring.gpg ./usr/share/keyrings/ubuntu-archive-keyring.gpg
#find . | cpio --quiet --dereference -o -H newc | gzip -9c - > /var/www/cobbler/ks_mirror/precise-x86_64/initrd.gz
#cd ..
#rm -rf initrd

if [ ! -d /var/www/cobbler/ks_mirror/precise-x86_64/ ] ; then
  mkdir -p /var/www/cobbler/ks_mirror/precise-x86_64/
fi

cp /cdrom/install/netboot/ubuntu-installer/amd64/{initrd.gz,linux} /var/www/cobbler/ks_mirror/precise-x86_64/
/usr/sbin/cobbler_sync.py

