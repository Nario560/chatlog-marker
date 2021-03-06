# Generated by Django 2.1 on 2018-08-27 06:25

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MarkedResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_date', models.DateField()),
                ('client_id', models.CharField(max_length=6)),
                ('custom_topic', models.CharField(max_length=800, null=True)),
                ('custom_subtopic', models.CharField(max_length=800, null=True)),
                ('aggressive_client', models.BooleanField(default=False)),
                ('non_standard_question', models.BooleanField(default=False)),
                ('chosen_phrases', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None)),
            ],
        ),
        migrations.CreateModel(
            name='ParsedDialogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cus_id', models.CharField(max_length=6)),
                ('dialog_time', models.DateTimeField()),
                ('session', models.CharField(max_length=16)),
                ('event_id', models.IntegerField()),
                ('genesys_id', models.CharField(max_length=16)),
                ('flag', models.CharField(max_length=6)),
                ('user_id', models.CharField(max_length=7)),
                ('phrase', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Subtopic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subtopic_name', models.CharField(default='UNKNOWN', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='subtopic',
            name='topic_ref',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.SET_DEFAULT, to='intent_marker.Topic'),
        ),
        migrations.AddField(
            model_name='markedresult',
            name='subtopic',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.SET_DEFAULT, to='intent_marker.Subtopic'),
        ),
        migrations.AddField(
            model_name='markedresult',
            name='topic',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.SET_DEFAULT, to='intent_marker.Topic'),
        ),
        migrations.AlterUniqueTogether(
            name='subtopic',
            unique_together={('subtopic_name', 'topic_ref')},
        ),
        migrations.AlterUniqueTogether(
            name='markedresult',
            unique_together={('chat_date', 'client_id')},
        ),
    ]
