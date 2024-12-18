from datetime import datetime
from django.db import models
from django.urls import reverse

from calendarapp.models import EventAbstract
from accounts.models import User


class EventManager(models.Manager):
    """ Event manager """

    def get_all_events(self, user):
        events = Event.objects.filter(user=user, is_active=True, is_deleted=False)
        return events

    def get_running_events(self, user):
        running_events = Event.objects.filter(
            user=user,
            is_active=True,
            is_deleted=False,
            end_time__gte=datetime.now().date(),
            start_time__lte = datetime.now().date()
        ).order_by("start_time")
        return running_events
    
    def get_completed_events(self, user):
        completed_events = Event.objects.filter(
            user=user,
            is_active=True,
            is_deleted=False,
            end_time__lt=datetime.now().date(),
        )
        return completed_events
    
    def get_upcoming_events(self, user):
        upcoming_events = Event.objects.filter(
            user=user,
            is_active=True,
            is_deleted=False,
            start_time__gt=datetime.now().date(),
        )
        return upcoming_events

    # def get_waiting_aproval_events(self, user):
    #     get_waiting_aproval_events = Event.objects.filter(
    #         user=user,
    #         state__title="En espera"
    #     )
    #     print()
    #     return get_waiting_aproval_events

class EventType(models.Model):
    description = models.CharField(max_length=200)
    duracion = models.TimeField()

    def __str__(self):
        return f"{self.duracion}"

class Patient(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    DocumentId = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.DocumentId}"

class Event(EventAbstract):
    """ Event model """

    user = models.ManyToManyField(User)
    patient = models.ForeignKey(Patient,on_delete=models.SET_NULL,null=True,related_name="patient")
    diagnosis = models.TextField()
    start_time = models.DateTimeField(null=True,blank=True)

    end_time = models.DateTimeField(null=True,blank=True)
    event_type = models.ForeignKey(EventType,on_delete=models.SET_NULL,null=True,related_name="event_type")

    objects = EventManager()


    def __str__(self):
        return self.diagnosis

    def get_absolute_url(self):
        return reverse("calendarapp:event-detail", args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse("calendarapp:event-detail", args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'

class EventCalendar(EventAbstract):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)

    def __str__(self):
        return f"{self.event.diagnosis} {self.start_time} {self.end_time}"
