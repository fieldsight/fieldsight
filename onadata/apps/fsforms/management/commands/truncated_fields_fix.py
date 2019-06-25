import math
import time
from django.core.management.base import BaseCommand, CommandError
from django.db import connections
from django.db.models import Func, F, Value

from onadata.apps.api.viewsets.xform_submission_api import update_mongo
from onadata.apps.logger.models import XForm, Instance
from onadata.apps.logger.models.instance import InstanceHistory

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
          "stakeholder_meeting":"stakeholder_me"
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

SANTOSH = {
    "Though_more_advanced_paragraph_structure":"Though_more",
    "Though_it_may_seem_f_ost_relevant_to_them":"Though_it_may_seem",

    "the_middle_par":"the_mi",
    "and__as_allude":"and_a",
    "a_one_sentence":"a_one",
    "_lebron_james_":"_lebro",
    "o_or_what_an_e":"o_or_wh",
    "having_done_th":"having",
    "ample_proves_y":"ample",
    "you_are_provid":"you_are"
}

DICT = {"1422133": TOLL_FREE_TRACKING,
        "1422297": EVENTS,
        "992794": STFC_SERVICES,
        "894808": CORRECTION_ACTION,
        "1640392": SANTOSH}


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

