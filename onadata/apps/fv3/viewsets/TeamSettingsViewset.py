import stripe
from django.conf import settings

from django.contrib.gis.geos import Point
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework import viewsets, status
from rest_framework.views import APIView

from onadata.apps.fieldsight.models import Organization, OrganizationType, COUNTRIES
from onadata.apps.fv3.serializers.TeamSerializer import TeamUpdateSerializer, TeamGeoLayer
from onadata.apps.fsforms.enketo_utils import CsrfExemptSessionAuthentication
from onadata.apps.geo.models import GeoLayer
from onadata.apps.subscriptions.models import Customer, Subscription
from onadata.apps.fv3.role_api_permissions import TeamDashboardPermissions


class TeamViewset(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing team.
    """
    queryset = Organization.objects.all()
    serializer_class = TeamUpdateSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated, TeamDashboardPermissions]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        long = request.data.get('longitude', None)
        lat = request.data.get('latitude', None)
        if lat and long is not None:
            p = Point(round(float(long), 6), round(float(lat), 6), srid=4326)
            instance.location = p
            instance.save()
        instance.logs.create(source=self.request.user, type=13, title="Edit Team",
                                       organization=instance, content_object=instance,
                                       description=u"{0} changed the details of Team named {1}".format(
                                           self.request.user.get_full_name(),
                                           instance.name))

        return Response(status=status.HTTP_200_OK, data=serializer.data)


class TeamGeoLayerViewset(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing geolayer.
    """
    queryset = GeoLayer.objects.all()
    serializer_class = TeamGeoLayer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated, TeamDashboardPermissions]

    def filter_queryset(self, queryset):
        team = self.request.query_params.get('team', None)
        if team:
            try:
                team = Organization.objects.get(id=team)
                return queryset.filter(organization=team)

            except ObjectDoesNotExist:
                return GeoLayer.objects.none()

        return queryset

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        if 'geo_shape_file' not in data:
            data.update({'geo_shape_file': instance.geo_shape_file})

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(status=status.HTTP_200_OK, data=serializer.data)


class TeamOwnerAccount(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated, TeamDashboardPermissions]

    def get(self, request, *args,  **kwargs):

        try:
            team = Organization.objects.get(id=self.kwargs.get('pk'))
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})

        # if request.user == team.owner:
        #
        #     try:
        #         customer = Customer.objects.get(user=self.request.user)
        #         email = customer.user.email
        #     except ObjectDoesNotExist:
        #         return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})
        #     if not customer.stripe_cust_id == 'free_cust_id':
        #         stripe_customer = stripe.Customer.retrieve(customer.stripe_cust_id)
        #         card = stripe_customer.sources.data[0].last4
        #     else:
        #         card = ''
        #         email = ''
        #
        #     subscribed_package = Subscription.objects.select_related('package', 'stripe_customer').get(stripe_customer=customer)
        #     has_free_package = Subscription.objects.filter(stripe_sub_id="free_plan", stripe_customer__user=self.request.user,
        #                                                    organization=team).exists()
        #     if has_free_package:
        #         period_type = 'Year'
        #
        #     else:
        #         period_type = subscribed_package.package.get_period_type_display()
        #
        #     return Response(status=status.HTTP_200_OK, data={'has_free_package': has_free_package, "team_owner": True,
        #                                                      'key': settings.STRIPE_PUBLISHABLE_KEY
        #     if not has_free_package else None, 'subscribed_package': {'plan': subscribed_package.package.get_plan_display(),
        #                                                                             'total_charge': subscribed_package.package.total_charge,
        #                                                                             'period_type': period_type,
        #          'total_submissions': subscribed_package.package.submissions}, 'account_information': {'card': card, 'email': email}
        #                                                      if not has_free_package else None})
        # else:
        return Response(status=status.HTTP_200_OK, data={"team_owner": False})

    def post(self, request, pk, format=None):
        """
          replace old card with new
        """
        try:
            customer = Customer.objects.get(user=request.user).stripe_cust_id
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Not found."})

        stripe.Customer.modify(
            customer,
            source=request.data['stripeToken'],
        )

        stripe_customer = stripe.Customer.retrieve(customer)
        card = stripe_customer.sources.data[0].last4

        return Response(status=status.HTTP_200_OK, data={"detail": "successfully updated.", 'data': card})


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def team_types_countries(request):
    team_types = OrganizationType.objects.values('id', 'name')
    countries = [{'key': c[0], 'value': c[1]} for c in COUNTRIES]

    return Response(data={'team_types': team_types, 'countries': countries}, status=status.HTTP_200_OK)
