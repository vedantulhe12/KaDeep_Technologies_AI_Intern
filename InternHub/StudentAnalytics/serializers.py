from rest_framework.serializers import ModelSerializer,Serializer , CharField
from .models import Internship, MatchResult, StudentProfile




class StudentProfileSerializer(ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = '__all__'
        
class InternshipSerializer(ModelSerializer):
    class Meta:
        model = Internship
        fields = '__all__'
        
class MatchResultSerializer(ModelSerializer):
    class Meta:
        model = MatchResult
        fields = '__all__'
        




class MatchRequestSerializer(Serializer):
    student = CharField()
    internship = CharField()

        
        