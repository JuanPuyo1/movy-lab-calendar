from django.forms import ModelForm, DateInput
from calendarapp.models import Event, EventMember
from django import forms
from accounts.models import User

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["patient", "diagnosis", "user", "event_type","start_time", "end_time"]
        widgets = {
            "patient": forms.Select(attrs={"class": "form-control", "id": "id_patient"}),
            "diagnosis": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter event description",
                }
            ),
            "event_type": forms.Select(attrs={"class": "form-control"}),
            "start_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "end_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
        }
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields["start_time"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["end_time"].input_formats = ("%Y-%m-%dT%H:%M",)



class AddMemberForm(forms.ModelForm):
    class Meta:
        model = EventMember
        fields = ["user"]
