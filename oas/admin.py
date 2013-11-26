import csv
from django.contrib import admin
# from django.core import serializers
from django.http import HttpResponse
from oas.models import Teacher, Section, Student, AssessEvent, Response


class TeacherAdmin(admin.ModelAdmin):
  list_display = ('first_name', 'last_name', 'school', 'email')
  list_filter = ('school',)
  # actions = ['export_uni1_by_teacher']

  # def export_uni1_by_teacher(modeladmin, request, queryset):
 	# 	# response = HttpResponse(content_type="application/json")
 	# 	# serializers.serialize("json", queryset, stream=response)

		# response = HttpResponse(content_type='text/csv')
		# writer = csv.writer(response)
		# writer.writerow(['teacher', 'school', 'blah'])
		# for t in queryset:
		# 	teach_info = [t.first_name, t.last_name]
		# 	sections = Section.objects.filter(teacher=t)
		# 	for s in sections:
		# 		sec_info = [s.name, s.subject, s.section]
		# 		assessmevents = AssessEvent.objects.filter(section=s, assessment_set='UNI1')
		# 		for a in assessmevents:
		# 			a_info = [a.student.student_id, a.student.last_name, a.date, a.assessment_set, a.location ]
		# 			responses = Response.objects.filter(assess_event=a).order_by("item_name")
		# 			for r in responses:
		# 				a_info.append(r.response)
		# 			writer.writerow(teach_info + sec_info + a_info)

		# response['Content-Disposition'] = 'attachment; filename="responses_by_teacher.csv"'

		# return response

class SectionAdmin(admin.ModelAdmin):
	list_display = ('teacher', 'name', 'subject', 'section')
	list_filter = ('subject', 'teacher')

class StudentAdmin(admin.ModelAdmin):
  list_display = ('first_name', 'last_name', 'school', 'student_id')
  list_filter = ('school',)

class AssessEventAdmin(admin.ModelAdmin):
	list_display = ('section', 'assessment_set', 'student', 'date')
	list_filter = ('date', 'assessment_set', 'section')
	actions = ['export_responses']

	def export_responses(modeladmin, request, queryset):
		response = HttpResponse(content_type='text/csv')
		writer = csv.writer(response)
		header_pt1 = ['school', 'teacher f_name', 'teacher l_name', 'section name', 'subject', 'section', 'student ID', 'student fname', 'student lname', 'grade', 'sex', 'dob', 'ethnicity', 'assessment date', 'assessment set', 'location']

		has_header = False

		for a in queryset:
			t = a.section.teacher
			sec = a.section
			st = a.student
			a_info = [t.school, t.first_name, t.last_name, sec.name, sec.subject, sec.section, st.student_id, st.first_name, st.last_name, st.grade, st.sex, st.dob, st.ethnicity, a.date, a.assessment_set, a.location ]
			responses = Response.objects.filter(assess_event=a).order_by("item_name")
			item_names = []
			for r in responses:
				item_names.append(r.item_name)
				a_info.append(r.response)
			if not has_header:
				writer.writerow(header_pt1 + item_names)
				has_header = True
			writer.writerow([unicode(a).encode("utf-8") for a in a_info])
		response['Content-Disposition'] = 'attachment; filename="responses.csv"'

		return response

class ResponseAdmin(admin.ModelAdmin):
	list_display = ('assess_event', 'item_name', 'response')
	list_filter = ('item_name',)


admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(AssessEvent, AssessEventAdmin)
admin.site.register(Response, ResponseAdmin)

