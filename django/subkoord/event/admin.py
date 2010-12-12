from subkoord.event.models import *
from django.contrib import admin

admin.site.register(Event,EventType,Task,Job,Note)
