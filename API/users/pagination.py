from rest_framework.pagination import PageNumberPagination


class LostFoundPagination(PageNumberPagination):
    page_size = 27
    page_size_query_param = "page_size"


class ChatPagination(PageNumberPagination):
    page_size = 40
    page_size_query_param = "page_size"
    max_page_size = 40
