from rest_framework import serializers

from onadata.apps.fieldsight.models import Site


class ProjectSitesListSerializer(serializers.ModelSerializer):
    region = serializers.CharField(source='region.name')
    submissions = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Site
        fields = ('id', 'name', 'address', 'logo', 'public_desc', 'region', 'submissions', 'progress')

    def get_submissions(self, obj):
        response = obj.get_site_submission_count()
        submissions = response['outstanding'] + response['flagged'] + response['approved'] + response['rejected']

        return submissions

    def get_status(self, obj):
        pass

    def get_progress(self, obj):

        if obj.progress:
            return obj.site_progress

