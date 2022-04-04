from nis import match
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from simplejson import JSONDecodeError 
from courses.models import Course, Sector
from users.models import User
from .dataserializers import CommentSerializer
from .dataserializers import CourseViewSerializer
from .dataserializers import StudentUnpaidSerializer
from .dataserializers import CourseListSerializer
from .dataserializers import ProductSerializer
from .dataserializers import CourseActivatedSerializer
from django.db.models import Q
from decimal import Decimal

import json
import time


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


# Search class toegevoegd (zonder Serializer)
class SearchCourse(APIView): #{
    def get(self, request, searchWords_lookup_from_q): #{
        #print(searchWords_lookup_from_q)
        matches = Course.objects.filter(Q(title__icontains=searchWords_lookup_from_q) | Q(desc__icontains=searchWords_lookup_from_q))
        #print(matches)
        serialized = CourseListSerializer(matches, many = True)
        return Response(data = serialized.data, status = status.HTTP_200_OK)
        #}
#}



class CommentOnCourse(APIView): #{
    def post(self, request, courseUUID): #{
        try:
            course = Course.objects.get(courseUUID = courseUUID)
        except Course.DoesNotExist:
            return HttpResponseBadRequest("Cursus bestaat nog niet.")
        try:
            courseContent = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return Response("Plaats een reactie", status = status.HTTP_400_BAD_REQUEST)

        #courseContent = json.loads(request.body)

        if not courseContent.get('message'):
            return Response(status = status.HTTP_400_BAD_REQUEST)
        
        serialized = CommentSerializer(data = courseContent)

        if serialized.is_valid():
            # nog geen authenticatie systeem
            author = User.objects.get(id=1)
            comments = serialized.save(user = author)
            #comment = serialized.save(user = request.user)
            course.comments.add(comments)
            return Response(status = status.HTTP_201_CREATED)
        else:
            return Response(data = serialized.errors, status = status.HTTP_400_BAD_REQUEST)

        #}
    
    #}

# CaptureBagDetail
class CaptureBagDetail(APIView): #{
    def post(self, request): #{
        try:
            body_data = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return HttpResponseBadRequest()

        if type(body_data.get('cart')) != list: #{
            return HttpResponseBadRequest()
        #}

        if len(body_data.get('cart')) == 0: #{
            return Response([])
        #}

        coursesList = []
        for x in body_data.get('cart'): #{
            cartItem = Course.objects.filter(courseUUID = x)
            
            if not cartItem:
                return HttpResponseBadRequest()
            coursesList.append(cartItem[0])

        serialized = ProductSerializer(coursesList, many = True)
        totalCalculateCart = Decimal(0.00)
        #}
        for x in serialized.data:
            totalCalculateCart += Decimal(x.get('price'))
        return Response(data = {
            'cartInfo':serialized.data,
            'totalCalculateCart':totalCalculateCart
        }, status = status.HTTP_200_OK)
            
    #}

#}


class CourseView(APIView): #{
    def get(self, request, courseUUID): #{
        try:
            course = Course.objects.get(courseUUID = courseUUID)
        except Course.DoesNotExist:
            return HttpResponseBadRequest("Cursus bestaat (nog) niet.")

        
        request.user = User.objects.get(id=1)
      
        # idk of dit werkt met user.* en filteren met course UUID
        userCourseActivated = request.user.courseActivated.filter(courseUUID = courseUUID)
        
        if not userCourseActivated:
            return HttpResponseNotAllowed("U heeft deze cursus niet gekocht.")
        # hmm onthoud deze
        serialized = CourseActivatedSerializer(course)
        
        return Response(serialized.data, status.HTTP_200_OK)
        
    #}
            
    

#}
