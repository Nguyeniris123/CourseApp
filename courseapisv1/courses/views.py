from email.policy import default

from django.template.defaulttags import comment
from rest_framework.decorators import action
from rest_framework.response import Response
from courses.models import Category, Course, Lesson, User
from courses import serializers, paginators
from rest_framework import viewsets, generics, parsers

class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.filter(active=True)
    serializer_class = serializers.CategorySerializer

class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Course.objects.filter(active=True)
    serializer_class = serializers.CourseSerializer
    pagination_class = paginators.CoursePaginator

    def get_queryset(self):
        query =  self.queryset
        q = self.request.query_params.get('q')
        if q:
            query = query.filter(subject__icontains=q)
        cate_id = self.request.query_params.get('category_id')
        if cate_id:
            query = query.filter(category_id=cate_id)
        return query

    @action(methods=['get'], url_path='lessons', detail=True)
    def get_lessons(sefl, request, pk):
        lessons = sefl.get_object().lesson_set.filter(active=True)
        return Response(serializers.LessonSerializer(lessons, many=True).data)

class LessonViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Lesson.objects.prefetch_related('tags').filter(active=True)
    serializer_class = serializers.LessonDetailSerializer

    @action(methods=['get'], url_path='comments', detail=True)
    def get_comments(self, request, pk):
        comments = self.get_object().comment_set.select_related('user').filter(active=True)
        return Response(serializers.CommentSerializer(comments, many=True).data)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser]
