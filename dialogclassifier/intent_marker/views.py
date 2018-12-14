import json
import csv
from queue import Empty
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
import logging
from .models import Topic, ParsedDialogs, MarkedResult, Subtopic, UserStat, MarkedResultsReport
from .custom_helpers import generate_seed, task_queue, log_record, save_stat
import requests
from dialogclassifier.settings import ELASTIC_URL

logger = logging.getLogger(__name__)


# Create your views here.
def index(request):
    """
    Start page
    """
    return redirect('dialog/{user}'.format(user=generate_seed()))


def total_stat(request):
    """
    Stat by users (all)
    """
    log_record('UNKNOWN', request)
    data = {'context': [{'date': x.dte, 'user': x.user, 'records': x.records_done} for x in UserStat.objects.all()]}
    return render(request, 'intent_marker/user_stat.html', data, RequestContext(request))


def topic_pie(request):
    """
    Iframe with Kibana pie chart, showing share by topics % subtopics
    """
    log_record('UNKNOWN', request)
    return render(request, 'intent_marker/topic_pie.html', None, RequestContext(request))


def user_stat(request, user):
    """
    Stat of a specific user
    """
    log_record(user, request)
    data = {'context': [{'date': x.dte, 'user': x.user, 'records': x.records_done} for x in
                        UserStat.objects.filter(user=user)]}
    return render(request, 'intent_marker/user_stat.html', data, RequestContext(request))


def date_stat(request, dte):
    """
    Stat filtered by date
    """
    log_record('UNKNOWN', request)
    data = {'context': [{'date': x.dte, 'user': x.user, 'records': x.records_done} for x in
                        UserStat.objects.filter(dte=dte)]}
    return render(request, 'intent_marker/user_stat.html', data, RequestContext(request))


def marked_results_report_index(request):
    """
    Reports base page
    """
    log_record('UNKNOWN', request)
    data = {'context': [x for x in MarkedResultsReport.objects.values('chat_date').distinct()]}
    return render(request, 'intent_marker/report_index.html', data, RequestContext(request))


def marked_results_total_report(request):
    """
    Shows all marked dialogs
    """
    log_record('UNKNOWN', request)
    data = {'context': [{
        'id': x.id,
        'chat_date': x.chat_date,
        'client_id': x.client_id,
        'topic_id': x.topic_id,
        'topic_name': x.topic_name,
        'subtopic_id': x.subtopic_id,
        'subtopic_name': x.subtopic_name,
        'custom_topic': x.custom_topic,
        'custom_subtopic': x.custom_subtopic,
        'aggressive_client': x.aggressive_client,
        'non_standard_question': x.non_standard_question,
        'chosen_phrases': x.chosen_phrases
    } for x in MarkedResultsReport.objects.all()]}
    return render(request, 'intent_marker/report_detail.html', data, RequestContext(request))


def marked_results_report_by_date(request, chat_dte):
    """
    Shows marked dialogs by date
    """
    log_record('UNKNOWN', request)
    data = {
        'chat_dte': chat_dte,
        'context': [{
            'id': x.id,
            'chat_date': x.chat_date,
            'client_id': x.client_id,
            'topic_id': x.topic_id,
            'topic_name': x.topic_name,
            'subtopic_id': x.subtopic_id,
            'subtopic_name': x.subtopic_name,
            'custom_topic': x.custom_topic,
            'custom_subtopic': x.custom_subtopic,
            'aggressive_client': x.aggressive_client,
            'non_standard_question': x.non_standard_question,
            'chosen_phrases': x.chosen_phrases
        } for x in MarkedResultsReport.objects.filter(chat_date=chat_dte)]}
    return render(request, 'intent_marker/report_detail.html', data, RequestContext(request))


