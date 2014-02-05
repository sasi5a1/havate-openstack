Modifying Havate for OpenStack
==============================

There are a number of areas to modify for potential target deployments.

The key files involved:

* cd-iso-recreate.sh

  This file provides the principal packaging service.  It loads code from the proto-build directory along with packages from the package_list.txt, and builds out an ISO with the packages in their own repository

* package_list.txt

  The file lists packages to be downloaded via apt-cache download.  Add packages here based on your specific requirements.  The default provides the packages needed to deploy a basic "All-in-one" OpenStack system.  Note that package resources are pulled down based on the repositories defined in /etc/apt/sources*

* proto-build/preseed/ubuntu-server.seed

  This is the default Ubuntu server preseed for the ISO deployment.  This file by default will build a system that presumes a DHCP service on eth0, and will copy over the entire cdrom contents to re-create the mirror on the target device.

* proto-build/gui/build_install.sh

  This script is the "real" build script, running once on first boot, and by default configuring both cobbler and puppet to build out a simple build node. It also sets up a preseed for cobbler to point back to the build node for disconnected deployments.



