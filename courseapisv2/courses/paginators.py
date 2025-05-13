from rest_framework.pagination import PageNumberPagination

class ItemPaginator(PageNumberPagination):
    page_size = 2


class CommentPaginator(PageNumberPagination):
    page_size = 3