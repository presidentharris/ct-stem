from django.contrib import admin
from oas.models import Teacher, Section, Student, AssessEvent

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'school', 'email')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'school', 'student_id')

admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Section)
admin.site.register(Student, StudentAdmin)
admin.site.register(AssessEvent)
# admin.site.register(Response)

