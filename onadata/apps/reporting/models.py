from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from jsonfield import JSONField

from onadata.apps.fieldsight.models import Project

REPORT_TYPES = (
    (0, 'Site'),
    (1, 'Region'),
    (2, 'Project'),
    (3, 'Team'),
    (4, 'User'),
    (5, 'Time Series'),
                )

REPORT_TYPES_DICT = dict(list(REPORT_TYPES))

METRICES_DATA = [
    {'code': 'num_sites', 'label': _('Number of Sites'), 'types': [1, 2, 3, 4, 5],
     'category': 'default'},
    {'code': 'num_regions', 'label': _('Number of Regions'), 'types': [2, 3, 4, 5],
     'category': 'default'},
    {'code': 'num_projects', 'label': _('Number of Projects'), 'types': [3, 4, 5],
     'category': 'default'},
    {'code': 'sites_visited', 'label': _('Sites Visited'), 'types': [0, 1, 2, 3, 4, 5],
     'category': 'default'},
    # {'code': 'regions_visited', 'label': _('Regions Visited'), 'types': [1, 2, 3, 4, 5],
    #  'category': 'default'},
    # {'code': 'projects_visited', 'label': _('Projects Visited'), 'types': [2, 3, 4, 5],
    #  'category': 'default'},
    # {'code': 'teams_visited', 'label': _('Teams Visited'), 'types': [3, 4, 5],
    #  'category': 'default'},
    {'code': 'sites_reviewed', 'label': _('Sites Reviewed'), 'types': [0, 1, 2, 3, 4, 5],
     'category': 'default'},
    # {'code': 'regions_reviewed', 'label': _('Regions Visited'), 'types': [1, 2, 3, 4, 5],
    #  'category': 'default'},
    # {'code': 'projects_reviewed', 'label': _('Project Visited'), 'types': [2, 3, 4, 5],
    #  'category': 'default'},
    # {'code': 'teams_reviewed', 'label': _('Teams Visited'), 'types': [3, 4, 5],
    #  'category': 'default'},
    {'code': 'progress', 'label': _('Progress (Actual)'), 'types': [0],
     'category': 'default'},
    {'code': 'progress_avg', 'label': _('Progress (Average)'), 'types': [1, 2, 3, 4, 5],
     'category': 'default'},
    {'code': 'progress_max', 'label': _('Progress (Maximum)'), 'types': [1, 2, 3, 4, 5],
     'category': 'default'},
    {'code': 'progress_min', 'label': _('Progress (Minimum)'), 'types': [1, 2, 3, 4, 5],
     'category': 'default'},

    {'code': 'status_most_recent_submission', 'label': _('Status of Most Recent Submission'), 'types': [0, 4],
     'category': 'default'},
    {'code': 'no_submissions', 'label': _('Number of Submissions'), 'types': [0, 1, 2, 3, 4, 5],
     'category': 'default'},
    {'code': 'no_pending_submissions_current', 'label': _('Number of Pending Submissions (Current)'),
     'types': [0, 1, 2, 3, 4], 'category': 'default'},
    {'code': 'no_pending_submissions_ever', 'label': _('Number of Pending Submissions (Ever)'),
     'types': [0, 1, 2, 3, 4, 5], 'category': 'default'},
    {'code': 'no_approved_submissions_current', 'label': _('Number of Approved Submissions (Current)'),
     'types': [0, 1, 2, 3, 4], 'category': 'default'},
    {'code': 'no_approved_submissions_ever', 'label': _('Number of Approved Submissions (Ever)'),
     'types': [0, 1, 2, 3, 4, 5], 'category': 'default'},
    {'code': 'no_flagged_submissions_current', 'label': _('Number of Flagged Submissions (Current)'),
     'types': [0, 1, 2, 3, 4], 'category': 'default'},
    {'code': 'no_flagged_submissions_ever', 'label': _('Number of Flagged Submissions (Ever)'),
     'types': [0, 1, 2, 3, 4, 5], 'category': 'default'},
    {'code': 'no_rejected_submissions_current', 'label': _('Number of Rejected Submissions (Current)'),
     'types': [0, 1, 2, 3, 4], 'category': 'default'},
    {'code': 'no_rejected_submissions_ever', 'label': _('Number of Rejected Submissions (Ever)'),
     'types': [0, 1, 2, 3, 4, 5], 'category': 'default'},
    {'code': 'no_resolved_submissions_current', 'label': _('Number of Resolved Submissions (Current)'),
     'types': [0, 1, 2, 3, 4], 'category': 'default'},
        {'code': 'no_resolved_submissions_ever', 'label': _('Number of Resolved Submissions (Ever)'),
     'types': [0, 4, 5], 'category': 'default'},
    {'code': 'submissions_flagged_by_user', 'label': _('Number of Submissions Flagged'),
     'types': [4], 'category': 'default'},
    {'code': 'submissions_rejected_by_user', 'label': _('Number of Submissions Rejected'),
     'types': [4], 'category': 'default'},
    {'code': 'submissions_approved_by_user', 'label': _('Number of Submissions Approved'),
     'types': [4], 'category': 'default'},
    {'code': 'submissions_resolved_by_user', 'label': _('Number of Submissions Resolved'),
     'types': [4], 'category': 'default'},
]

