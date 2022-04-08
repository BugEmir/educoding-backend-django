from django.contrib import admin
from .models import Course, Sector, CourseSection, EpisodeCourse, Comment

admin.site.register(Course)
admin.site.register(Sector)
admin.site.register(CourseSection)
admin.site.register(EpisodeCourse)
admin.site.register(Comment)

