from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from onadata.apps.fsforms.enketo_utils import CsrfExemptSessionAuthentication
from rest_framework.response import Response
from django.utils.translation import ugettext as _
from onadata.apps.fsforms.models import FieldSightXF
from onadata.apps.fv3.serializers.KoboExportSerializer import ExportSerializer
from onadata.apps.viewer.models import Export
from onadata.apps.viewer.tasks import create_async_export


class ExportViewSet(viewsets.ModelViewSet):
    queryset = Export.objects.all()
    serializer_class = ExportSerializer
    authentication_classes = [CsrfExemptSessionAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        params = self.request.query_params
        id = params.get('id')
        fsxf = params.get('fsxf')
        is_project = params.get('is_project')
        version = params.get('version')
        if not (id and fsxf and is_project):
            return []
        if is_project in ["1", True]:
            self.queryset = self.queryset.filter(fsxf=fsxf)
        else:
            self.queryset = self.queryset.filter(fsxf=fsxf, site=id)
        if version:
            return self.queryset.filter(version=version)
        return self.queryset

    def create(self, request, *args, **kwargs):
        params = self.request.query_params
        id = params.get('id')
        fsxf = params.get('fsxf')
        is_project = params.get('is_project')
        version = params.get('version', 0)
        if not (id and fsxf and is_project):
            return Response({'error': 'Parameters missing'},status=status.HTTP_400_BAD_REQUEST)
        fsxf = FieldSightXF.objects.get(pk=fsxf)
        if is_project == 1 or is_project == '1':
            site_id = 0
            query = {"fs_project_uuid": str(fsxf)}
        else:
            site_id = id
            if fsxf.site:
                query = {"fs_uuid": str(id)}
            else:
                query = {"fs_project_uuid": str(id), "fs_site": site_id}
        force_xlsx = True
        if version not in ["0", 0]:
            query["__version__"] = version
        deleted_at_query = {
            "$or": [{"_deleted_at": {"$exists": False}},
                    {"_deleted_at": None}]
        }
        # join existing query with deleted_at_query on an $and
        query = {"$and": [query, deleted_at_query]}
        print("query at excel generation", query)

        # export options
        group_delimiter = request.POST.get("options[group_delimiter]", '/')
        if group_delimiter not in ['.', '/']:
            return Response({'error': _("%s is not a valid delimiter" % group_delimiter)}, status=status.HTTP_400_BAD_REQUEST)

        # default is True, so when dont_.. is yes
        # split_select_multiples becomes False
        split_select_multiples = request.POST.get(
            "options[dont_split_select_multiples]", "no") == "no"

        binary_select_multiples = False
        # external export option
        meta = request.POST.get("meta")
        options = {
            'group_delimiter': group_delimiter,
            'split_select_multiples': split_select_multiples,
            'binary_select_multiples': binary_select_multiples,
            'meta': meta.replace(",", "") if meta else None
        }

        create_async_export(fsxf.xform, 'xls', query, force_xlsx, options, is_project, id, site_id , version, False)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
