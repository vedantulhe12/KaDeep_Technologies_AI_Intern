from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentProfileViewSet, InternshipViewSet, MatchResultViewSet

router = DefaultRouter()
router.register(r'student-profiles', StudentProfileViewSet, basename='studentprofile')
router.register(r'internships', InternshipViewSet, basename='internship')
router.register(r'match-results', MatchResultViewSet, basename='matchresult')
urlpatterns = [
    path('', include(router.urls)),
]