from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify


# Create your models here.
class Event(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.CharField(max_length=500)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    capacity = models.IntegerField(null=True, blank=True)
    subscriptions = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_events',)
    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField(editable=False)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
            self.slug = slugify(self.subject)
        self.updated = timezone.now()
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.subject

    