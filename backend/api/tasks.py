from celery import shared_task

from django.core.mail import send_mail

from events.models import Event

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