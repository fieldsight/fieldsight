from rest_framework import serializers

from onadata.apps.fsforms.models import FieldSightXF, FInstance


class ProjectSiteResponseSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    title = serializers.SerializerMethodField(read_only=True)
    created_date = serializers.SerializerMethodField(read_only=True)
    last_response = serializers.SerializerMethodField(read_only=True)
    submissions = serializers.SerializerMethodField(read_only=True)
    # json = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FieldSightXF
        fields = ('id', 'name', 'title', 'created_date', 'last_response', 'submissions')

    def get_name(self, obj):
        return u"%s" % obj.xf.title

    def get_title(self, obj):
        return u"%s" % obj.xf.id_string

    def get_created_date(self, obj):
        return obj.date_created

    def get_last_response(self, obj):
        return obj.getlatestsubmittiondate.first.date

    def get_submissions(self, obj):
        submission_count = FInstance.objects.filter(project_fxf=obj.project_fxf)
        return submission_count