INDIVIDUAL_FORM_METRICS_DATA = [
      {'code': 'form_no_submissions', 'label': _('Number of Submissions'), 'types': [0, 1, 2, 3, 4, 5],
       'category': 'individual_form'},
      {'code': 'form_no_pending_submissions_current', 'label': _('Number of Pending Submissions (Current)'), 'types': [0, 1, 2, 3, 4],
       'category': 'individual_form'},
      {'code': 'form_no_approved_submissions_current', 'label': _('Number of Approved Submissions (Current)'), 'types': [0, 1, 2, 3, 4],
       'category': 'individual_form'},
      {'code': 'form_no_flagged_submissions_current', 'label': _('Number of Flagged Submissions (Current'), 'types': [0, 1, 2, 3, 4],
       'category': 'individual_form'},
      {'code': 'form_no_rejected_submissions_current', 'label': _('Number of Rejected Submissions (Current)'), 'types': [0, 1, 2, 3],
       'category': 'individual_form'},
      {'code': 'form_no_resolved_submissions_current', 'label': _('Number of Resolved Submissions (Current)'), 'types': [],
       'category': 'individual_form'},
      {'code': 'form_no_submissions_reviewed', 'label': _('Submissions Reviewed'), 'types': [0, 1, 2, 3, 4, 5],
       'category': 'individual_form'},
      {'code': 'form_no_submissions_flagged_ever', 'label': _('Submissions Flagged (Ever)'), 'types': [0, 1, 2, 3, 4, 5],
       'category': 'individual_form'},
      {'code': 'form_submissions_rejected_ever', 'label': _('Submissions Rejected (Ever)'), 'types': [0, 1, 2, 3, 4, 5],
       'category': 'individual_form'},
      {'code': 'form_submissions_approved_ever', 'label': _('Submissions Approved (Ever)'), 'types': [0, 1, 2, 3, 4, 5],
       'category': 'individual_form'},
      {'code': 'form_submissions_resolutions_ever', 'label': _('Submission Resolutions (Ever)'), 'types': [0, 1, 2, 3, 4, 5],
       'category': 'individual_form'}
]


USERS_METRICS_DATA = [
    {'code': 'active_users', 'label': _('Number of Active Users'), 'types': [0, 1, 2, 3, 5], 'category': 'users'},
    {'code': 'no_of_organization_admin', 'label': _('Number of Organization Admin'),
     'types': [3, 5], 'category': 'users'},
    {'code': 'no_of_project_manager', 'label': _('Number of Project Manager'),
     'types': [2, 3, 5], 'category': 'users'},
    {'code': 'no_of_project_donor', 'label': _('Number of Project Donor'),
     'types': [2, 3, 5], 'category': 'users'},
    {'code': 'no_of_region_supervisor', 'label': _('Number of Region Supervisor'),
     'types': [1, 2, 3, 5], 'category': 'users'},
    {'code': 'no_of_region_reviewer', 'label': _('Number of Region Reviewer'),
     'types': [1, 2, 3, 5], 'category': 'users'},
    {'code': 'no_of_site_supervisor', 'label': _('Number of Site Supervisor'),
     'types': [0, 1, 2, 3, 5], 'category': 'users'},
    {'code': 'no_of_site_reviewer', 'label': _('Number of Reviewer'), 'types': [0, 1, 2, 3, 5], 'category': 'users'},
    {'code': 'no_of_active_organization_admin', 'label': _('Number of Active Organization Admin'),
     'types': [3, 5], 'category': 'users'},
    {'code': 'no_of_active_project_manager', 'label': _('Number of Active Project Manager'),
     'types': [2, 3, 5], 'category': 'users'},
    {'code': 'no_of_active_project_donor', 'label': _('Number of Active Project Donor'),
     'types': [2, 3, 5], 'category': 'users'},
    {'code': 'no_of_active_region_supervisor', 'label': _('Number of Active Region Supervisor'),
     'types': [1, 2, 3, 5], 'category': 'users'},
    {'code': 'no_of_active_region_reviewer', 'label': _('Number of Active Region Reviewer'),
     'types': [1, 2, 3, 5], 'category': 'users'},
    {'code': 'no_of_active_site_supervisor', 'label': _('Number of Active Site Supervisor'),
     'types': [0, 1, 2, 3, 5], 'category': 'users'},
    {'code': 'no_of_active_site_reviewer', 'label': _('Number of Active Reviewer'),
     'types': [0, 1, 2, 3, 5], 'category': 'users'}
]

