#/bin/sh
echo Upgrading db...
DEBUG=True FLASK_APP=app.py flask db upgrade
echo Done