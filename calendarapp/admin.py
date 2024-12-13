from django.contrib import admin
from calendarapp import models

@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    model = models.Event
    list_display = [
        "id",
        "title",
        "user",
        "request",
        "is_active",
        "is_deleted",
        "created_at",
        "updated_at",
    ]

    def user(self, obj):
        return "\n".join([p.users for p in obj.user.all()])
    
    list_filter = ["is_active", "is_deleted"]
    search_fields = ["title"]


@admin.register(models.EventMember)
class EventMemberAdmin(admin.ModelAdmin):
    model = models.EventMember
    list_display = ["id", "event", "user", "created_at", "updated_at"]
    list_filter = ["event"]

    def user(self, obj):
        return "\n".join([p.users for p in obj.user.all()])


admin.site.register(models.Request)
admin.site.register(models.State)