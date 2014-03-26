#!/bin/bash
set -x

cd /gui/horizon

if [ ! -z /usr/share/openstack-dashboard/openstack_dashboard ] ; then
  if [ ! `grep crispy_forms /usr/share/openstack-dashboard/openstack_dashboard/settings.py` ] ; then
  sed -e "/dashboards.router/a \\
    'six',\n\
    'django_extensions',\n\
    'south',\n\
    'crispy_forms',\n\
    'config'," -i /usr/share/openstack-dashboard/openstack_dashboard/settings.py 

  sed -e "/logging.DEBUG/a \\
\\
DATABASES = {\\
'default': {\\
'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'. 'NAME': 'openstackgui', # Or path to database file if using sqlite3.\\
'USER': 'root', #MySQL User\\
'PASSWORD': 'mysql',\\
'HOST': '', # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP .\\
'PORT': '', # Set to empty string for default.\\
}\\
}\\" -i /usr/share/openstack-dashboard/openstack_dashboard/settings.py


sed -e "/openstack_auth.urls/a \\
    url(r'^config/', include('config.urls'))," -i /usr/share/openstack-dashboard/openstack_dashboard/urls.py

  fi
fi

cd  /gui/horizon/openstack-dashboard
cp -R * /usr/share/openstack-dashboard/

cd /gui/horizon/horizon
cp -R * /usr/share/pyshared/horizon/templates/horizon/

cd /usr/share/openstack-dashboard/
python manage.py syncdb
python manage.py migrate

chmod 777 openstack_dashboard/openstack_settings.txt
chmod 777 openstack_dashboard/static_raw/statics/*
chmod 777 openstack_dashboard/static_raw/scenarios/*

service apache2 restart

