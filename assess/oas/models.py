from django.db import models


class Teacher(models.Model):
   first_name = models.CharField(max_length=30)
   last_name = models.CharField(max_length=30)
   school = models.CharField(max_length=50)
   email = models.EmailField()
   
   def __unicode__(self):
      return u'%s %s' % (self.first_name, self.last_name)   
   

class Section(models.Model):
   name = models.CharField(max_length=30)
   teacher = models.ForeignKey(Teacher)
   subject = models.CharField(max_length=20)
   section = models.CharField(max_length=30)

   def __unicode__(self):
      return u'%s, %s, %s' % (self.teacher.last_name, self.name, self.section)
   

class Student(models.Model):
   student_id = models.CharField(max_length=50)
   first_name = models.CharField(max_length=30)
   last_name = models.CharField(max_length=30)
   grade = models.IntegerField()
   sex = models.CharField(max_length=1)
   dob = models.DateField()
   school = models.CharField(blank=True, max_length=50)
   email = models.EmailField(blank=True)
   ethnicity = models.CharField(max_length=200)
   
   def __unicode__(self):
      return u'%s, %s' % (self.last_name, self.first_name)
   

class AssessEvent(models.Model):
   student = models.ForeignKey(Student)
   section = models.ForeignKey(Section)
   date = models.DateTimeField()
   location = models.CharField(max_length=40)  # where is the student taking the assessment
   assessment_set = models.CharField(max_length=30)
   
