from django.db import models

REPORT_TYPES = (
    (0, 'Site'),
    (1, 'Region'),
    (2, 'Project'),
    (3, 'Team'),
    (4, 'User'),
    (5, 'Time Series'),
                )

METRICES = (
    ('0', 'Number of Sites'),
)

class ReportSettings(models.Model):

    type = models.IntegerField(default=0, choices=REPORT_TYPES)
