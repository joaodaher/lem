from django.db import OperationalError, connections
from mock import patch
from rest_framework import status

from v1 import models
from v1.tests.tests_base import BaseApiTest


class HealthCheckTests(BaseApiTest):
    url = '/healthcheck/'

    def test_healthcheck_returns_200(self):
        result = self.client.get(self.url)
        self.assertEqual(result.status_code, status.HTTP_200_OK)

        self.assertIn('OK', result.json().get('database'))

    def test_healthcheck_db_fail(self):
        conn = connections['default']
        with patch.object(conn.__class__, 'cursor') as mock_method:
            mock_method.side_effect = OperationalError('Mocked database error')

            result = self.client.get(self.url)
            self.assertEqual(result.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
            self.assertIn('ERROR', result.json().get('database'))


class AdminTests(BaseApiTest):
    def test_locale_middleware(self):
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, status.HTTP_302_FOUND)
