from django.db import models
from django.contrib.auth.models import User

class TeacherManager(models.Manager):
	def getSchoolChoices(self):
		return [(t['school'], t['school']) for t in self.get_query_set().values('school').distinct()]

class Teacher(models.Model):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	school = models.CharField(max_length=50)
	display_name = models.CharField(max_length=40, help_text="This is the name that students will see. Ex: Mr. Smith, Ms. Jackson") # this would hold: Mr. Weintrop, Ms. Trouille, etc.
	email = models.EmailField()
	owner = models.ForeignKey(User) # manually assigned creator of teacher
	objects = TeacherManager()

	def __unicode__(self):
		return self.first_name + ' ' + self.last_name

class Section(models.Model):
  name = models.CharField(max_length=30, help_text="Ex: 8th Period Physics")
  teacher = models.ForeignKey(Teacher)
  subject = models.CharField(max_length=10, help_text="Ex: Physics, Algebra")
  section = models.CharField(max_length=30, help_text="Ex: 9, 11:30-12")
  
  def __unicode__(self):
		return self.teacher.last_name + ', ' + self.teacher.first_name + ": " + self.name + " section: " + self.section

class Student(models.Model):
	student_id = models.CharField(max_length=50)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	grade = models.IntegerField()
	sex = models.CharField(max_length=1)
	dob = models.DateField()
	school = models.CharField(max_length=50, blank=True)
	email = models.EmailField(blank=True)
	ethnicity = models.CharField(max_length=200)

	def __unicode__(self):
		return self.last_name + ' ' + self.first_name

class AssessEvent(models.Model):
	student = models.ForeignKey(Student)
	section = models.ForeignKey(Section)
	date = models.DateTimeField()					# should this be called start time? do we also want end time? or infer that from the last response?
	location = models.CharField(max_length=40)
	assessment_set = models.CharField(max_length=30) # "Purple Bugs", "HDI", "Warblers", "CPS1", etc.

	def __unicode__(self):
		return self.student.last_name + ': ' + self.assessment_set

class Response(models.Model):
	assess_event = models.ForeignKey(AssessEvent)
	item_name	= models.CharField(max_length=10) 						#"PB1a", "Warb1"  
	response = models.CharField(max_length=400)
 	submitted_at = models.DateTimeField()

 	def __unicode__(self):
 		return self.assess_event.student.last_name + ': ' +self.item_name + ' : ' + self.response