def marked_results_save_report(request, chat_dte):
    """
    Hook to save report
    """
    log_record('UNKNOWN', request)
    response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename=report_{smart_str(chat_dte)}.csv'

    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf-8'))
    writer.writerow([
        smart_str(u'id'),
        smart_str(u'chat_date'),
        smart_str(u'client_id'),
        smart_str(u'topic_id'),
        smart_str(u'topic_name'),
        smart_str(u'subtopic_id'),
        smart_str(u'subtopic_name'),
        smart_str(u'custom_topic'),
        smart_str(u'custom_subtopic'),
        smart_str(u'aggressive_client'),
        smart_str(u'non_standard_question'),
        smart_str(u'chosen_phrases'),
    ])
    for x in MarkedResultsReport.objects.filter(chat_date=chat_dte):
        writer.writerow([
            smart_str(x.id),
            smart_str(x.chat_date),
            smart_str(x.client_id),
            smart_str(x.topic_id),
            smart_str(x.topic_name),
            smart_str(x.subtopic_id),
            smart_str(x.subtopic_name),
            smart_str(x.custom_topic),
            smart_str(x.custom_subtopic),
            smart_str(x.aggressive_client),
            smart_str(x.non_standard_question),
            smart_str(x.chosen_phrases)
        ])
    return response


@csrf_exempt
def dialog(request, user):
    """
    Display new workpage for user (with new dialog to check)
    """
    log_record(user, request)
    topics = {x.topic_name: sorted([y.subtopic_name for y in x.subtopic_set.filter(active=True).all()]) for x in
              Topic.objects.filter(active=True)}
    # use cache to ensure that user receives the same record until he processes it or inactive for time X
    cached_record = cache.get(user)
    if cached_record:
        task = cached_record
    else:
        try:
            task = task_queue.get(block=False).dialog_list
        except Empty:
            return HttpResponse("<h1>Задачи закончились</h1>")
    next_record = {
        'context': {
            'customer': task['cus_id'],
            'dialog_date': task['dialog_date'],
            'dialog': sorted(task['dialog'],key=lambda d: (d['dialog_time'],d['event_id']))
        },
        'topics': sorted(topics.keys()),
        'topic_meta': topics,
    }
    cache.set(user, task)
    # set TTL for cached task
    cache.touch(user, 60 * 60 * 2)
    return render(request, 'intent_marker/dialog.html', next_record, RequestContext(request))


@csrf_exempt
def save_data(request):
    """
    Hook to save marked dialog
    """
    if request.method != 'POST':
        return HttpResponseBadRequest('<h1>Method not allowed</h1>')
    data = json.loads(request.body)
    user = data['user'].split('/')[-1]

    log_record(user, request)

    cached_record = cache.get(user)

    try:
        top = Topic.objects.get(topic_name=data['topic'], active=True) if data['topic'] != '' else Topic.objects.get(
            topic_name='')
        sbtp = Subtopic.objects.get(subtopic_name=data['subtopic'], topic_ref=top, active=True) if data[
                                                                                                       'topic'] != '' else top.subtopic_set.get(
            subtopic_name='')

        obj, created = MarkedResult.objects.update_or_create(
            chat_date=cached_record['dialog_date'],
            client_id=data['client_id'],
            topic=top,
            subtopic=sbtp,
            custom_topic=data['custom_topic'],
            custom_subtopic=data['custom_subtopic'],
            aggressive_client=data['agressive_client'],
            non_standard_question=data['non_standart_question'],
            chosen_phrases=[x['phrase'] for x in data['chosen_phrases']],
        )

        payload = json.dumps({
            'id': obj.id,
            'chat_date': str(obj.chat_date),
            'client_id': obj.client_id,
            'topic_id': obj.topic.id,
            'topic_name': obj.topic.topic_name,
            'subtopic_id': obj.subtopic.id,
            'subtopic_name': obj.subtopic.subtopic_name,
            'custom_topic': obj.custom_topic,
            'custom_subtopic': obj.custom_subtopic,
            'aggressive_client': obj.aggressive_client,
            'non_standard_question': obj.non_standard_question,
            'chosen_phrases': obj.chosen_phrases
        })

        requests.post(ELASTIC_URL + f'{obj.id}?pretty', payload)

        for parsed_rec in ParsedDialogs.objects.filter(dialog_date=cached_record['dialog_date'],
                                                       cus_id=cached_record['cus_id']):
            parsed_rec.processed = True
            parsed_rec.save()
            # Remove record from cache after it's processed
            cache.delete(user)

    except Exception as e:
        print(e)
    save_stat(user)
    return HttpResponse('')
