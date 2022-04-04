#from xml.etree.ElementTree import Comment
from rest_framework.serializers import Serializer
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from users.userDataSerializer import userSerializer
from .models import Course, Comment, CourseSection, EpisodeCourse

class CourseViewSerializer(ModelSerializer): #{
    #studentID = Serializer.IntegerField(source = 'capture_paid_student')
    studentID = serializers.IntegerField(source='capture_paid_student')
    author = userSerializer()
    img_url = serializers.CharField(source='capture_full_image_url')

    class Meta: #{
        model = Course
        fields = [
            'courseUUID',
            'title',
            'studentID',
            'author', # author is een ForeignKey
            'price',
            'img_url'
        ]
        #}
#}

class CommentSerializer(ModelSerializer): #{rlCourses
    user = userSerializer(read_only=True)
    class Meta: #{
        model = Comment
        exclude = [
            'id',
        ]

        #}

    #}


class EpisodeUnpaidSerializer(ModelSerializer): #{
    length = serializers.CharField(source='capture_video_time')
    class Meta: #{
        model = EpisodeCourse
        exclude = [
            'file'
        ]

        #}
    
    #}
    
class EpisodeActivatedSerializer(ModelSerializer): #{
    length = serializers.CharField(source='capture_video_time')
    class Meta: #{
        model = EpisodeCourse
        fields = [
            'file',
            'length',
            'title'
        ]

    #}


class CourseSectionUnPaidSerializer(ModelSerializer): #{
    episodeData = EpisodeUnpaidSerializer(many=True)
    complete_HR_VID_MAX = serializers.CharField(source='total_length')
    class Meta: #{
        model = CourseSection
        fields = [
            'sectionTitle',
            'episodeData',
            'complete_HR_VID_MAX',
        ]
        #}
    #}
    
class CourseSectionActivatedSerializer(ModelSerializer): #{
    episodeData = EpisodeActivatedSerializer(many=True)
    complete_HR_VID_MAX = serializers.CharField(source='total_length')
    class Meta: #{
        model = CourseSection
        fields = [
            'sectionTitle',
            'episodeData',
            'complete_HR_VID_MAX',
        ]    
        #}
#}


class StudentUnpaidSerializer(ModelSerializer): #{
    # als je geen ManytoManyField wilt gebruiken zet many=False
    comments = CommentSerializer(many=True)
    author = userSerializer()
    courseSectionData = CourseSectionUnPaidSerializer(many=True)
    studentID = serializers.IntegerField(source='capture_paid_student')
    completeLessons = serializers.IntegerField(source='capture_total_lessons')
    completeDuration = serializers.CharField(source='available_course_length')
    image = serializers.CharField(source='capture_full_image_url')

    class Meta: #{
        model = Course
        exclude = [
            'id'
        ]
    #}
#}



class CourseActivatedSerializer(ModelSerializer): #{
    # als je geen ManytoManyField wilt gebruiken zet many=False
    comments = CommentSerializer(many=True)
    author = userSerializer()
    courseSectionData = CourseSectionActivatedSerializer(many=True)
    studentID = serializers.IntegerField(source='capture_paid_student')
    completeLessons = serializers.IntegerField(source='capture_total_lessons')
    completeDuration = serializers.CharField(source='available_course_length')
    image = serializers.CharField(source='capture_full_image_url')

    class Meta: #{
        model = Course
        exclude = [
            'id'
        ]
    

#}


class CourseListSerializer(ModelSerializer): #{
    studentID = serializers.IntegerField(source='capture_paid_student')
    author = userSerializer()
    desc = serializers.CharField(source='capture_full_desc')
    completeLessons = serializers.IntegerField(source='capture_total_lessons')

    class Meta: #{
        model = Course
        fields = [
            'courseUUID',
            'title',
            'studentID',
            'author',
            'price',
            'imageURL',
            'desc',
            'completeLessons'
        ]
        
        #}
    
    #}
