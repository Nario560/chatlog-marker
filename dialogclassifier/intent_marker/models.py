from django.db import models
from django.contrib.postgres import fields
from datetime import datetime


# Create your models here.

class Topic(models.Model):
    topic_name = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.topic_name


class Subtopic(models.Model):
    class Meta:
        unique_together = (('subtopic_name', 'topic_ref'),)

    subtopic_name = models.CharField(max_length=255, default='UNKNOWN')
    active = models.BooleanField(default=True)
    topic_ref = models.ForeignKey(Topic, on_delete=models.SET_DEFAULT, default=-1)

    def __str__(self):
        return f'{self.subtopic_name} - {self.topic_ref}'


class MarkedResult(models.Model):
    class Meta:
        unique_together = (('chat_date', 'client_id'),)
        indexes = [
            models.Index(fields=['chat_date', ]),
            models.Index(fields=['client_id', ]),

        ]

    chat_date = models.DateField()
    client_id = models.CharField(max_length=6)
    topic = models.ForeignKey(Topic, on_delete=models.SET_DEFAULT, default=-1)
    subtopic = models.ForeignKey(Subtopic, on_delete=models.SET_DEFAULT, default=-1)
    custom_topic = models.CharField(max_length=800, null=True)
    custom_subtopic = models.CharField(max_length=800, null=True)
    aggressive_client = models.BooleanField(default=False)
    non_standard_question = models.BooleanField(default=False)
    chosen_phrases = fields.ArrayField(models.TextField())

    def __str__(self):
        return f'{self.client_id};{self.topic};{self.subtopic};{self.custom_topic};{self.custom_subtopic};{self.aggressive_client};{self.non_standard_question};{self.chosen_phrases}'


class ParsedDialogs(models.Model):
    class Meta:
        unique_together = (('cus_id', 'dialog_time', 'session', 'event_id'),)
        indexes = [
            models.Index(fields=['cus_id', ]),
            models.Index(fields=['dialog_time', ]),
            models.Index(fields=['dialog_date', ]),
            models.Index(fields=['cus_id', 'dialog_time', ]),
            models.Index(fields=['cus_id', 'dialog_date']),
        ]

    cus_id = models.CharField(max_length=6)
    dialog_time = models.DateTimeField()
    dialog_date = models.DateField(null=True)
    session = models.CharField(max_length=16)
    event_id = models.IntegerField()
    genesys_id = models.CharField(max_length=16)
    flag = models.CharField(max_length=6)
    user_id = models.CharField(max_length=7)
    phrase = models.TextField()
    processed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.cus_id};{self.dialog_time};{self.session};{self.event_id};{self.genesys_id};{self.flag};{self.user_id};{self.phrase}'


class TaskDateRange(models.Model):
    start_date = models.DateField(default=datetime.now().date())
    end_date = models.DateField(default=datetime.now().date())

    def __str__(self):
        return f'{self.start_date}{self.end_date}'


class TaskList(models.Model):
    class Meta:
        db_table = 'intent_marker_task_list'
        managed = False

    dialog_list = fields.JSONField(primary_key=True)


class MarkedResultsReport(models.Model):
    class Meta:
        db_table = 'intent_marker_results_report'
        managed = False

    id = models.IntegerField(primary_key=True)
    chat_date = models.DateField()
    client_id = models.CharField(max_length=6)
    topic_id = models.IntegerField()
    topic_name = models.CharField(max_length=255)
    subtopic_id = models.IntegerField()
    subtopic_name = models.CharField(max_length=255)
    custom_topic = models.CharField(max_length=800)
    custom_subtopic = models.CharField(max_length=800)
    aggressive_client = models.BooleanField()
    non_standard_question = models.BooleanField()
    chosen_phrases = fields.ArrayField(models.TextField())


class LogRecord(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['record_time', ]),
            models.Index(fields=['user', ]),
        ]

    record_time = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=32)
    user_ip = models.CharField(max_length=15)
    user_host = models.TextField()
    request = models.TextField()


class UserStat(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['dte', ]),
            models.Index(fields=['user', ]),
        ]

    dte = models.DateField(default=datetime.now().date())
    user = models.CharField(max_length=32)
    records_done = models.IntegerField(null=False)
