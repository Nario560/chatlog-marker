# Generated by Django 2.1 on 2018-09-10 11:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intent_marker', '0009_auto_20180910_1437'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserStat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dte', models.DateField(default=datetime.date(2018, 9, 10))),
                ('user', models.CharField(max_length=32)),
                ('records_done', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='logrecord',
            name='record_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
