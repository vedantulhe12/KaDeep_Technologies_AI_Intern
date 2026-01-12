from django.contrib import admin
from .models import StudentProfile, Internship, MatchResult
# Register your models here.

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('created_at',)
    
@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ('company', 'role', 'location', 'stipend', 'created_at')
    search_fields = ('company', 'role', 'location')
    list_filter = ('created_at',)
    
@admin.register(MatchResult)
class MatchResultAdmin(admin.ModelAdmin):
    list_display = ('student__name', 'internship', 'ats_score', 'created_at')
    search_fields = ('student__name', 'internship__company', 'internship__role')
    list_filter = ('created_at',)
    
    