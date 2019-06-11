import math
import time
from django.core.management.base import BaseCommand, CommandError
from django.db import connections
from django.db.models import Func, F, Value
from onadata.apps.logger.models import XForm, Instance

TOLL_FREE_TRACKING = {"project_details": "project_detail",
                       "drawing_document": "drawing_docume",
                       "technical_question": "technical_ques"}

EVENTS = {"radio_broadcast": "radio_broadcas",
          "homeowner_training": "homeowner_trai",
          "engineer_training": "engineer_train",
          "project_introduction": "project_introd",
          "introduction_about_tsc": "introduction_a",
          "municipal_process_of_drawing": "municipal_proc",
          "reconstruction_process_of_nepa": "reconstruction",
          "inspection_mechanism_of_houses": "inspection_mec",
          "things_to_consider_before_duri": "things_to_cons",
          "through_stones_and_tie_stones": "through_stones",
          "correction_methodology_of_non_": "correction_met",
          "khadgabhanjyang": "khadgabhanjyan",
          "vertical_reinforcement": "vertical_reinf",
          }

STFC_SERVICES = {"municipality_report": "municipality_r",
                 "special_actions": "special_action",
                 "project_inquiry": "project_inquir",
                 "municipal_procedure": "municipal_proc",
                 "vulnerable_consultation": "vulnerable_con",
                 "grievance_consultation": "grievance_cons",
                 "banking_consultation": "banking_consul",
                 "construction_site": "construction_s",
                 "drawing_registration": "drawing_regist",
                 "drawing_receive": "drawing_receiv",
                 "banking_support": "banking_suppor",
                 "land_facilitation": "land_facilitat",
                 "pa_agreement_sa": "pa_agreement_s",
                 "withdraw_tranche": "withdraw_tranc",
                 }

CORRECTION_ACTION = {"construction_material": "construction_m",
                     "vertical_reinforcement": "vertical_reinf",
                     "horizontal_bands": "horizontal_ban"}

DICT = {"1422133": TOLL_FREE_TRACKING,
        "1422297": EVENTS,
        "992794": STFC_SERVICES,
        "894808": CORRECTION_ACTION}


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
        instances = Instance.objects.filter(fieldsight_instance__project_fxf=project_fxf).only('xml')
        instances = instances.annotate(
            root_node_name=Func(
                F('xml'),
                Value(pattern),
                function='regexp_matches'
            )
        ).values_list('pk', flat=True)
        if not instances():
            self.stderr.write('No Instances found.')
            return
        self.stderr.write('{} instance fro pattern {}'.format(len(instances), pattern))

        for instance_id in instances:

            queryset = Instance.objects.filter(pk=instance_id).only('xml')
            fixed_xml = replace_all_pattern(project_fxf,queryset[0].xml)
            new_xml_hash = Instance.get_hash(fixed_xml)
            queryset.update(xml=fixed_xml, xml_hash=new_xml_hash)

        self.stderr.write(
            '\nFinished {} '.format(
                instance_id,)
        )

