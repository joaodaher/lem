from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheck(APIView):
    SUCCESS = 'OK'
    ERROR = 'ERROR'

    def get(self, request):
        db = self._check_db()

        error = self.ERROR in db
        r_status = status.HTTP_200_OK if not error else status.HTTP_503_SERVICE_UNAVAILABLE

        return Response(
            data={
                'database': db,
            },
            status=r_status,
        )

    def _check_db(self):
        from django.db import connections
        from django.db.utils import OperationalError
        db_conn = connections['default']
        try:
            db_conn.cursor()
            message = self.SUCCESS
        except OperationalError as e:
            message = '{}: {}'.format(self.ERROR, str(e))
        return message
