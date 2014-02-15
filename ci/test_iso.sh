#!/bin/bash
set -x

/root/staging.sh

virsh destroy staging
virsh undefine staging
rm /var/lib/libvirt/images/staging.img
dd if=/dev/zero of=/var/lib/libvirt/images/staging.img bs=1G count=12
virsh create ~/staging.xml

until [ $(curl -s http://172.16.0.5/finished | grep up) ]; do echo 'waiting...'>>/tmp/test.log ; sleep 5 ; done

virsh destroy pxe
virsh undefine pxe
rm /var/lib/libvirt/images/pxe.img
dd if=/dev/zero of=/var/lib/libvirt/images/pxe.img bs=1G count=10
virsh create ~/pxe.xml
