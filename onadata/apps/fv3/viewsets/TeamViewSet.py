from datetime import datetime
import dateutil.relativedelta

import stripe

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.gis.geos import Point
from django.db.models import Prefetch

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, permission_classes

from onadata.apps.eventlog.models import CeleryTaskProgress
from onadata.apps.fsforms.tasks import clone_form

from onadata.apps.fv3.serializers.TeamSerializer import TeamSerializer, TeamProjectSerializer
from onadata.apps.fv3.serializer import ProjectUpdateSerializer
from onadata.apps.fieldsight.models import Organization, Project, Region, SiteType, Site
from onadata.apps.fv3.role_api_permissions import TeamDashboardPermissions
from onadata.apps.subscriptions.models import Customer, Package, Subscription
from onadata.apps.fsforms.enketo_utils import CsrfExemptSessionAuthentication
from onadata.apps.userrole.models import UserRole
from onadata.apps.fsforms.models import FInstance


class TeamDashboardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated, TeamDashboardPermissions]

    def get_queryset(self):
        return self.queryset

    def get_serializer_context(self):
        context = {'request': self.request}

        return context


class TeamProjectsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = TeamProjectSerializer
    permission_classes = [IsAuthenticated, TeamDashboardPermissions]

    def get_queryset(self):
        return self.queryset.prefetch_related(Prefetch(
            'project_roles',
            queryset=UserRole.objects.filter(ended_at=None).distinct('user')
        ), Prefetch(
            'project_instances',
            queryset=FInstance.objects.filter(is_deleted=False)

        ), Prefetch(
            'project_region',
            queryset=Region.objects.filter(is_active=True, parent__isnull=True)
        ), Prefetch(
            'sites',
            queryset=Site.objects.filter(is_active=True, is_survey=False, site__isnull=True)
        )).filter(organization=self.kwargs.get('pk'), is_active=True)

    def list(self, request, *args, **kwargs):
        projects = self.serializer_class(self.get_queryset(), many=True).data
        team = Organization.objects.get(id=self.kwargs.get('pk'))

        data = {'projects': projects, 'breadcrumbs': {'name': 'Projects', 'team': team.name,
                                                      'team_url': team.get_absolute_url()}}

        return Response(data)


# class StripeSubscriptions(APIView):
#
#     authentication_classes = (CsrfExemptSessionAuthentication, SessionAuthentication, IsAuthenticated)
#     permission_classes = [TeamDashboardPermissions, ]
#
#     def post(self, request, pk, format=None):
#         try:
#             organization = Organization.objects.get(id=pk)
#
#         except ObjectDoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#         customer_data = {
#             'email': request.user.email,
#             'description': 'Some Customer Data',
#             'card': request.data['stripeToken'],
#             'metadata': {'username': request.user.username}
#         }
#
#         customer = stripe.Customer.create(**customer_data)
#         cust = Customer.objects.get(user=request.user)
#         cust.stripe_cust_id = customer.id
#         cust.save()
#
#         stripe_customer = stripe.Customer.retrieve(cust.stripe_cust_id)
#         card = stripe_customer.sources.data[0].last4
#
#         period = request.data['interval']
#
#         starting_date = datetime.now().strftime('%A, %B %d, %Y')
#         if period == 'yearly':
#             overage_plan = settings.YEARLY_PLANS_OVERRAGE[request.data['plan_name']]
#             selected_plan = settings.YEARLY_PLANS[request.data['plan_name']]
#             package = Package.objects.get(plan=settings.PLANS[selected_plan], period_type=2)
#             ending_date = datetime.now() + dateutil.relativedelta.relativedelta(months=12)
#             plan_name = YEARLY_PLAN_NAME[request.data['plan_name']]
#
#         elif period == 'monthly':
#             overage_plan = settings.MONTHLY_PLANS_OVERRAGE[request.data['plan_name']]
#             selected_plan = settings.MONTHLY_PLANS[request.data['plan_name']]
#             package = Package.objects.get(plan=settings.PLANS[selected_plan], period_type=1)
#             ending_date = datetime.now() + dateutil.relativedelta.relativedelta(months=1)
#             plan_name = MONTHLY_PLAN_NAME[request.data['plan_name']]
#
#         try:
#
#             sub = customer.subscriptions.create(
#                 items=[
#                     {
#                         'plan': selected_plan,
#
#                     },
#
#                     {
#                         'plan': overage_plan,
#                     },
#
#                 ],
#
#             )
#         except Exception as e:
#             return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'No such plan in stripe.'})
#         sub_data = {
#             'stripe_sub_id': sub.id,
#             'is_active': True,
#             'initiated_on': datetime.now(),
#             'package': Package.objects.get(plan=settings.PLANS[selected_plan]),
#             'organization': organization
#
#         }
#         try:
#             # Subscription.objects.create(**sub_data)
#             Subscription.objects.filter(stripe_customer=cust, stripe_sub_id="free_plan").update(**sub_data)
#
#         except Exception as e:
#             return Response(status=status.HTTP_204_NO_CONTENT, data={'error': str(e)})
#
#         return Response(status=status.HTTP_201_CREATED, data={'organization': organization.name,
#                                                               'submissions': package.submissions,
#                                                               'amount': package.total_charge,
#                                                               'starting_date': starting_date,
#                                                               'ending_date': ending_date.strftime('%A, %B %d, %Y'),
#                                                               'card': card,
#                                                               'plan_name': plan_name,
#                                                               })
#

class AddTeamProjectViewset(viewsets.ModelViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated, TeamDashboardPermissions]
    serializer_class = ProjectUpdateSerializer

    def list(self, request, *args, **kwargs):
        team_id = self.kwargs.get('pk')
        team = Organization.objects.get(id=team_id)
        location = team.location
        team = Organization.objects.get(id=team_id)
        breadcrumbs = {'current_page': 'Create Project', 'name': team.name, 'name_url': team.get_absolute_url()}
        data = {'location': str(location), 'breadcrumbs': breadcrumbs}

        return Response(data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)

        task_obj = CeleryTaskProgress.objects.create(user=request.user,
                                                     description="Auto Clone and Deployment of Forms",
                                                     task_type=15, content_object=instance.organization)
        clone_form.delay(instance.id, task_obj.id)
        longitude = request.data.get('longitude', None)
        latitude = request.data.get('latitude', None)

        if latitude and longitude is not None:
            p = Point(round(float(longitude), 6), round(float(latitude), 6), srid=4326)
            instance.location = p
            instance.save()

        noti = instance.logs.create(source=self.request.user, type=10, title="new Project",
                                       organization=instance.organization, content_object=instance,
                                       description=u'{0} created new project '
                                                   u'named {1}'.format(
                                           self.request.user.get_full_name(), instance.name))

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()


@permission_classes([IsAuthenticated, ])
@api_view(['GET'])
def team_regions_types(request, pk):
    try:
        team = Organization.objects.get(id=pk, is_active=True)

    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data="Not found")

    regions = Region.objects.filter(project__organization__id=team.id, is_active=True).select_related('project')
    regions_data = [{'id': reg.id, 'identifier': reg.identifier, 'name': reg.name, 'project_id': reg.project.id,
                     'project_name': reg.project.name} for reg in regions]
    site_types = SiteType.objects.filter(project__organization__id=team.id, deleted=False).select_related('project')
    site_types_data = [{'id': si_type.id, 'identifier': si_type.identifier, 'name': si_type.name, 'project_id': si_type.project.id,
                     'project_name': si_type.project.name} for si_type in site_types]
    data = {'regions': regions_data, 'site_types': site_types_data}

    return Response(status=status.HTTP_200_OK, data=data)
