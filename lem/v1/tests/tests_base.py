from rest_framework.test import APITransactionTestCase


class FieldFactoryMixin:
    pass


class ModelFactoryMixin(FieldFactoryMixin):
    pass


class BaseApiTest(ModelFactoryMixin, APITransactionTestCase):
    def assertFieldInResponse(self, members, response, fields=None):
        def _create_key(item):
            return '#'.join([str(item.get(field)) for field in fields])

        if not fields:
            fields = ['id']

        data = response.data
        try:
            results = data['results']
        except KeyError:
            results = [data]

        pks = [_create_key(item=r) for r in results]

        if not isinstance(members, list):
            members = [members]
        for member in members:
            pk = _create_key(item=member)
            self.assertIn(pk, pks)
            pks.remove(pk)
        self.assertEqual(any(pks), False)
