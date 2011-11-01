from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.utils.translation import ugettext as _
from django.conf import settings
from django.core.management.base import NoArgsCommand
import os
import subprocess

class Command(NoArgsCommand):
	help = 'Generate a dump from the database'
	def handle_noargs(self, **options):
		last_backup = datetime.fromtimestamp(os.path.getmtime(settings.BACKUP_DIR+"/backup.sql"))
		if last_backup > datetime.now() - timedelta(hours=1):
			return "only one backup per hour"
		if settings.DATABASES['default']['HOST'] != "":
			host = "-h " + settings.DATABASES['default']['HOST']
		else: host = ""
		user =  "-u " + settings.DATABASES['default']['USER']
		password = "-p" + settings.DATABASES['default']['PASSWORD']
		dbname = settings.DATABASES['default']['NAME']
		mysqldump = "mysqldump --add-drop-table " + " ".join([user, password, host, dbname]) + " >  backup.sql"
		subprocess.call(args=mysqldump, shell=True, cwd=settings.BACKUP_DIR)
		subprocess.Popen(args="gzip -c backup.sql > backup.gz", shell=True, cwd=settings.BACKUP_DIR)
