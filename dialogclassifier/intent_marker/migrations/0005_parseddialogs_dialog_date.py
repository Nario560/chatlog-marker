# Generated by Django 2.1 on 2018-09-04 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intent_marker', '0004_auto_20180903_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='parseddialogs',
            name='dialog_date',
            field=models.DateField(null=True),
        ),
    ]
