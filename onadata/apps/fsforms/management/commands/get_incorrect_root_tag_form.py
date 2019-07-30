import os
from django.core.management.base import BaseCommand
from onadata.apps.logger.models import Instance, XForm
from onadata.apps.fsforms.models import XformHistory
import re


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
            for form in xf:
                id_string = form.id_string
                xml = form.xml
                if id_string + '_' in xml:
                    with open('invalid.txt', 'a+') as f:
                        print('Xform: ' + str(form.id) + str(form.id_string) + str(form.title))
                        f.write('Xform: ' + str(form.id) + str(form.id_string) + str(form.title) + '\n')

        # for  ever forms history
        total_xfhist = XformHistory.objects.all().count()
        page_size = 100
        page = 0
        while total_xfhist > 100:
            xfhist = XformHistory.objects.all()[page*page_size:(page+1)*page_size]
            print('Checking xform history from ', page * page_size, (page + 1) * page_size)
            for form in xfhist:
                id_string = form.id_string
                xml = form.xml
                if id_string + '_' in xml:
                    with open('invalid.txt', 'a+') as f:
                        print('Xform history: ' + str(form.id) + str(form.id_string) + str(form.version) + str(form.title))
                        f.write('Xform history: ' + str(form.id) + str(form.id_string) + str(form.version) + str(form.title) + '\n')
