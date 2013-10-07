from django.shortcuts import render
from django.http import HttpResponse
from oas.models import Student, Section, Teacher, AssessEvent, Response
from forms import StudentRegistrationForm

import datetime
import json

ASSESSMENTS = {'PB' : 'purple_bugs.html', 'WARB' : 'warblers.html', 'HDI' : 'HDI.html', 'CPS1' : 'cps1.html'}

def student_login(request):
    schools = Teacher.objects.values('school').distinct()
    teachers = Teacher.objects.all().order_by("last_name")
    return render(request, 'student_login.html', {'schools':schools, 'teachers':teachers})

def get_data(request, table):
    if 'filter' in request.GET:
        inFilter = request.GET['filter']
        if table == 'Teacher':
            teachers = Teacher.objects.filter(school=inFilter).order_by("last_name")
            data_json = [(t.id, t.display_name) for t in teachers]
        elif table == 'Section':
            teacher = Teacher.objects.get(id=inFilter)
            sections = Section.objects.filter(teacher=teacher)
            data_json = [(s.id, s.subject + ' ' + s.section) for s in sections]
        return HttpResponse(json.dumps({'table' : table, 'values': data_json}), mimetype="application/json")
    else:
        return HttpResponse(table)

def student_status(request):
    errors = []
    if 'student_id' not in request.POST or not request.POST['student_id']:
        errors.append('Please enter your student ID.')
    if 'school' not in request.POST or not request.POST['school']:
        errors.append('Please select your school.')
    if 'teacher' not in request.POST or not request.POST['teacher']:
        errors.append('Please select your teacher.')
    if 'section' not in request.POST or not request.POST['section']:
        errors.append('Please select your current section.')
    if 'assessment_set' not in request.POST or not request.POST['assessment_set']: 
        errors.append('Please select the assessment set you want to take.')
    if 'location' not in request.POST or not request.POST['location']: 
        errors.append('Please specifcy your current location.')

    if errors:
        #TODO: figure out how to reuse the student_login method
        schools = Teacher.objects.values('school').distinct()
        teachers = Teacher.objects.all().order_by("last_name")
        return render(request, 'student_login.html', {'schools':schools, 'teachers':teachers, 'errors':errors})

    try:
        student_id = request.POST['student_id']
        section = Section.objects.get(id=request.POST['section'])
        student = Student.objects.get(student_id=student_id, school=section.teacher.school)        

        assessmevent = AssessEvent (
            student = student,
            section = section,
            date = datetime.datetime.now(),
            location = request.POST['location'],
            assessment_set = request.POST['assessment_set']
            )
        assessmevent.save()

        # how are we going to decide which assessment student should take? Maybe an intermediate page that says: hi {{name}} welcome back, please choose the assessment you'd like to take.
        return render(request, 'sets/' + ASSESSMENTS[assessmevent.assessment_set], {'assessmevent': assessmevent})

    except Student.DoesNotExist:
        registration_form = StudentRegistrationForm(
            initial={'student_id' : student_id, 'school' : section.teacher.school, 'section_id' : section.id, 'assessment_set': request.POST['assessment_set'], 'location' : request.POST['location']}
            )
        return render(request, 'student_registration.html', {'form': registration_form, 'section': section})
    except Exception as e:
        errors.append("An error occured, please verify your information and try again.")
        return render(request, 'student_login.html', {'errors': errors, 'e':e})

def student_register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            in_data = form.cleaned_data

            if ( not Student.objects.filter(student_id=in_data['student_id'], school=in_data['school'])):
                #create student!
                student = Student(
                    student_id=in_data['student_id'],
                    first_name=in_data['first_name'],
                    last_name=in_data['last_name'],
                    grade=in_data['grade'],
                    sex=in_data['sex'],
                    dob=in_data['date_of_birth'],
                    school=in_data['school'],
                    email=in_data['email'],
                    ethnicity=in_data['ethnicity'])

                student.save()
            else:
                student = Student.objects.get(student_id=in_data['student_id'], school=in_data['school'])

            section = Section.objects.get(id=in_data['section_id'])
            assessmevent = AssessEvent (
                student = student,
                section = section,
                date = datetime.datetime.now(),
                location = in_data['location'],
                assessment_set = in_data['assessment_set']
                )
            assessmevent.save()
            return render(request, 'sets/' + ASSESSMENTS[assessmevent.assessment_set], {'assessmevent': assessmevent})
        else:
            return render(request, 'student_registration.html', {'form': form})
            # return HttpResponse(form.errors)

def record_assessment(request, assessmevent_id):
    if request.method == 'POST':
        assessmevent = AssessEvent.objects.get(id=assessmevent_id)

        # be sure to only record a single set of responses per assessmevent
        if ( not Response.objects.filter(assess_event=assessmevent)):
            for item_name, value in request.POST.items():
                new_response = Response(
                    assess_event = assessmevent,
                    item_name = item_name,
                    response = value,
                    submitted_at = datetime.datetime.now()
                    )
                new_response.save()
        return render(request, 'assessment_complete.html')
    # this handler will be assessment agnostic - it will serve up the assessment passed in
    return HttpResponse('something went wrong')    

