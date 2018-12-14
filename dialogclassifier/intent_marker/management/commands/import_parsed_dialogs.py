import csv
from dateutil.parser import parse
from django.core.management.base import BaseCommand
from intent_marker.models import ParsedDialogs


def import_parsed_dialogs(raw_path: str, delim=';'):
    with open(raw_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=delim)
        cnter = 0
        for row in reader:
            if cnter != 0:
                ParsedDialogs.objects.create(
                    cus_id=row[0],
                    dialog_time=row[1],
                    session=row[2],
                    event_id=int(row[3]),
                    genesys_id=row[4],
                    flag=row[5],
                    user_id=row[6],
                    phrase=row[7],
                    dialog_date=parse(row[1]).date()
                )
                # sys.stdout.write(f'\rWriting row {cnter}')
                # sys.stdout.flush()
            cnter += 1


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('raw_path', type=str)

    def handle(self, *args, **options):
        import_parsed_dialogs(options['raw_path'])
