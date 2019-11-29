from rest_framework import serializers

from onadata.apps.fieldsight.models import ProgressSettings


class ProgressSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgressSettings
        exclude = ('active', 'project', 'user', 'date')

    def validate_source(self, source):
        if source is None:
            raise serializers.ValidationError("Source is Required")
        elif source in [0, 1]:
            self.initial_data['pull_integer_form'] = None
            self.initial_data['pull_integer_form_question'] = None
            self.initial_data['no_submissions_form'] = None
            self.initial_data['no_submissions_total_count'] = None
            return source
        elif source == 2:
            self.initial_data['no_submissions_form'] = None
            self.initial_data['no_submissions_total_count'] = None
            if not self.initial_data['pull_integer_form']:
                raise serializers.ValidationError("Fieldsight Form id is Required")
            if not self.initial_data.get('pull_integer_form_question'):
                raise serializers.ValidationError("Form Question Name is Required")
        elif source in [3, 4]:
            self.initial_data['pull_integer_form'] = None
            self.initial_data['pull_integer_form_question'] = None
            if not self.initial_data['no_submissions_total_count']:
                raise serializers.ValidationError("Total No of Submission Is Required")
            if source == 4 and not self.initial_data['no_submissions_form']:
                raise serializers.ValidationError("Select Form which submission need to be track for site progress, no_submissions_form field")
            elif source == 3:
                self.initial_data['no_submissions_form'] = None
        return source
