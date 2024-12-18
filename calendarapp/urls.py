from django.urls import path

from . import views

app_name = "calendarapp"


urlpatterns = [
    path("calender/", views.CalendarViewNew.as_view(), name="calendar"),
    path("calenders/", views.CalendarView.as_view(), name="calendars"),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('next_week/<int:event_id>/', views.next_week, name='next_week'),
    path('next_day/<int:event_id>/', views.next_day, name='next_day'),
    path("event/new/", views.create_event, name="event_new"),
    path("event/new-tentative-event/", views.TentativeEventCreateView.as_view(), name="event_new_tentative"),
    path("event/edit/<int:pk>/", views.EventEdit.as_view(), name="event_edit"),
    path("event/<int:event_id>/details/", views.event_details, name="event-detail"),
    path('update_event/<int:event_id>/', views.update_event, name='update_event'),
    path('create_patient/', views.create_patient, name='create_patient'),
    path(
        "add_eventmember/<int:event_id>", views.add_eventmember, name="add_eventmember"
    ),
    path(
        "event/<int:pk>/remove",
        views.EventMemberDeleteView.as_view(),
        name="remove_event",
    ),
    path(
        "event/<int:pk>/modify-state",
        views.EventModifyStateView.as_view(),
        name="modify-state",
    ),
    path("all-event-list/", views.AllEventsListView.as_view(), name="all_events"),
    path(
        "running-event-list/",
        views.RunningEventsListView.as_view(),
        name="running_events",
    ),
    path(
        "upcoming-event-list/",
        views.UpcomingEventsListView.as_view(),
        name="upcoming_events",
    ),
    path(
        "completed-event-list/",
        views.CompletedEventsListView.as_view(),
        name="completed_events",
    ),
    path(
        "waiting-approval-events-list/",
        views.WaitingEventsListView.as_view(),
        name="waiting_events",
    ),

]
