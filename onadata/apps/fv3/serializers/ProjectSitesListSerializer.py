from rest_framework import serializers

from onadata.apps.fieldsight.models import Site


class ProjectSitesListSerializer(serializers.ModelSerializer):
    region = serializers.CharField(source='region.name')
    submissions = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()
    type = serializers.CharField(source='type.name')
    status = serializers.SerializerMethodField()

    class Meta:
        model = Site
        fields = ('id', 'identifier', 'name', 'address', 'logo', 'region', 'submissions', 'progress', 'type', 'status')

    def get_submissions(self, obj):
        response = obj.get_site_submission_count()
        submissions = response['outstanding'] + response['flagged'] + response['approved'] + response['rejected']

        return submissions

    def get_status(self, obj):
        return 'Approved'

    def get_progress(self, obj):

        if obj.progress:
            return obj.site_progress

