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
mysql -uroot -e "CREATE DATABASE IF NOT EXISTS havate; GRANT USAGE ON *.* TO havate@localhost IDENTIFIED BY 'havate'; GRANT ALL PRIVILEGES ON havate.* TO havate@localhost; FLUSH PRIVILEGES;"

  sed -e "/logging.DEBUG/a \\
\\
DATABASES = {\\
    'default': {\\
        'ENGINE': 'django.db.backends.mysql',\\
        'NAME': 'havate',\\
        'USER': 'havate',\\
        'PASSWORD': 'havate',\\
        'HOST': 'localhost',\\
        'PORT': '',\\
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

