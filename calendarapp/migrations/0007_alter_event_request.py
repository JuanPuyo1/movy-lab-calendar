# Generated by Django 5.1.3 on 2024-12-06 02:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0006_alter_eventmember_unique_together_remove_event_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='request',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='requests', to='calendarapp.request'),
        ),
    ]
