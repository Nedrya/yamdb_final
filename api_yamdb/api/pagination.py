from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ApiPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {},
            'count': self.page.paginator.count,
            'response': data
        })
