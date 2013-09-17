from django import forms
from oas.models import Teacher

class StudentLoginForm(forms.Form):
		def __init__(self, *args, **kwargs):
			super(StudentLoginForm, self).__init__(*args, **kwargs)
			self.fields['school'] = forms.ChoiceField(choices = ([(t['school'], t['school']) for t in Teacher.objects.values('school').distinct()]))

		student_id = forms.CharField()
		school = forms.CharField(widget=forms.Select)
		# teacher = forms.CharField()
		# section = forms.CharField()
    