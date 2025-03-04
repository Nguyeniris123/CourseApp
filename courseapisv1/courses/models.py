from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
class User(AbstractUser):
    avatar = models.ImageField(upload_to='users/%y/%m', null=True)

class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-id']

class Category(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Course(BaseModel):
    subject = models.CharField(max_length=255)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='courses/%y/%m')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('subject', 'category')

    def __str__(self):
        return self.subject

class Lesson(BaseModel):
    subject = models.CharField(max_length=255)
    content = RichTextField()
    image = models.ImageField(upload_to='courses/%y/%m')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    tags =models.ManyToManyField('Tag')

    def __str__(self):
        return self.subject

    class Meta:
        unique_together = ('subject', 'course')

class Tag(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name



