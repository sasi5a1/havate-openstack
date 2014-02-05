#!/bin/bash

sed -e 's~^#\(d-i mirror/http/proxy string \)none~\1 http://192.168.26.170:8080~' -i $PWD/FinalCD/preseed/ubuntu-server.seed
sed -e 's/sda/vda/' -i $PWD/FinalCD/preseed/ubuntu-server.seed

$PWD/cd-iso-recreate.sh
