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

ROLE_MATRICS = [
    {'code': 'organization_admin', 'label': _('Organization Admin'), 'children': []},
    {'code': 'project_manager', 'label': _('Project Manager'), 'children': []},
    {'code': 'project_donor', 'label': _('Project Donor'), 'children': []},
    {'code': 'region_supervisor', 'label': _('Region Supervisor'), 'children': []},
    {'code': 'region_reviewer', 'label': _('Region Reviewer'), 'children': []},
    {'code': 'site_supervisor', 'label': _('Site Supervisor'), 'children': []},
    {'code': 'reviewer', 'label': _('Reviewer'), 'children': []},

]

METRICES_DATA = [
    {'code': 'num_sites', 'label': _('Number of Sites'), 'types': [1, 2, 3, 4, 5], 'children':
        [{'code': 'test', 'label': _('Test Label')}, {'code': 'test2', 'label': _('Test Label2')}],
     'category': 'default'},
    {'code': 'num_regions', 'label': _('Number of Regions'), 'types': [0, 2, 3, 4, 5], 'children': [],
     'category': 'default'},
    {'code': 'num_projects', 'label': _('Number of Projects'), 'types': [0, 1, 3, 4, 5], 'children': [],
     'category': 'default'},
    {'code': 'sites_visited', 'label': _('Sites Visited'), 'types': [0, 1, 2, 3, 4, 5], 'children': [],
     'category': 'default'},
    {'code': 'regions_visited', 'label': _('Regions Visited'), 'types': [1, 2, 3, 4, 5], 'children': [],
     'category': 'default'},
    {'code': 'projects_visited', 'label': _('Projects Visited'), 'types': [2, 3, 4, 5], 'children': [],
     'category': 'default'},
    {'code': 'teams_visited', 'label': _('Teams Visited'), 'types': [3, 4, 5], 'children': [],
     'category': 'default'},
    {'code': 'sites_reviewed', 'label': _('Sites Reviewed'), 'types': [0, 1, 2, 3, 4, 5], 'children': [],
     'category': 'default'},
    {'code': 'regions_reviewed', 'label': _('Regions Visited'), 'types': [1, 2, 3, 4, 5], 'children': [],
     'category': 'default'},
    {'code': 'projects_reviewed', 'label': _('Project Visited'), 'types': [2, 3, 4, 5], 'children': [],
     'category': 'default'},
    {'code': 'teams_reviewed', 'label': _('Teams Visited'), 'types': [3, 4, 5], 'children': [],
     'category': 'default'},
    {'code': 'progress', 'label': _('Progress (Average)'), 'types': [0], 'children': [],
     'category': 'default'},
    {'code': 'progress_avg', 'label': _('Progress (Average)'), 'types': [1, 2, 3, 4, 5], 'children': [],
     'category': 'default'},
    {'code': 'progress_max', 'label': _('Progress (Maximum)'), 'types': [1, 2, 3, 4, 5], 'children': [],
     'category': 'default'},
    {'code': 'progress_min', 'label': _('Progress (Minimum)'), 'types': [1, 2, 3, 4, 5], 'children': [],
     'category': 'default'},
    {'code': 'status_most_recent_submission', 'label': _('Status of Most Recent Submission'), 'types': [0, 4],
     'children': [], 'category': 'default'},
    {'code': 'no_submissions', 'label': _('Number of Submissions'), 'types': [0, 1, 2, 3, 4, 5], 'children': [],
     'category': 'default'},
    {'code': 'no_pending_submissions_current', 'label': _('Number of Pending Submissions (Current)'),
     'types': [0, 1, 2, 3, 4, 5], 'children': [], 'category': 'default'},
    {'code': 'no_pending_submissions_ever', 'label': _('Number of Pending Submissions (Ever)'),
     'types': [0, 1, 2, 3, 4, 5], 'children': [], 'category': 'default'},
    {'code': 'no_approved_submissions_current', 'label': _('Number of Approved Submissions (Current)'),
     'types': [0, 1, 2, 3, 4, 5], 'children': [], 'category': 'default'},
    {'code': 'no_approved_submissions_ever', 'label': _('Number of Approved Submissions (Ever)'),
     'types': [0, 1, 2, 3, 4, 5], 'children': [], 'category': 'default'},
    {'code': 'no_flagged_submissions_current', 'label': _('Number of Flagged Submissions (Current)'),
     'types': [0, 1, 2, 3, 4, 5], 'children': [], 'category': 'default'},
    {'code': 'no_flagged_submissions_ever', 'label': _('Number of Flagged Submissions (Ever)'),
     'types': [0, 1, 2, 3, 4, 5], 'children': [], 'category': 'default'},
    {'code': 'no_rejected_submissions_current', 'label': _('Number of Rejected Submissions (Current)'),
     'types': [0, 1, 2, 3, 4, 5], 'children': [], 'category': 'default'},
    {'code': 'no_rejected_submissions_ever', 'label': _('Number of Rejected Submissions (Ever)'),
     'types': [0, 1, 2, 3, 4, 5], 'children': [], 'category': 'default'},
    {'code': 'no_resolved_submissions_current', 'label': _('Number of Resolved Submissions (Current)'),
     'types': [0, 1, 2, 3, 4, 5], 'children': [], 'category': 'default'},
    {'code': 'no_resolved_submissions_ever', 'label': _('Number of Resolved Submissions (Ever)'),
     'types': [0, 1, 2, 3, 4, 5], 'children': [], 'category': 'default'},
    {'code': 'submissions_flagged_by_user', 'label': _('Number of Submissions Flagged'),
     'types': [4], 'children': [], 'category': 'default'},
    {'code': 'submissions_rejected_by_user', 'label': _('Number of Submissions Rejected'),
     'types': [4], 'children': [], 'category': 'default'},
    {'code': 'submissions_approved_by_user', 'label': _('Number of Submissions Approved'),
     'types': [4], 'children': [], 'category': 'default'},
    {'code': 'submissions_resolved_by_user', 'label': _('Number of Submissions Resolved'),
     'types': [4], 'children': [], 'category': 'default'},
    {'code': 'users', 'label': _('Users'),
     'types': [0, 1, 2, 3, 5], 'children':
         [{'code': 'active_users', 'label': _('Number of Active Users'), 'children': [], },
          {'code': 'users_by_role', 'label': _('Number of Users by Role'), 'children': ROLE_MATRICS},
          {'code': 'active_users_by_role', 'label': _('Number of Active Users by Role'), 'children': ROLE_MATRICS, },
          ], 'category': 'users'},

    {'code': 'form', 'label': _('Individual Form Metrics'),
     'types': [0, 1, 2, 3, 4, 5], 'children':
         [{'code': 'form_no_submissions', 'label': _('Number of Submissions'), 'children': [], },
          {'code': 'form_no_pending_submissions', 'label': _('Number of Pending Submissions'), 'children': []},
          {'code': 'form_no_approved_submissions', 'label': _('Number of Approved Submissions'), 'children': [], },
          {'code': 'form_no_flagged_submissions', 'label': _('Number of Flagged Submissions'), 'children': [], },
          {'code': 'form_no_rejected_submissions', 'label': _('Number of Rejected Submissions'), 'children': [], },
          {'code': 'form_no_resolved_submissions', 'label': _('Number of Resolved Submissions'), 'children': [], },
          {'code': 'form_submissions_reviewed', 'label': _('Submissions Reviewed'), 'children': [], },
          {'code': 'form_submissions_flagged', 'label': _('Submissions Flagged'), 'children': [], },
          {'code': 'form_submissions_rejected', 'label': _('Submissions Rejected'), 'children': [], },
          {'code': 'form_submissions_approved', 'label': _('Submissions Approved'), 'children': [], },
          {'code': 'form_submissions_resolutions', 'label': _('Submission Resolutions'), 'children': [], },
          ], 'category': 'users'},

]

