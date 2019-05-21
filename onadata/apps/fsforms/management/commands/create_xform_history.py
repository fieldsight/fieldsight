from __future__ import unicode_literals

import os
import glob

from django.core.files import File

from django.core.management.base import BaseCommand
from onadata.apps.fsforms.models import XformHistory
from onadata.apps.logger.models import XForm

from pyxform.builder import create_survey_from_xls

from pyxform import xls2json_backends
import xlwt
import re
import StringIO

def copy_filelike_to_filelike(src, dst, bufsize=16384):
    while True:
        buf = src.read(bufsize)
        if not buf:
            break
        dst.write(buf)


def csv_to_xls(csv_repr):
    csv_repr = ''.join([
        line for line in csv_repr if line.strip().strip('"')
    ])

    def _add_contents_to_sheet(sheet, contents):
        cols = []
        for row in contents:
            for key in row.keys():
                if key not in cols:
                    cols.append(key)
        for ci, col in enumerate(cols):
            sheet.write(0, ci, col)
        for ri, row in enumerate(contents):
            for ci, col in enumerate(cols):
                val = row.get(col, None)
                if val:
                    sheet.write(ri + 1, ci, val)

    encoded_csv = csv_repr.decode("utf-8").encode("utf-8")
    dict_repr = xls2json_backends.csv_to_dict(StringIO.StringIO(encoded_csv))
    workbook = xlwt.Workbook()
    for sheet_name in dict_repr.keys():
        # pyxform.xls2json_backends adds "_header" items for each sheet.....
        if not re.match(r".*_header$", sheet_name):
            cur_sheet = workbook.add_sheet(sheet_name)
            _add_contents_to_sheet(cur_sheet, dict_repr[sheet_name])
    # TODO: As XLS files are binary, I believe this should be `io.BytesIO()`.
    string_io = StringIO.StringIO()
    workbook.save(string_io)
    string_io.seek(0)
    return string_io


def get_version(xml):
    import re
    p = re.compile('version="(.*)">')
    m = p.search(xml)
    if m:
        return m.group(1)
    raise Exception("no version found")


def get_id_string(xml):
    import re
    p = re.compile('id="(.*)" ')
    m = p.search(xml)
    if m:
        return m.group(1)
    raise Exception("no id string found")


class Command(BaseCommand):
    help = 'Create xml from xls'
    
    def add_arguments(self, parser):
        parser.add_argument('directory', type=str)

    def handle(self, *args, **options):
        # xls_directory = "/home/xls"
        xls_directory = options['directory']
        error_file_list = []
        # csv_to_xls(xls_directory)
        for filename in os.listdir(xls_directory):
            if os.path.isfile(os.path.join(xls_directory,filename)):
                if filename.endswith(".xls"):
                    pass
                elif filename.endswith(".csv"):
                    pass
                else:
                    print("##########################")
                    print("##########################")
                    print("Differentt format file", filename)
                    print("##########################")
                    print("##########################")
                    continue

            xls_file = open(os.path.join(xls_directory, filename))
            print("creating survey for ", xls_file)
            try:
                if filename.endswith(".csv"):
                    csv_file = open(os.path.join(xls_directory, filename))
                    bytes_io = csv_to_xls(csv_file)
                    with open(xls_directory + '' + filename.replace('.csv', '.xls'), 'wb') as f:
                        copy_filelike_to_filelike(bytes_io, f)
                        f.close()
                    xls_file = open(xls_directory + '' + filename.replace('.csv', '.xls'), 'r')

                survey = create_survey_from_xls(xls_file)
                xml = survey.to_xml()
                version = get_version(xml)
                id_string = get_id_string(xml)
            except Exception as e:
                error_file_list.append(filename)
                pass

            else:
                xls_file.close()
            
            # print("version =  ======", version)
            if not XForm.objects.filter(id_string=id_string).exists():
                print("xform with id string not found ", id_string)
                continue
            xform = XForm.objects.get(id_string=id_string)
            xform_version = get_version(xform.xml)
            if version == xform_version:
                print("##########################")
                print("##########################")
                print("this file is current version of Xform", filename, "Ignored")
                print("##########################")
                print("##########################")
                continue
            if not XformHistory.objects.filter(xform=xform, version=version).exists():
                print("creating history from file ", filename)
                if filename.endswith('.csv'):
                    file_obj = open(xls_directory + '' + filename.replace('.csv', '.xls'), 'r')
                else:
                    file_obj = open(os.path.join(xls_directory, filename))
                history = XformHistory(xform=xform, xls=File(file_obj))
                history.save()
            else:
                print('History already exists of this file  ', filename)
            print('Successfully created XFORM HISTORY form  ', filename)
        
        if error_file_list:
            print('Errors occured at files: ')
            for files in error_file_list:
                print(files)