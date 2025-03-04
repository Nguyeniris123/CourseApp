from django.contrib import admin
from django.db.models import Count
from django.template.response import TemplateResponse
from django.utils.safestring import mark_safe
from courses.models import Category, Course, Lesson, Tag
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.urls import path

class MyAdminSite(admin.AdminSite):
    site_header = 'OU course online'

    def get_urls(self):
        return [
            path('course-stats/', self.stats_view)
        ] + super().get_urls()

    def stats_view(self, request):
        stats = Course.objects.annotate(lesson_count=Count('lesson__id')).values('id', 'subject', 'lesson_count')
        return TemplateResponse(request, 'admin/stats_view.html', {
            'stats': stats
        })

admin_site = MyAdminSite(name='admin')

class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Lesson
        fields = '__all__'


class MyLessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'active', 'created_date', 'course_id']
    search_fields = ['subject', 'content']
    list_filter = ['id', 'created_date', 'subject']
    readonly_fields = ['image_view']
    form = LessonForm

    def image_view(self, lesson):
        if lesson:
            return mark_safe(f"<img src = '/static/{lesson.image.name}' width='120' />")


admin_site.register(Category)
admin_site.register(Course)
admin_site.register(Lesson, MyLessonAdmin)
admin_site.register(Tag)
