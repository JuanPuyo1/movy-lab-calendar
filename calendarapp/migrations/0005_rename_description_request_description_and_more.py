# Generated by Django 5.1.3 on 2024-12-05 00:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0004_request_event_request'),
    ]

    operations = [
        migrations.RenameField(
            model_name='request',
            old_name='Description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='request',
            old_name='Name',
            new_name='title',
        ),
    ]