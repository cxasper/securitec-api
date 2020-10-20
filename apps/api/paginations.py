from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 15


class CustomPagination(PageNumberPagination):
    page = DEFAULT_PAGE
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'page_size'

    def __to__(self):
        if self.get_current_page() == self.page.paginator.num_pages:
            return self.get_basic_count() + self.get_count_list()
        return self.get_count_list() * self.get_current_page()

    def __from__(self):
        if self.get_current_page() <= 1:
            return 1
        return self.get_basic_count() + 1

    def get_basic_count(self):
        return self.get_page_size(self.request) * (self.get_current_page() - 1)

    def get_current_page(self):
        return int(self.request.GET.get('page', DEFAULT_PAGE))

    def get_count_list(self):
        return len(self.page.object_list)

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'last_page': self.page.paginator.num_pages,
            'current_page': self.get_current_page(),
            'page_size': self.get_page_size(self.request),
            'total_items': self.page.paginator.count,
            'from': self.__from__(),
            'to': self.__to__(),
            'results': data
        })
