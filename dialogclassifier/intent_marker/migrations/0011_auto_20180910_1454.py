# Generated by Django 2.1 on 2018-09-10 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intent_marker', '0010_auto_20180910_1452'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='logrecord',
            index=models.Index(fields=['record_time'], name='intent_mark_record__23310a_idx'),
        ),
        migrations.AddIndex(
            model_name='logrecord',
            index=models.Index(fields=['user'], name='intent_mark_user_ffca88_idx'),
        ),
        migrations.AddIndex(
            model_name='userstat',
            index=models.Index(fields=['dte'], name='intent_mark_dte_4ae394_idx'),
        ),
        migrations.AddIndex(
            model_name='userstat',
            index=models.Index(fields=['user'], name='intent_mark_user_ea7023_idx'),
        ),
    ]
