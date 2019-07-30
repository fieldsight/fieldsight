import os
from django.core.management.base import BaseCommand
from onadata.apps.logger.models import Instance, XForm
from onadata.apps.fsforms.models import XformHistory
import re
import json


class Command(BaseCommand):
    help = 'Find the forms that contain incorrect root tag in xml'

    # def add_arguments(self, parser):
    #     parser.add_argument('username', type=str)

    def handle(self, *args, **options):
        # for every forms
        total_xf = XForm.objects.all().count()
        page_size = 100
        page = 0
        while total_xf > 100:
            xf = XForm.objects.all()[page*page_size:(page+1)*page_size]
            print('Checking xform from ', page * page_size, (page + 1) * page_size)
            with open("invalid.json", "a+") as f:
                for form in xf:
                    id_string = form.id_string
                    xml = form.xml
                    if id_string + '_' in xml:
                        print('Xform: ', form.id, form.id_string, form.title)
                        d = {'Xform id': form.id, 'id_string': form.id_string, 'Form name': form.title}
                        j = json.dumps(d)
                        f.write(j)
            total_xf -= page_size
            page += 1

        # for  ever forms history
        total_xfhist = XformHistory.objects.all().count()
        page_size = 100
        page = 0
        while total_xfhist > 100:
            xfhist = XformHistory.objects.all()[page*page_size:(page+1)*page_size]
            print('Checking xform history from ', page * page_size, (page + 1) * page_size)
            with open("invalid.json", "a+") as f:
                for form in xfhist:
                    id_string = form.id_string
                    xml = form.xml
                    if id_string + '_' in xml:
                        with open('invalid.txt', 'a+') as f:
                            print('Xform history: ', form.id, form.id_string, form.version, form.title)
                            d = {'Xform history id': form.id, 'id_string': form.id_string, 'Form name': form.title, 'Form version': form.version}
                            j = json.dumps(d)
                            f.write(j)
            total_xfhist -= page_size
            page += 1
