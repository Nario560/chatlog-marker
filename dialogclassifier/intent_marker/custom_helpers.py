import hashlib
import random
import socket
from queue import Queue

from django.core.cache import cache

from .models import TaskList, LogRecord, UserStat


def generate_seed():
    temp_seed = ''

    while len(temp_seed) < 10:
        temp_seed += chr(random.randrange(97, 122))

    seed_hash = hashlib.md5(temp_seed.encode('utf-8')).hexdigest()

    if cache.get(seed_hash) is not None:
        return generate_seed()
    else:
        return seed_hash


def log_record(user, request):
    LogRecord.objects.create(
        user=user,
        user_ip=request.META.get('REMOTE_ADDR'),
        user_host=socket.getfqdn(request.META.get('REMOTE_ADDR')),
        request=request
    )


def save_stat(user):
    try:
        db_rec = UserStat.objects.get(user=user)
        db_rec.records_done += 1
        db_rec.save()
    except UserStat.DoesNotExist:
        UserStat.objects.create(user=user, records_done=1)


class TaskQ:
    def __init__(self):
        self.task_queue = Queue()

    def load_data(self):
        data = TaskList.objects.all()
        for record in data:
            self.task_queue.put(record)


__tq = TaskQ()
__tq.load_data()
task_queue = __tq.task_queue