SITE_INFORMATION_VALUES_METRICS_DATA = [
    {'code': 'actual', 'label': _('Actual'), 'types': [0],
     'category': 'site_information'},

    {'code': 'average', 'label': _('Average'), 'types': [3, 2],
     'category': 'site_information'},

    {'code': 'sum', 'label': _('Sum'), 'types': [3, 2],
     'category': 'site_information'},

    {'code': 'maximum', 'label': _('Maximum'), 'types': [3, 2],
     'category': 'site_information'},

    {'code': 'minimum', 'label': _('Minimum'), 'types': [3, 2],
     'category': 'site_information'},

    {'code': 'most_common', 'label': _('Most Common'), 'types': [3, 2],
     'category': 'site_information'},

    {'code': 'count', 'label': _('Count'), 'types': [3, 2],
     'category': 'site_information'},

    {'code': 'count_distinct', 'label': _('Count Distinct'), 'types': [3, 2],
     'category': 'site_information'},

    {'code': 'all_values', 'label': _('All Values'), 'types': [],
     'category': 'site_information'},
]

FORM_INFORMATION_VALUES_METRICS_DATA = [
    {'code': 'form_info_most_recent', 'label': _('Most Recent'), 'types': [0, 1, 2],
     'category': 'form_information'},

    {'code': 'form_info_average', 'label': _('Average'), 'types': [0, 1, 2],
     'category': 'form_information'},

    {'code': 'form_info_sum', 'label': _('Sum'), 'types': [0, 1, 2],
     'category': 'form_information'},

    {'code': 'form_info_maximum', 'label': _('Maximum'), 'types': [0, 1, 2],
     'category': 'form_information'},

    {'code': 'form_info_minimum', 'label': _('Minimum'), 'types': [0, 1, 2],
     'category': 'form_information'},

    {'code': 'form_info_most_common', 'label': _('Most Common'), 'types': [0, 1, 2],
     'category': 'form_information'},

    {'code': 'form_info_count', 'label': _('Count'), 'types': [0, 1, 2],
     'category': 'form_information'},

    {'code': 'form_info_count_distinct', 'label': _('Count Distinct'), 'types': [0, 1, 2],
     'category': 'form_information'},

    {'code': 'form_info_all_values', 'label': _('All Values'), 'types': [],
     'category': 'form_information'},
]


FILTER_METRICS_DATA = [
    {'code': 'projects', 'label': _('Project'), 'types': [1, 3, 4, 5],
     'category': 'filter'},

    {'code': 'regions', 'label': _('Regions'), 'types':  [0],
     'category': 'filter'},

    {'code': 'site_types', 'label': _('Site Types'), 'types': [0],
     'category': 'filter'},

    {'code': 'user_roles', 'label': _('User Roles'), 'types':  [4],
     'category': 'filter'},

    {'code': 'time_period', 'label': _('Time Period'), 'types':  [5],
     'category': 'filter'},

    {'code': 'site_information', 'label': _('Site Information'), 'types':  [3],
     'category': 'filter'},

    {'code': 'value', 'label': _('Value'), 'types':  [3],
     'category': 'filter'},

    {'code': 'sub_group', 'label': _('Sub Group'), 'types':  [3],
     'category': 'filter'},
]


class ReportSettings(models.Model):
    type = models.IntegerField(default=0, choices=REPORT_TYPES)
    description = models.TextField()
    title = models.CharField(max_length=250)
    owner = models.ForeignKey(User, related_name="report_settings", on_delete=models.CASCADE)
    shared_with = models.ManyToManyField(User, related_name="shared_report_settings", blank=True)
    attributes = JSONField(default=dict)
    filter = JSONField(default=dict)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="report_settings")
    add_to_templates = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    logs = GenericRelation('eventlog.FieldSightLog')

    def __str__(self):
        return self.title

    def getname(self):
        return self.title

    def get_absolute_url(self):
        return "/fieldsight/application/#/report-dashboard/{}".format(self.pk)

    def get_type_display(self):
        return REPORT_TYPES_DICT[self.type]




