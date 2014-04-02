#!/bin/bash
set -x

cd /gui/horizon

MYSQL=`which mysql`
MYSQL=${MYSQL:-/usr/bin/mysql}
$MYSQL -e "CREATE DATABASE IF NOT EXISTS havate; GRANT USAGE ON *.* TO havate@localhost IDENTIFIED BY 'havate'; GRANT ALL PRIVILEGES ON havate.* TO havate@localhost; FLUSH PRIVILEGES;"

if [ ! -z /usr/share/openstack-dashboard/openstack_dashboard ] ; then
  if [ ! `grep crispy_forms /usr/share/openstack-dashboard/openstack_dashboard/settings.py` ] ; then
  sed -e "/dashboards.router/a \\
    'six',\n\
    'django_extensions',\n\
    'south',\n\
    'crispy_forms',\n\
    'config'," -i /usr/share/openstack-dashboard/openstack_dashboard/settings.py 

  sed -e "/BIN_DIR/a \\
PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))\\
\n\
DATABASES = {\n\
    'default': {\n\
        'ENGINE': 'django.db.backends.mysql',\n\
        'NAME': 'havate',\n\
        'USER': 'havate',\n\
        'PASSWORD': 'havate',\n\
        'HOST': 'localhost',\n\
        'PORT': '',\n\
    }\n\
}\n\ " -i /usr/share/openstack-dashboard/openstack_dashboard/settings.py


sed -e "/openstack_auth.urls/a \\
    url(r'^config/', include('config.urls'))," -i /usr/share/openstack-dashboard/openstack_dashboard/urls.py

  fi
fi

cd  /gui/horizon/openstack-dashboard
cp -R * /usr/share/openstack-dashboard/

cd /gui/horizon/horizon
cp -R * /usr/share/pyshared/horizon/templates/horizon/

cd /usr/share/openstack-dashboard/

python manage.py syncdb --noinput
python manage.py migrate 

chmod 777 openstack_dashboard/openstack_settings.txt
chmod 777 openstack_dashboard/static-raw/*
chown horizon.horizon /var/log/horizon/horizon.log

service apache2 restart

