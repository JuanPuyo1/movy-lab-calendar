# Generated by Django 5.1.4 on 2024-12-08 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0008_state_event_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='color',
            field=models.CharField(max_length=5, null=True),
        ),
    ]
