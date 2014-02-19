from django.core.management.base import NoArgsCommand
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils import translation
from datetime import datetime, timedelta
from event.models import Event

class Command(NoArgsCommand):
    help = 'Check for open tasks and send e-mail if necessary'
    def handle_noargs(self, **options):
        remind_window = timedelta(hours=settings.EVENT_REMINDER_WINDOW)
        remind_pause = timedelta(hours=settings.EVENT_REMINDER_PAUSE)
        now = datetime.now()
        events = Event.objects.select_related(
            ).filter(date__gte = now
            ).filter(date__lte = now + remind_window + remind_pause
            ).exclude(cron__gte = now - remind_pause)
        events_in_remind_window = False
        for event in events:
            if event.date <= now + remind_window:
                events_in_remind_window = True
            if event.all_tasks_satisfied:
                events = events.exclude(id = event.id)
        if events.count() > 0 and events_in_remind_window:
            translation.activate(settings.LANGUAGE_CODE)
            text_plain = loader.render_to_string("email/open_tasks.html",
                {'events': events, 'site_url': settings.SITE_URL,})
            text_html = loader.render_to_string("email/open_tasks_html.html",
                {'events': events, 'site_url': settings.SITE_URL,})
            mail = EmailMultiAlternatives(
                subject = settings.EVENT_REMINDER_SUBJECT,
                body = text_plain,
                from_email = settings.EVENT_REMINDER_FROM,
                to = settings.EVENT_REMINDER_ADDRESSBOOK,
                headers = {'From': settings.EVENT_REMINDER_FROM },
            )
            mail.attach_alternative(text_html, "text/html")
            mail.send()
            for event in events:
              event.cron = datetime.now()
              event.save()
            translation.deactivate()
