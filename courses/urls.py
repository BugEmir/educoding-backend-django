from django.urls import path
from django.urls import include
from courses.views import CoursesHub 
from courses.views import CourseInstruct
from courses.views import SearchCourse 
from courses.views import SectorGroupingCourse
from courses.views import CommentOnCourse
from courses.views import CaptureBagDetail
from courses.views import CourseView
# EduCoding Routing schema

urlpatterns = [
    #indexpage endpoint route
    path('', CoursesHub.as_view()),
    #informatie per cursus endpoint route
    path('information/<uuid:courseUUID>/', CourseInstruct.as_view()),
    #cursussen in sectoren ophalen endpoint route (Course Lijst)
    path('<uuid:sectorUUID>/', SectorGroupingCourse.as_view()),
    # search functie van course lijst endpoint
    path('search/<str:searchWords_lookup_from_q>/', SearchCourse.as_view()),
    # comment op cursus functie endpoint
    path('comment/<courseUUID>/', CommentOnCourse.as_view()),
    # winkelwagen endpoint
    path('bag/', CaptureBagDetail.as_view()),
    # Course check endpoint
    path('study/<uuid:courseUUID>/', CourseView.as_view())
]