Continuous Integration Test
===========================

This is a draft of a test to deploy the ISO to a VM, and then PXE a VM from the deployed VM.

This assumes that the libvirt-bin and kvm packages are installed, and that a network called br0 is created against a local interface (e.g. eth1) that supports PXE boot with libvirt.

This is not a perfect test setup yet, gaps include:

1) PXE test needs to wait for initial ISO to be deployed
2) No testing for the GUI (may need UCSM emulator VM to be installed)

