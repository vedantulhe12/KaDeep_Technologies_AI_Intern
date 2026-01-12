from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import StudentProfile, Internship, MatchResult
from .serializers import StudentProfileSerializer, InternshipSerializer, MatchResultSerializer , MatchRequestSerializer
from .services import InternHubAIService
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class StudentProfileViewSet(ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    http_method_names = ['get', 'post']

class InternshipViewSet(ModelViewSet):
    queryset = Internship.objects.all()
    serializer_class = InternshipSerializer
    http_method_names = ['get', 'post']

class MatchResultViewSet(ModelViewSet):
    queryset = MatchResult.objects.all()
    serializer_class = MatchResultSerializer
    http_method_names = ['get', 'post']
    
    def create(self, request, *args, **kwargs):
        serializer = MatchRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        student_name = serializer.validated_data["student"]
        internship_name = serializer.validated_data["internship"]

        student = get_object_or_404(StudentProfile, name=student_name)

        company, role = internship_name.split(" - ", 1)
        internship = get_object_or_404(
            Internship,
            company=company.strip(),
            role=role.strip()
        )

        service = InternHubAIService()
        result = service.analyze(student, internship)

        return Response({
            "student": student.name,
            "internship": f"{internship.company} - {internship.role}",
            "version": result.version,
            "match_summary": result.match_summary,
            "skill_gaps": result.skill_gaps,
            "recommendation": result.recommendation_text,
            "ats_score": result.ats_score,
            "generated_resume": result.generated_resume
        })
    def get_serializer_class(self):
        if self.action == "create":
            return MatchRequestSerializer
        return MatchResultSerializer
