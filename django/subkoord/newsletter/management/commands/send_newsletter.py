from django.core.management.base import NoArgsCommand
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.template import Context, Template
from django.conf import settings
from datetime import datetime
from subkoord.newsletter.models import Letter, Message, Subscriber

class Command(NoArgsCommand):
	help = 'Send the newsletter queued in Letters'
	def handle_noargs(self, **options):
		letters = Letter.objects.all()[:settings.NEWSLETTER_QUOTA]
		jobs = {}
		for letter in letters:
			footer_text = Template(letter.job.to.footer_text)
			footer_html = Template(letter.job.to.footer_html)
			c = Context({
				'unsubscribe_url': settings.SITE_URL+reverse('subscriber_public_delete', args=[letter.recipient.id, letter.recipient.token]),
			})
			text_plain = "\n".join([letter.message.text_as_plain, footer_text.render(c)])
			text_html = "\n<br>\n".join([letter.message.text_as_html, footer_html.render(c)])
			mail = EmailMultiAlternatives(
				subject = u'%s %s' % (letter.job.to.praefix, letter.message.subject),
				body = text_plain,
				from_email = settings.NEWSLETTER_FROM,
				to = [letter.recipient.email],
			)
			for attachement in letter.message.attachements.all():
				mail.attach_file(attachement.file.file.name)
			if letter.message.text_format != "plain":
				mail.attach_alternative(text_html, "text/html")
			mail.send()
			try:
				job = jobs[letter.job.id]
			except KeyError:
				job = letter.job
				jobs[letter.job.id] = job
			job.letters_sent += 1
			letter.delete()
		for job_id, job in jobs.items():
			job.last_delivery = datetime.now()
			job.save()
