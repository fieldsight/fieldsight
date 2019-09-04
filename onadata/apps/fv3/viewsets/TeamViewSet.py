from datetime import datetime
import dateutil.relativedelta

import stripe

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from onadata.apps.fv3.serializers.TeamSerializer import TeamSerializer, TeamProjectSerializer
from onadata.apps.fieldsight.models import Organization, Project
from onadata.apps.fv3.role_api_permissions import TeamDashboardPermissions
from onadata.apps.subscriptions.models import Customer, Package, Subscription
from onadata.apps.subscriptions.views import MONTHLY_PLAN_NAME, YEARLY_PLAN_NAME


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
        return self.queryset.filter(organization=self.kwargs.get('pk'), is_active=True)

    def list(self, request, *args, **kwargs):
        projects = self.serializer_class(self.get_queryset(), many=True).data
        team = Organization.objects.get(id=self.kwargs.get('pk'))

        data = {'projects': projects, 'breadcrumbs': {'name': 'Projects', 'team': team.name,
                                                      'team_url': team.get_absolute_url()}}

        return Response(data)


@api_view(['POST'])
def subscriptions(request, org_id):
    try:
        organization = Organization.objects.get(id=org_id)

    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    customer_data = {
        'email': request.user.email,
        'description': 'Some Customer Data',
        'card': request.POST['stripeToken'],
        'metadata': {'username': request.user.username}
    }

    customer = stripe.Customer.create(**customer_data)
    cust = Customer.objects.get(user=request.user)
    cust.stripe_cust_id = customer.id
    cust.save()

    stripe_customer = stripe.Customer.retrieve(cust.stripe_cust_id)
    card = stripe_customer.sources.data[0].last4

    period = request.POST['interval']

    starting_date = datetime.now().strftime('%A, %B %d, %Y')
    if period == 'yearly':
        overage_plan = settings.YEARLY_PLANS_OVERRAGE[request.POST['plan_name']]
        selected_plan = settings.YEARLY_PLANS[request.POST['plan_name']]
        package = Package.objects.get(plan=settings.PLANS[selected_plan], period_type=2)
        ending_date = datetime.now() + dateutil.relativedelta.relativedelta(months=12)
        plan_name = YEARLY_PLAN_NAME[request.POST['plan_name']]

    elif period == 'monthly':
        overage_plan = settings.MONTHLY_PLANS_OVERRAGE[request.POST['plan_name']]
        selected_plan = settings.MONTHLY_PLANS[request.POST['plan_name']]
        package = Package.objects.get(plan=settings.PLANS[selected_plan], period_type=1)
        ending_date = datetime.now() + dateutil.relativedelta.relativedelta(months=1)
        plan_name = MONTHLY_PLAN_NAME[request.POST['plan_name']]

    try:

        sub = customer.subscriptions.create(
            items=[
                {
                    'plan': selected_plan,

                },

                {
                    'plan': overage_plan,
                },

            ],

        )
    except Exception as e:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'No such plan in stripe.'})
    sub_data = {
        'stripe_sub_id': sub.id,
        'is_active': True,
        'initiated_on': datetime.now(),
        'package': Package.objects.get(plan=settings.PLANS[selected_plan]),
        'organization': organization

    }
    try:
        # Subscription.objects.create(**sub_data)
        Subscription.objects.filter(stripe_customer=cust, stripe_sub_id="free_plan").update(**sub_data)

    except Exception as e:
        return Response(status=status.HTTP_204_NO_CONTENT, data={'error': str(e)})

    return Response(status=status.HTTP_201_CREATED, data={'organization': organization,
                                                              'submissions': package.submissions,
                                                              'amount': package.total_charge,
                                                              'starting_date': starting_date,
                                                              'ending_date': ending_date.strftime('%A, %B %d, %Y'),
                                                              'card': card,
                                                              'plan_name': plan_name,
                                                              })
