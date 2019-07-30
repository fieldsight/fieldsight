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
                    pattern = re.compile(str(id_string)+'_[A-Za-z0-9]+')
                    match = pattern.search(xml)
                    if match:
                        print(match.group(0))
                        xml = xml.replace(match.group(0), id_string)
                        form.xml = xml
                        form.save()
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
                    id_string = form.xform.id_string
                    xml = form.xml
                    pattern = re.compile(str(id_string) + '_[A-Za-z0-9]+')
                    match = pattern.search(xml)
                    if match:
                        print(match.group(0))
                        xml = xml.replace(match.group(0), id_string)
                        form.xml = xml
                        form.save()
            total_xfhist -= page_size
            page += 1
