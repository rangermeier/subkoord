from subkoord.newsletter.models import *
from django.contrib import admin

admin.site.register(List,Subscriber,Message,Job,Letter,Attachement)
