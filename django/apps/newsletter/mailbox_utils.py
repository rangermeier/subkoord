import poplib
import email
from email.header import decode_header
from email.Utils import parseaddr
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist
from models import Subscriber

def get_server():
    server = poplib.POP3_SSL(settings.NEWSLETTER_ERROR_MAILBOX, 995)
    server.getwelcome()
    server.user(settings.NEWSLETTER_ERROR_USER)
    server.pass_(settings.NEWSLETTER_ERROR_PASS)
    return server

def decodeUnknown(charset, string):
    if not charset:
        try:
            string = string.decode('utf-8')
        except:
            string = string.decode('iso8859-1')
    else:
        string = unicode(string.decode(charset))
    return string

def decode_mail_headers(string):
    decoded = decode_header(string)
    return u' '.join([unicode(msg, charset or 'utf-8') for msg, charset in decoded])

def parse_email(message):
    # 'message' must be an RFC822 formatted message.
    msg = message
    message = email.message_from_string(msg)
    subject = message.get('subject', _('Created from e-mail'))
    subject = decode_mail_headers(decodeUnknown(message.get_charset(), subject))

    date = message.get('date', _('Date'))
    date = decode_mail_headers(decodeUnknown(message.get_charset(), date))

    sender = message.get('from', _('Unknown Sender'))
    sender = decode_mail_headers(decodeUnknown(message.get_charset(), sender))
    sender_email = parseaddr(sender)[1]

    recip = message.get('to', _('Unknown Sender'))
    recip = decode_mail_headers(decodeUnknown(message.get_charset(), recip))
    recip_email = parseaddr(recip)[1]

    message_id = message.get('Message-Id', _('Message-Id'))
    message_id = decode_mail_headers(decodeUnknown(message.get_charset(), message_id))

    body = ""
    for part in message.walk():
        #body = decodeUnknown(part.get_content_charset(), part.get_payload(decode=True))
        #if part.get_content_maintype() == 'multipart':
        #   continue
        if part.get_content_maintype() == 'text' and part.get_param("name") == None:
            if part.get_content_subtype() == 'plain':
                body += decodeUnknown(part.get_content_charset(), part.get_payload(decode=True))

    return {'subject': subject,
        'date': date,
        'sender': sender_email,
        'recipient': recip_email,
        'body': body,
        'message_id': message_id }

def match_error_to_subscriber(message):
    to = message['recipient']
    subscriber_parts = to.split('_')
    try:
        int(subscriber_parts[1]) + 1
        subscriber_id = int(subscriber_parts[1])
    except IndexError:
        return False
    except TypeError:
        return False
    try:
        subscriber = Subscriber.objects.get(pk=subscriber_id)
    except ObjectDoesNotExist:
        return False
    return subscriber
