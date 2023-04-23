from celery import shared_task

from django.core.mail import send_mail

from events.models import Event

from django.utils import timezone

from events.models import Event
import logging

logger = logging.getLogger(__name__)

@shared_task
def event_reserved(event_id):
    event = Event.objects.get(id=event_id)
    subject = f'Event subject : {event.id}'
    message = f'Dear {event.user.username} \n\n' \
              f'You have successfully reserved \'{event.subject}\' at \n ' \
              f'{event.start_date}'
    
    mail_sent = send_mail(subject, 
                            message,
                            'admin@event.com',
                            [event.user.email])
    return mail_sent


def send_email(subject, message, to):
    mail = send_mail(
            subject=subject,
            message=message, 
            from_email='noreply@evenhive.com',
            recipient_list=to
        )
    return mail

@shared_task
def send_reminders():
    now = timezone.now()
    
    one_hour_before = now + timezone.timedelta(minutes=4)
    one_day_before = now + timezone.timedelta(days=1)
    
    events = Event.objects.all()
    
    for event in events:
        hour_subject = 'Reminder: {} is happening soon!'.format(event.subject)
        hour_message = 'Hi,\n\nThis is a friendly reminder that {} is happening in one hour.\
                        \n\nThanks!'.format(event.subject)

        day_message = 'Hi,\n\nThis is a friendly reminder that {} is happening tomorrow.\
                        \n\nThanks!'.format(event.subject)

        day_subject = 'Reminder: {} is happening tomorrow!'.format(event.subject)

        
        participants = event.subscriptions.all()
        hour = one_hour_before <= event.start_date <= one_hour_before + timezone.timedelta(minutes=4)
        day = one_day_before <= event.start_date <= one_day_before + timezone.timedelta(days=1)
        users_email = [user.email for user in participants]

        logger.info(event.start_date)
        logger.info(one_hour_before)
        mail_sent = None
        if hour:
            mail_sent = send_email(hour_subject, hour_message, users_email)

        if day:
            mail_sent = send_email(day_subject, day_message, users_email)
        
        return mail_sent


