# Generated by Django 5.1.1 on 2024-09-18 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_event_num_tickets_sold'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='available_tickets',
            field=models.IntegerField(),
        ),
    ]
