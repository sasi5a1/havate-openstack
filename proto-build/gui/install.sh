cd /gui
pip install -r requirements.txt -f file:/gui/packages/
python manage.py syncdb --noinput
python manage.py migrate
chmod 660 /gui/openstack.db
chown root.www-data /gui/openstack.db
#Only deploying the GUI
#ln -s /gui/gui.conf /etc/apache2/conf.d/gui.conf
ln -s /gui/gui-8443.conf /etc/apache2/conf.d/gui.conf
ln -s /gui/mirror.conf /etc/apache2/conf.d/mirror.conf
cd /gui/UcsSdk-0.5
python setup.py install
