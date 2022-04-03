from enum import unique
from getpass import getuser
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from decimal import Decimal
from mutagen.mp4 import MP4
from mutagen.mp4 import MP4StreamInfoError

#from loaders import load_time

import uuid


def load_timer(length:float,type:str='long'): #{
    h = length // 3600
    m = length % 3600 // 60
    s = length % 3600 % 60
    if type=='short':
        return f"{h}h {f'0{m}' if m < 10 else m}m"

    if type=='min':
        return f"{f'0{m}' if m < 10 else m}min"

    else:
        if h>=1:
            return f"{h}:{f'0{m}' if m < 10 else m}:{f'0{round(s)}' if s < 10 else round(s)}"
        else:
            return f"{f'0{m}' if m < 10 else m}:{f'0{round(s)}' if s < 10 else round(s)}"
#}

class Sector(models.Model): #{
    name=models.CharField(max_length=240)
    sectorUUID=models.UUIDField(default=uuid.uuid4, unique=True)
    rlCourses=models.ManyToManyField('Course', blank=True)
    sector_img=models.ImageField(upload_to='sector_image')

    # load path voor IMG's 
    # /media/sector_img/banner.png
    def capture_image_url(self): #{
        #return 'http://localhost:8000'+ settings.MEDIA_ROOT +self.sector_img.url
         return 'http://localhost:8000' + self.sector_img.url
         #}

class Course(models.Model): #{
    title=models.CharField(max_length=255)
    desc=models.TextField()
    createdAt=models.DateTimeField(auto_now_add=True)
    updatedAt=models.DateTimeField(auto_now=True)
    author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    language=models.CharField(max_length=40)
    courseSectionData=models.ManyToManyField('CourseSection', blank=True)
    comments=models.ManyToManyField('Comment', blank=True)
    imageURL=models.ImageField(upload_to='course_imgs') # course_images
    courseUUID=models.UUIDField(default=uuid.uuid4,unique=True) #course_uuid 
    price=models.DecimalField(max_digits=6, decimal_places=2) # 6 = gelijk aan 1k eur met 2 decimale erachter 
                                                              # e.x: 1000,00,- EUR
    
    
    def capture_full_desc(provide): #{
        return provide.desc[:100]

    #}

    def capture_paid_student(provide): #{
        students = get_user_model().objects.filter(courseActivated = provide)
        return len(students)
    #}

    def capture_total_lessons(provide): #{
        lessons = 0
        for x in provide.courseSectionData.all():
            lessons += len(x.episodeData.all())
        return lessons
    #}

    def available_course_length(provide): #{
        length = Decimal(0.0)
        for x in provide.courseSectionData.all():
            for episode in x.episodeData.all():
                length += episode.length
        return load_timer(length, type='short')

        #}
    
    def capture_full_image_url(provide): #{
        return 'http://localhost:8000' + provide.imageURL.url

        #}
#}

class CourseSection(models.Model): #{
    sectionTitle = models.CharField(max_length=255)
    episodeData = models.ManyToManyField('EpisodeCourse', blank=True)

    def total_length(provide): #{
        totalDec = Decimal(0.0)
        for x in provide.episodeData.all():
            totalDec += EpisodeCourse.length
        return load_timer(totalDec, type='min')
    #}

# Onze Course Sectie class vanuit de Model 
#Episode
class EpisodeCourse(models.Model): #{
    title=models.CharField(max_length=255)
    file=models.FileField(upload_to='course_videos')
    length=models.DecimalField(max_digits=10, decimal_places=2)

    def capture_video_length(provide): #{
        try:
            courseVideo = MP4(provide.file)
            return courseVideo.info.length
        except MP4StreamInfoError:
            return 0.0
    #}

    def capture_video_time(provide): #{
        return load_timer(provide.length)
    #}

    def capture_pathURL(provide): #{
        return 'http://localhost:8000' + provide.file.url
    #}

    def save(provide,*args,**kwargs): #{
        provide.length = provide.capture_video_length()
        return super().save(*args, **kwargs)
    #}

class Comment(models.Model): #{
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message=models.TextField()
    createdAt=models.DateTimeField(auto_now_add=True)
    #}
#}