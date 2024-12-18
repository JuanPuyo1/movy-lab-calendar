# cal/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import timedelta, datetime, date
import calendar
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from calendarapp.models import EventMember, Event, EventCalendar, Patient
from calendarapp.utils import Calendar
from calendarapp.forms import EventForm, AddMemberForm


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month


class CalendarView(LoginRequiredMixin, generic.ListView):
    login_url = "accounts:signin"
    model = Event
    template_name = "calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)
        return context


@login_required(login_url="signup")
def create_event(request):
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data["title"]
        description = form.cleaned_data["description"] 
        start_time = form.cleaned_data["start_time"]
        end_time = form.cleaned_data["end_time"]
        Event.objects.get_or_create(
            user=request.user,
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
        )
        return HttpResponseRedirect(reverse("calendarapp:calendar"))
    return render(request, "event.html", {"form": form})


class EventEdit(generic.UpdateView):
    model = Event
    fields = ["title", "description", "start_time", "end_time"]
    template_name = "event.html"


@login_required(login_url="signup")
def event_details(request, event_id):
    
    event = Event.objects.get(id=event_id)

    users = [user for user in event.user.all()]
    print(users)
    eventmember = EventMember.objects.filter(event=event)
    context = {"event": event, "users": users}
    return render(request, "event-details.html", context)


def add_eventmember(request, event_id):
    forms = AddMemberForm()
    if request.method == "POST":
        forms = AddMemberForm(request.POST)
        if forms.is_valid():
            print("ENTRO")
            users = forms.cleaned_data["user"]  # This will be a QuerySet of selected users
            print(users)
            event = Event.objects.get(id=event_id)
            event.user.add(*users) 
            return redirect(event.get_absolute_url())
    context = {"form": forms}
    return render(request, "add_member.html", context)


class EventMemberDeleteView(generic.DeleteView):
    model = EventMember
    template_name = "event_delete.html"
    success_url = reverse_lazy("calendarapp:calendar")

class TentativeEventCreateView(generic.CreateView):
    form_class = EventForm 
    template_name = "event_tentative_create.html"
    success_url = reverse_lazy("calendarapp:calendar")

    def form_valid(self, form):
        # Get or create the "Aprobado" state
        #state, created = State.objects.get_or_create(title="En espera", color="Yellow")
        
         # Update the event's state
        instance = form.save(commit=False)  # Get the form instance without saving it to the database
        #instance.state = state  # Set the state
        instance.save()  # Save the instance to the database
        
        form.save_m2m()  # Save the many-to-many relationships (if any)
        
        return redirect(self.get_success_url())

    def get_success_url(self):
        # Redirect back to the calendar or a specific page
        return self.success_url

class EventModifyStateView(generic.UpdateView):

    model = Event
    form_class = EventForm 
    template_name = "event_modify.html"
    success_url = reverse_lazy("calendarapp:calendar")

    def form_valid(self, form):
        # Get or create the "Aprobado" state
        #state, created = State.objects.get_or_create(title="Aprobado", color="Blue")
        # if created:
        #     print(f"New state created: {state}")
        # else:
        #     print(f"Existing state used: {state}")

        # # Save the form and associate the State object
        # form.instance.state = state
        form.instance.save()
        
        return redirect(self.get_success_url())

    def get_success_url(self):
        # Redirect back to the calendar or a specific page
        return self.success_url

class CalendarViewNew(LoginRequiredMixin, generic.View):
    login_url = "accounts:signin"
    template_name = "calendarapp/calendar.html"
    form_class = EventForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        events = EventCalendar.objects.all()
        events_month = Event.objects.get_running_events(user=request.user)
        event_list = []
        # start: '2020-09-16T16:00:00'
        for event in events:
            event_list.append(
                {   "id": event.id,
                    "diagnosis": event.event.diagnosis,
                    "start": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                }
            )
        
        context = {"form": forms, "events": event_list,
                   "events_month": events_month}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        #print(forms["user"])
        if forms.is_valid():
            print("ENTRO")
            eventCalendar = EventCalendar(event=forms.save(), start_time=forms.cleaned_data["start_time"], end_time=forms.cleaned_data["end_time"])
            eventCalendar.save()
            forms.save()
        
            # Save the ManyToManyField for users
            #forms.save_m2m()

            return redirect("calendarapp:calendar")
        context = {"form": forms}
        print("NO ENTRO")
        return render(request, self.template_name, context)



def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        return JsonResponse({'message': 'Event sucess delete.'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)

def next_week(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        next = event
        next.id = None
        next.start_time += timedelta(days=7)
        next.end_time += timedelta(days=7)
        next.save()
        return JsonResponse({'message': 'Sucess!'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)

def next_day(request, event_id):

    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        next = event
        next.id = None
        next.start_time += timedelta(days=1)
        next.end_time += timedelta(days=1)
        next.save()
        return JsonResponse({'message': 'Sucess!'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)


@login_required
def update_event(request, event_id):
    print("HOLA")
    event = get_object_or_404(EventCalendar, id=event_id)
    print(event)
    if request.method == 'POST':
        
        #event.title = request.POST.get('title')
        print(request.POST.get('diagnosis'))
        print(event.event.diagnosis)
        event.event.diagnosis = request.POST.get('diagnosis')
        event.event.save()
        event.start_time = request.POST.get('start_time')
        event.end_time = request.POST.get('end_time')
        event.save()
        return JsonResponse({'message': 'Success!'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)
    

def create_patient(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        print(first_name)
        last_name = request.POST.get('last_name')
        print(last_name)
        document_id = request.POST.get('DocumentId')
        print(document_id)
        
        patient = Patient.objects.create(
            first_name=first_name,
            last_name=last_name,
            DocumentId=document_id
        )
        
        return JsonResponse({
            'patient_id': patient.id,
            'patient_name': f"{patient.first_name} {patient.last_name} {patient.DocumentId}"
        })