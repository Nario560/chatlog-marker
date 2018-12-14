# Generated by Django 2.1 on 2018-09-04 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intent_marker', '0005_parseddialogs_dialog_date'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='markedresult',
            index=models.Index(fields=['client_id'], name='intent_mark_client__e0062d_idx'),
        ),
        migrations.AddIndex(
            model_name='parseddialogs',
            index=models.Index(fields=['dialog_date'], name='intent_mark_dialog__7161e2_idx'),
        ),
        migrations.AddIndex(
            model_name='parseddialogs',
            index=models.Index(fields=['cus_id', 'dialog_date'], name='intent_mark_cus_id_557517_idx'),
        ),
    ]
