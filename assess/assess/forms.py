from django import forms
from oas.models import Teacher

class StudentLoginForm(forms.Form):
		student_id = forms.CharField()
		school = forms.ChoiceField(choices = Teacher.objects.getSchoolChoices())
		# teacher = forms.CharField()
		# section = forms.CharField()

class StudentRegistrationForm(forms.Form):
		def __init__(self, *args, **kwargs):
			super(StudentRegistrationForm, self).__init__(*args, **kwargs)
			self.fields['grade'] = forms.ChoiceField(choices = [(9, '9th grade'), (10, '10th grade'), (11, '11th grade'), (12, '12th grade')])
			self.fields['sex'] = forms.ChoiceField(choices = [('M', 'Male'), ('F', 'Female'), ('other', 'Other')])

		student_id = forms.CharField()
		school = forms.CharField()
		first_name = forms.CharField()
		last_name = forms.CharField()
		date_of_birth = forms.DateField() #, attrs={'pattern': 'mm/dd/yyyy'})
		grade = forms.CharField(widget=forms.Select)
		sex = forms.CharField(widget=forms.Select)
		email = forms.EmailField()
		ethnicity = forms.CharField()
		section_id = forms.IntegerField()
		assessment_set = forms.CharField()
		location = forms.CharField()



    