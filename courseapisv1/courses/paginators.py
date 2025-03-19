from rest_framework import pagination

class CoursePaginator(pagination.PageNumberPagination):
    page_size = 6

class CommentPaginator(pagination.PageNumberPagination):
    page_size = 2