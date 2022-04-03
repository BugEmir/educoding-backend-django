from django.http import HttpResponseBadRequest
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status 
from courses.models import Course, Sector
from .dataserializers import CourseViewSerializer
from .dataserializers import StudentUnpaidSerializer
from .dataserializers import CourseListSerializer


# EduCoding views index
class CoursesHub(APIView):
    
    def get(provide, request, *args, **kwargs):
        # Dit gaat onze string randomizen (Courses)
        sectorsCourse = Sector.objects.order_by("?")[:6]
        sectorResp = []

        for x in sectorsCourse:
            sectorCrs = x.rlCourses.order_by("?")[:4]
            dataSerializer = CourseViewSerializer(sectorCrs,many=True)

        sectorObject = {
            'sectorName':x.name,
            'sectorUUID':x.sectorUUID,
            'featuredCrs':dataSerializer.data,
            'sector_img':x.capture_image_url()
        }

        sectorResp.append(sectorObject)
    
        return Response(data = sectorResp, status = status.HTTP_200_OK)


# EduCoding information page voor cursussen
class CourseInstruct(APIView):
    def get(provide, request, courseUUID, *args, **kwargs):
        course = Course.objects.filter(courseUUID=courseUUID)

        if not course:
            return HttpResponseBadRequest('Oeps, deze cursus bestaat (nog) niet.')

        # serialize data die we sturen naar onze frontend
        serialized = StudentUnpaidSerializer(course[0])
        return Response(data = serialized.data, status = status.HTTP_200_OK)


 
class SectorGroupingCourse(APIView): #{
    def get(provide, request, sectorUUID, *args, **kwargs): #{
        sector = Sector.objects.filter(sectorUUID=sectorUUID)

        if not sector:
            return HttpResponseBadRequest('Oeps, deze onderdeel bestaat (nog) niet.')
        
        sectorCourse = sector[0].rlCourses.all()
        #serialize data die we sturen naar onze frontend
        serialized = CourseListSerializer(sectorCourse, many=True)

        completeStudents = 0
        for x in sectorCourse: #{
            completeStudents += x.capture_paid_student()
            #respons JSON object naar frontend
        return Response({
            'data':serialized.data,
            'sectorName':sector[0].name,
            'completeStudent':completeStudents,
        },status=status.HTTP_200_OK)
        
        #}
    #}
#}


#class SearchCourse(APIView):
  #  def get(provide, request, searchString):
        #matches = 
        #searchbar afmaken 
        # serializer maken voor searchbar