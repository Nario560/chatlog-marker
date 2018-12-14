from xml.etree import ElementTree
from dateutil.parser import parse
import xlrd
from django.core.management.base import BaseCommand
from intent_marker.models import ParsedDialogs


def parse_and_upload(raw_path: str):
    book = xlrd.open_workbook(raw_path)
    sh = book.sheet_by_index(0)
    total_parsed = 0
    failed = 0

    for rw in range(1, sh.nrows):
        try:
            row = sh.row(rw)[-1].value
            root_tag = ElementTree.fromstring(row)

            cus_id = root_tag.find('.//userData/item/[@key="cus"]').text
            dialog_time = parse(root_tag.attrib['startAt'])
            session = root_tag.attrib['sessionId']

            roles = {}
            for node in root_tag.findall('newParty'):
                actor = ''
                uid = ''
                if len(node) == 2:
                    actor = 'CLIENT'
                    uid = cus_id
                elif len(node) == 1:
                    actor = 'AGENT'
                    uid = node.find('userInfo').attrib['personId']
                roles[node.attrib['userId']] = {'flag': actor, 'user_id': uid}

            for message in root_tag.findall('message'):
                try:
                    event_id = message.attrib['eventId']
                    genesys_id = message.attrib['userId']
                    flag = roles[genesys_id]['flag']
                    user_id = roles[genesys_id]['user_id']
                    phrase = message.find('msgText').text

                    ParsedDialogs.objects.create(
                        cus_id=cus_id,
                        dialog_time=dialog_time,
                        session=session,
                        event_id=event_id,
                        genesys_id=genesys_id,
                        flag=flag,
                        user_id=user_id,
                        phrase=phrase,
                        dialog_date=dialog_time.date(),
                    )
                except KeyError:
                    failed += 1
            total_parsed += 1
        except ElementTree.ParseError:
            failed += 1
    print('Parsing complete.')
    print('Successfully parsed {parsed_ok}'.format(parsed_ok=total_parsed))
    print('Failed to parse {failed}'.format(failed=failed))
    print('Exiting...')


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('raw_path', type=str)

    def handle(self, *args, **options):
        parse_and_upload(options['raw_path'])
