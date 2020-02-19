from rest_framework import viewsets, status, response
from fcm.utils import get_device_model
from fcm.serializers import DeviceSerializer
from rest_framework.authentication import BasicAuthentication
from django.contrib.auth.models import User

from onadata.apps.fsforms.enketo_utils import CsrfExemptSessionAuthentication

Device = get_device_model()


class FcmDeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = ()
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        try:
            device = Device.objects.get(dev_id=serializer.data["dev_id"])

        except Device.DoesNotExist:
            device = Device(dev_id=serializer.data["dev_id"])
        device.is_active = True
        device.reg_id = serializer.data["reg_id"]
        username_email = serializer.data["name"]
        if User.objects.filter(email__iexact=username_email).exists():
            device.name = User.objects.get(email__iexact=username_email).email
        elif User.objects.filter(username__iexact=username_email).exists():
            email = User.objects.get(username__iexact=username_email).email
            device.name = email
        else:
            return response.Response(
                {"error": "Invalid Name Received {}".format(username_email)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            device.save()
        except Exception as e:
            return response.Response(
                {"error": "Invalid Fcm Data {}".format(str(e))}, status=status.HTTP_400_BAD_REQUEST)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        try:
            device = Device.objects.get(dev_id=serializer.data["dev_id"])

        except Device.DoesNotExist:
            device = Device(dev_id=serializer.data["dev_id"])
        device.is_active = True
        device.reg_id = serializer.data["reg_id"]
        username_email = serializer.data["name"]
        if User.objects.filter(email__iexact=username_email).exists():
            device.name = User.objects.get(email__iexact=username_email).email
        elif User.objects.filter(username__iexact=username_email).exists():
            email = User.objects.get(username__iexact=username_email).email
            device.name = email
        else:
            return response.Response(
                {"error": "Invalid Name Received {}".format(username_email)}, status=status.HTTP_400_BAD_REQUEST)

        device.save()

    def destroy(self, request, *args, **kwargs):
        try:
            Device.objects.filter(dev_id=kwargs["pk"]).update(is_active=False)
            return response.Response(status=status.HTTP_200_OK)
        except Device.DoesNotExist:
            return response.Response(status=status.HTTP_404_NOT_FOUND)

    def inactivate(self, request):
        try:
            Device.objects.filter(dev_id=request.data.get("dev_id")).update(is_active=False)
            return response.Response(status=status.HTTP_200_OK)
        except Device.DoesNotExist:
            return response.Response(status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
