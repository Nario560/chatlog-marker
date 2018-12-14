from django.contrib import admin
from .models import Topic, Subtopic, MarkedResult, ParsedDialogs, TaskDateRange

# Register your models here.
admin.site.register(Topic)
admin.site.register(Subtopic)
admin.site.register(MarkedResult)
admin.site.register(ParsedDialogs)
admin.site.register(TaskDateRange)
