from django.contrib import admin
from oas.models import Teacher, Section, Student, AssessEvent


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'school', 'email')
    
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'last_name', 'first_name', 'school', 'email')
    
    
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Section)
admin.site.register(AssessEvent)

