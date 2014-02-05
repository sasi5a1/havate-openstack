Havate OpenStack
================

Introducing Havate for Cisco OpenStack
--------------------------------------

Havate addresses one of the most common issues with deploying distributed application envionrments against bare metal hardware: How do I get all of the components configured to work togehter, and get the software installed in an efficient manner.  This is especially difficult if multiple teams need to replicate the enviornment, or a customized version of a deployment is necessary.

Havate is a tool that builds on a number of basic building blocks to accelerate the deployment process and to provide a repeatable solution for deployment by leveraging a number of key capabilities:

* A tool to build an ISO from which the entire deployment enviornment can be built including:
  - a full mirror of the software (base OS/Hypervisor and appliation code)
  - a PXE deployment based on cobbler to automate multiple physical machine deployments
  - a puppet enviornment for application deployment and configuration
  - a Cisco UCS Manager integration to accelerate the phyical system configuration

* UCSM integration toolset:
  - Service profile template creation based on target device roles
  - Network configuration for multiple network services based on target role requirements
  - Physical to role mapping via the cobbler/puppet integration

* A Django based web UI:
  - graphical presentation of available resources
  - extensible for additional use cases and models

These tools, along with an open source methodology, will allow end users to modify the system to suit their particular needs, while simplifying some of the initial configuration needed to get the system into a reproducibly working state.

In addition, the system is built with a Continuous Integration and Continuous Deployment testing environment as a part of the project to allow for validation of the development and deployment environment in advance of actual deployment.

Prerequisites
-------------
In order to build the system in it's baseline configuration, it is expected that the following environment be available:

* A Cisco UCSM managed UCS B-series blade or UCS C-series rack server environment that has it's basic management interface configured and accessible to the end user management network
* A Cisco L3 capable upstream network environment based on the Nexus platform (N3/5/6/7/9K) with an interface accessible to the end user management network
* A copy of the Havate ISO for OpenStack, or a physical or VM Ubuntu 12.04.3 LTS x86_64 server based system with a stable and preferably proxy free network connection
* a system on which a VM can be deployed that can be reached from the defined PXE network (this network will be associated via UCSM service profile, but must be accessible to the VM in order to provide PXE boot services)


Hardware requirements
---------------------
While Havate can be used to deploy to nearly any x86 based platform that supports PXE boot, by default it is targeted at deploying UCS Manager supported and managed devices, both in the UCS B-series blade servers and UCS C-series rack servers.  A base configuration includes the following at a minimum:

* Nexus 5548-UP with L3 services (2 in a redundant network connected configuration)
* UCS 6248 redundant pair of Fabric Interconnect devices
* UCS IOM for the 6508 chassis or UCS 2232 Fabric Extender (in a paired redundant configuration)
* UCS 6508 chassis with at least 1, and but preferably 3 B200-M3 blades with 2x e6509 CPUs, 16GB memory, and 2x 600G SAS drives or 3 UCS C-220-M3-s systems with a standalone RAID card, Cisco VIC, and 2x e6509 CPUs, 16GB memory, and 2x 600G SAS drives

A simple way to ensure the appropriate hardware is available is to acquire a Cisco UCS smart solution bundle for OpenStack, which includes 8 servers and the appropriate network components. 

Supported software
------------------
The Havate deployment system currently enables the deployment of OpenStack based on the Havana release on an Ubuntu 12.04.3 LTS based server platform.  The supported deployment of OpenStack is based on the StackForge project puppet modules, and the puppet\_openstack\_builder model for deployment.

UCS Concepts
------------
While Havate can deploy against any x86 PXE based platform, the UI and the integration for UCSM make it easier to use the tool directly against UCSM managed devices.  To that end it's useful to understand a few of the concepts that are used in the UCS environment, 
-service profile
-service profile template

Downloading Havate ISO
----------------------
The Havate ISO can be downloaded from the [OneCloud website](http://1-cloud.net) at [http://1-cloud.net](http://1-cloud.net)

Or the code to actually build your own can be pulled from the Github project at [https://github.com/havate/havate-openstack](https://github.com/havate/havate-openstack)

The current master snapshot of the cd-create code can also be acquired from the OneCloud web site.

Deploying OpenStack with Havate
-------------------------------
While the Havate GUI tries to guide the user through most of the required steps, there are some pre-configuration steps that are necessary to simplify the deployment process:

* Decide on a VM or physical based staging/build machine, or deploy to the initial node

	This machine can will be the target for the initial ISO install, and as such, is by default configured as a build only node, running cobbler and a puppetmaster instance, from which additional nodes can be deployed.  This is also the system that runs the UCSM integration management, configuring the UCS service profile templates, network models, and storage configurations.  It provides a mirror of the packages needed to deploy OpenStack against the Ubuntu targeted environment.

	An alternate model for this machine is to make it the initial deployment node, however this currently requires manually configuration of at a minimum the service profile for the initial server, and is not recommended.

* Determine the OpenStack deployment model.

  The model for OpenStack can be broken down into two basic categories:

  * Extensible All-in-one controller

		This is the basic all in one model, where all core OpenStack services are deployed to a single system, with the ability to add additional service specific servers (by default only additional compute nodes are defined).  This is the simplest system to deploy directly with the ISO without going though the process of building a build node as a target.

  * Extensible HA based controller

		This is a more complex model, and includes the required configuration scenarios and parameters to enable a 3-way active active control plane, load balanced with internally deployed ha-proxy models.  This system also includes all of the core OpenStack components deployed in as highly available a solution as is possible.  Extension to this model is also possible, though a larger deployment may be better suited to use the non-collapsed HA model which by default requires as many as 13 nodes to support all of the core components including separate devices for front end load balancing and SWIFT proxy services.

  These models can be updated by manipulating the scenario mapping, and can even include software beyond the defaults defined as a part of the baseline ISO.  The current UI does not currently dynamically inspect the actuall scenario beyond the available roles, so any configuration parameters needed beyond that which is currently captured by the UI will need to be entered manually prior to node deployment, or an update to the UI can be made to enable additional data capture.


Installing the OpenStack All-in-One Scenario
--------------------------------------------
The following steps will provide a basic all-in-one scenario based system, and will provide a system that looks like the following diagram:

![openstack all-in-one logical and physical diagram](aio-mapping.svg)

* Capture the required system information.

Next steps
----------

Customizing the ISO
-------------------
This system was designed to support customization by building and/or re-building the ISO from which the system is deployed.  To do so, see the customization document that describes some of the key areas that are likely to be changed, or read through the source code directly.
