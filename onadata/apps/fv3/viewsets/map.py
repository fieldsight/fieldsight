from rest_framework.views import APIView
from rest_framework.response import Response

from onadata.apps.fieldsight.fs_exports.utils import project_map_data


class ProjectsApi(APIView):
    def get(self, request, format=None):
        """
        Return a list projects.
        """
        df = project_map_data()
        data = df.to_dict(orient='records')
        return Response({'data': data})