SITE_INFORMATION_VALUES_METRICS_DATA = [
    {'code': 'actual', 'label': _('Actual'), 'types': [0, 1, 2], 'children':[],
     'category': 'site_information'},

    {'code': 'average', 'label': _('Average'), 'types': [1, 2], 'children': [],
     'category': 'site_information'},

    {'code': 'sum', 'label': _('Sum'), 'types': [1, 2], 'children': [],
     'category': 'site_information'},

    {'code': 'maximum', 'label': _('Maximum'), 'types': [1, 2], 'children': [],
     'category': 'site_information'},

    {'code': 'minimum', 'label': _('Minimum'), 'types': [1, 2], 'children': [],
     'category': 'site_information'},

    {'code': 'most_common', 'label': _('Most Common'), 'types': [1, 2], 'children': [],
     'category': 'site_information'},

    {'code': 'count', 'label': _('Count'), 'types': [1, 2], 'children': [],
     'category': 'site_information'},

    {'code': 'count_distinct', 'label': _('Count Distinct'), 'types': [1, 2], 'children': [],
     'category': 'site_information'},

    {'code': 'all_values', 'label': _('All Values'), 'types': [1, 2], 'children': [],
     'category': 'site_information'},
]

FORM_INFORMATION_VALUES_METRICS_DATA = [
    {'code': 'form_info_most_recent', 'label': _('Most Recent'), 'types': [0, 1, 2], 'children':[],
     'category': 'form_information'},

    {'code': 'form_info_average', 'label': _('Average'), 'types': [0, 1, 2], 'children': [],
     'category': 'form_information'},

    {'code': 'form_info_sum', 'label': _('Sum'), 'types': [0, 1, 2], 'children': [],
     'category': 'form_information'},

    {'code': 'form_info_maximum', 'label': _('Maximum'), 'types': [0, 1, 2], 'children': [],
     'category': 'form_information'},

    {'code': 'form_info_minimum', 'label': _('Minimum'), 'types': [0, 1, 2], 'children': [],
     'category': 'form_information'},

    {'code': 'form_info_most_common', 'label': _('Most Common'), 'types': [0, 1, 2], 'children': [],
     'category': 'form_information'},

    {'code': 'form_info_count', 'label': _('Count'), 'types': [0, 1, 2], 'children': [],
     'category': 'form_information'},

    {'code': 'form_info_count_distinct', 'label': _('Count Distinct'), 'types': [0, 1, 2], 'children': [],
     'category': 'form_information'},

    {'code': 'form_info_all_values', 'label': _('All Values'), 'types': [0, 1, 2], 'children': [],
     'category': 'form_information'},
]


class ReportSettings(models.Model):
    type = models.IntegerField(default=0, choices=REPORT_TYPES)
    description = models.TextField()
    title = models.CharField(max_length=250)
    owner = models.ForeignKey(User, related_name="report_settings", on_delete=models.CASCADE)
    shared_with = models.ManyToManyField(User, related_name="shared_report_settings", blank=True)
    attributes = JSONField(default=dict)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="report_settings")
    add_to_templates = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



