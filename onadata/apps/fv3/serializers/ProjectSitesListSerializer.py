from rest_framework import serializers

from onadata.apps.fieldsight.models import Site

FORM_STATUS = {0: 'Pending', 1: "Rejected", 2: 'Flagged', 3: 'Approved'}


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

        # if obj.current_status <= 3:
        #     return FORM_STATUS[obj.current_status]
        try:
            if obj.site_instances.all():
                return FORM_STATUS[obj.current_status]
        except:
            return None

    def get_progress(self, obj):

        if obj.current_progress:
            return obj.current_progress
        else:
            return 0

    def to_representation(self, obj):
        data = super(ProjectSitesListSerializer, self).to_representation(obj)
        if self.context.get('is_region', None):

            data.pop('region')
        return data