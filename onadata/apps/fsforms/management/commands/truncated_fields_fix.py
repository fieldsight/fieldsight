import math
import time
from django.core.management.base import BaseCommand, CommandError
from django.db import connections
from django.db.models import Func, F, Value

from onadata.apps.api.viewsets.xform_submission_api import update_mongo
from onadata.apps.logger.models import XForm, Instance
from onadata.apps.logger.models.instance import InstanceHistory


SECOND_TRANCHE = {
    "non_compliant":"com_excep",
    "compliant":"com_excep",
    "com_correc":"com_excep",

}

THIRD_TRANCHE = {
    "non_compliant":"compliant",
    "com_excep":"compliant",
    "com_correc":"compliant",

}

TOLL_FREE = {
    "project_details":"project_detail",
    "drawing_document":"drawing_docume",

}
CORRECTION_ACTION = {
    "horizontal_bands":"horizontal_ban",

}

EVENTS = {
    # "homeowner_training":"homeowner_trai",
    # "project_introduction":"project_introd",
    # "introduction_about_tsc":"introduction_a",
    # "municipal_process_of_drawing":"municipal_proc",
    # "reconstruction_process_of_nepa":"reconstruction",
    "stakeholder_me ":"stakeholder_me",

}

STFC_SERVICES = {
    # "municipal_procedure":"municipal_proc",
    # "grievance_consultation":"grievance_cons",
    # "banking_consultation":"banking_consul",
    # "drawing_registration":"drawing_regist",
    # "drawing_receive":"drawing_receiv",
    # "pa_agreement_sa":"pa_agreement_s",
    "construction_site":"construction_s",

}

DICT = {
        # "894805": THIRD_TRANCHE,
        # "894804": SECOND_TRANCHE,
        "992794": STFC_SERVICES,
        "1422133": TOLL_FREE,
        "1422297": EVENTS,
        "894808": CORRECTION_ACTION,
}


def replace_all_pattern(project_form, xml):
    patterns_dict = DICT.get(str(project_form))
    for pattern, new_pattern in patterns_dict.items():
        xml = xml.replace(pattern, new_pattern)
    return xml


class Command(BaseCommand):
    ''' This command replace string in xml '''

    help = 'fixes instances whose root node names do not match their forms'

    def add_arguments(self, parser):
        parser.add_argument(
            '--project-form-pk',
            type=int,
            dest='project_fxf',
            help='consider only instances whose Project Form ID is equal '\
                 'to this number'
        )
        parser.add_argument(
            '--pattern',
            type=str,
            dest='pattern',
            help='consider only instances whose matches this pattern'
        )

    def handle(self, *args, **options):
        project_fxf = options["project_fxf"]
        pattern = options["pattern"]
        instances = Instance.objects.filter(
         fieldsight_instance__project_fxf__pk=project_fxf
        ).only('xml')
        matches = instances.annotate(
            match=Func(
                F('xml'),
                Value(pattern),
                function='regexp_matches'
            )
        ).values_list('pk', 'match')

        instances = [i[0] for i in matches]

        if not instances:
            self.stderr.write('No Instances found.')
            return
        self.stderr.write('{} instance found for  pattern {}'.format(len(instances), pattern))

        for instance_id in instances:

            queryset = Instance.objects.filter(pk=instance_id).only('xml')
            ih = InstanceHistory(xform_instance=queryset[0],xml=queryset[0].xml)
            ih.save()
            fixed_xml = replace_all_pattern(project_fxf,queryset[0].xml)
            new_xml_hash = Instance.get_hash(fixed_xml)
            queryset.update(xml=fixed_xml, xml_hash=new_xml_hash)
            new_instance = queryset[0]
            new_instance.xml = fixed_xml
            new_instance.xml_hash=new_xml_hash
            update_mongo(new_instance)

        self.stderr.write(
            '\nFinished {} '.format(
                instance_id,)
        )

