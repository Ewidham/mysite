# Generated by Django 2.2.2 on 2019-06-14 12:08

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_question_nr_of_votes'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='added',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 14, 12, 8, 52, 422063, tzinfo=utc), verbose_name='date added'),
        ),
    ]
