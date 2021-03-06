from django.core.management.base import NoArgsCommand
from django.conf import settings
from newsletter.models import Letter

class Command(NoArgsCommand):
    help = 'Send the newsletter queued in Letters'
    def handle_noargs(self, **options):
        letters = Letter.objects.all().order_by("id")[:settings.NEWSLETTER_QUOTA]
        for letter in letters:
            letter.send()
            letter.delete()
