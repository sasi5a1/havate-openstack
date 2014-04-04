#!/bin/bash

/root/staging.sh
ssh-keygen -R 192.168.241.240
ssh-keygen -R 192.168.241.230

virsh destroy staging
rm /var/lib/libvirt/images/staging.img
dd if=/dev/zero of=/var/lib/libvirt/images/staging.img bs=1G count=16
virsh create ~/staging.xml
count=0
until [ $(curl -s http://192.168.241.240/ubuntu/finished | grep up) ]; do echo "waiting... try ${count}" |& tee /tmp/test.log ; ((count++)); sleep 15 ; done

virsh destroy pxe
rm /var/lib/libvirt/images/pxe.img
dd if=/dev/zero of=/var/lib/libvirt/images/pxe.img bs=1G count=16
virsh create ~/pxe.xml
