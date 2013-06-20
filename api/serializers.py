import copy
from django.forms import widgets
from django.contrib.auth.models import User
from rest_framework import serializers

from main.models import UserProfile
from main.forms import RegistrationFormUserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.WritableField(source='user.username')
    email = serializers.WritableField(source='user.email')
    website = serializers.WritableField(source='home_page', required=False)
    gravatar = serializers.Field(source='gravatar')
    password = serializers.WritableField(
        source='user.password', widget=widgets.PasswordInput())

    class Meta:
        model = UserProfile
        fields = ('username', 'name', 'password', 'email', 'city',
                  'country',
                  'organization', 'website', 'twitter', 'gravatar',
                  'require_auth')

    def to_native(self, obj):
        """
        Serialize objects -> primitives.
        """
        ret = super(UserProfileSerializer, self).to_native(obj)
        if 'password' in ret:
            del ret['password']
        return ret

    def restore_object(self, attrs, instance=None):
        params = copy.deepcopy(attrs)
        if instance:
            pass  # TODO: updates
        username = attrs['user.username']
        password = attrs['user.password']
        name = attrs['name']
        name_split = name.split()
        first_name = name_split[0]
        last_name = u''
        if len(name_split) > 1:
            last_name = u' '.join(name_split[1:])
        email = attrs['user.email']
        params.update({
            'email': email, 'username': username,
            'password1': password, 'password2': password})
        form = RegistrationFormUserProfile(params)
        if form.is_valid():
            new_user = User(username=username, first_name=first_name,
                            last_name=last_name, email=email)
            new_user.set_password(password)
            new_user.save()
            profile = UserProfile(
                user=new_user, name=attrs.get('name', u''),
                city=attrs.get('city', u''),
                country=attrs.get('country', u''),
                organization=attrs.get('organization', u''),
                home_page=attrs.get('home_page', u''),
                twitter=attrs.get('twitter', u''))
            return profile
        return attrs
