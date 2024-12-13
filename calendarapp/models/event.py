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

    def get_waiting_aproval_events(self, user):
        get_waiting_aproval_events = Event.objects.filter(
            user=user,
            state__title="En espera"
        )
        print()
        return get_waiting_aproval_events

class Request(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} {self.description}"


class State(models.Model):
    title = models.CharField(max_length=50)
    color = models.CharField(max_length=20,null=True)

    def __str__(self):
        return f"{self.title} {self.color}"

class Event(EventAbstract):
    """ Event model """

    user = models.ManyToManyField(User)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    request = models.ForeignKey(Request,on_delete=models.SET_NULL,null=True,related_name="requests")
    state = models.ForeignKey(State, on_delete=models.CASCADE,null=True,related_name="states")

    objects = EventManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("calendarapp:event-detail", args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse("calendarapp:event-detail", args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'

