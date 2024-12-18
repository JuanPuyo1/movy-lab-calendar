from .event_list import AllEventsListView, CompletedEventsListView, RunningEventsListView, UpcomingEventsListView,WaitingEventsListView
from .other_views import (
    CalendarViewNew,
    CalendarView,
    create_event,
    EventEdit,
    event_details,
    add_eventmember,
    EventMemberDeleteView,
    EventModifyStateView,
    TentativeEventCreateView,
    delete_event,
    next_week,
    next_day,
    update_event,
    create_patient,
)


__all__ = [
    AllEventsListView,
    RunningEventsListView,
    UpcomingEventsListView,
    CompletedEventsListView,
    WaitingEventsListView,
    TentativeEventCreateView,
    CalendarViewNew,
    CalendarView,
    create_event,
    EventEdit,
    event_details,
    add_eventmember,
    EventMemberDeleteView,
    EventModifyStateView,
    delete_event,
    next_week,
    next_day,
]
