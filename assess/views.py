import csv, codecs, cStringIO
from django.shortcuts import render
from django.http import HttpResponse
from oas.models import Student, Section, Teacher, AssessEvent, Response
from forms import StudentRegistrationForm, GuestRegistrationForm

import datetime
import json
import collections

Assessment = collections.namedtuple('Assessment', ['id', 'name', 'url', 'current_version', 'ipad_compatible'])
ASSESSMENTS = {
    'CPS1': Assessment(id='CPS1', name='Computational Problem Solving 1', url='cps1.html', current_version='1.0', ipad_compatible=''),
    'HDI': Assessment(id='HDI', name='Human Development Index', url='HDI.html', current_version='1.0', ipad_compatible='disabled'),
    'PB': Assessment(id='PB', name='Purple Bugs', url='purple_bugs.html', current_version='1.0', ipad_compatible='disabled'), 
    'FP': Assessment(id='FP', name='Flower Pickers', url='flower_pickers.html', current_version='1.0', ipad_compatible='disabled'), 
    'UNI1': Assessment(id='UNI1', name='General CT-STEM Assessment 1', url='uni1.html', current_version='1.1', ipad_compatible='disabled'),
    'WARB': Assessment(id='WARB', name='Warblers', url='warblers.html', current_version='1.0', ipad_compatible=''), 
    'UNI2': Assessment(id='UNI2', name='General CT-STEM Assessment 2', url='gen2.html', current_version='1.0', ipad_compatible=''),
    }


def student_login(request):
    ua = request.META.get('HTTP_USER_AGENT', '').lower()
    is_ipad = ua.find("ipad") > 0

    schools = Teacher.objects.values("school").distinct().order_by("school")
    teachers = Teacher.objects.all().order_by("last_name")
    return render(request, 'student_login.html', {'schools':schools, 'teachers':teachers, 'assessments': sorted(ASSESSMENTS.values(), cmp=lambda x,y: cmp(x.name, y.name)), 'is_ipad': is_ipad})

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

    ua = request.META.get('HTTP_USER_AGENT', '').lower()
    is_ipad = ua.find("ipad") > 0

    if errors:
        #TODO: figure out how to reuse the student_login method
        schools = Teacher.objects.values('school').distinct()
        teachers = Teacher.objects.all().order_by("last_name")
        return render(request, 'student_login.html', {'schools':schools, 'teachers':teachers, 'errors':errors, 'assessments': sorted(ASSESSMENTS.values(), cmp=lambda x,y: cmp(x.name, y.name)), 'is_ipad': is_ipad})

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

        return render(request, 'sets/' + ASSESSMENTS[assessmevent.assessment_set].url, {'assessment': ASSESSMENTS[assessmevent.assessment_set], 'assessmevent': assessmevent})

    except Student.DoesNotExist:
        registration_form = StudentRegistrationForm(
            initial={'student_id' : student_id, 'school' : section.teacher.school, 'section_id' : section.id, 'assessment_set': request.POST['assessment_set'], 'location' : request.POST['location']}
            )
        return render(request, 'student_registration.html', {'form': registration_form, 'section': section})
    except Exception as e:
        errors.append("An error occured, please verify your information and try again.")
        schools = Teacher.objects.values("school").distinct().order_by("school")
        return render(request, 'student_login.html', {'errors': errors, 'e':e, 'schools':schools, 'assessments': sorted(ASSESSMENTS.values(), cmp=lambda x,y: cmp(x.name, y.name)), 'is_ipad': is_ipad})

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
            return render(request, 'sets/' + ASSESSMENTS[assessmevent.assessment_set].url, {'assessment': ASSESSMENTS[assessmevent.assessment_set], 'assessmevent': assessmevent})
        else:
            return render(request, 'student_registration.html', {'form': form})
            # return HttpResponse(form.errors)

def guest_login(request):
    ua = request.META.get('HTTP_USER_AGENT', '').lower()
    is_ipad = ua.find("ipad") > 0

    registration_form = GuestRegistrationForm(
        initial={
            'assessment_set': request.GET.get('assessment')
        })

    return render(request, 'guest_registration.html', {'form': registration_form, 'assessments': sorted(ASSESSMENTS.values(), cmp=lambda x,y: cmp(x.name, y.name)), 'is_ipad':is_ipad})

def guest_register(request):
    if request.method == 'POST':
        form = GuestRegistrationForm(request.POST)
        if form.is_valid():
            in_data = form.cleaned_data

            # for guests - make the email address the natural key (to keep for getting guest dups)
            #   yes this conditional is goofy, but it needs to be due to falsy-ness of strings and filter method
            if ( not in_data['email'] or not Student.objects.filter(email=in_data['email'], student_id='GUEST')):
                student = Student(
                        student_id='GUEST',
                        first_name=in_data['first_name'],
                        last_name=in_data['last_name'],
                        grade='0',
                        sex='-',
                        dob=datetime.date.today(),
                        school=in_data['school'],
                        email=in_data['email'],
                        ethnicity=in_data['ethnicity'])
            else:
                student = Student.objects.get(email=in_data['email'], student_id='GUEST')

            student.save()

            section = Section.objects.get(name='Guest Section')

            assessmevent = AssessEvent (
                student = student,
                section = section,
                date = datetime.datetime.now(),
                location = 'guest',
                assessment_set = in_data['assessment_set']
                )

            assessmevent.save()
            return render(request, 'sets/' + ASSESSMENTS[assessmevent.assessment_set].url, {'assessment': ASSESSMENTS[assessmevent.assessment_set], 'assessmevent': assessmevent})
        else:
            return render(request, 'guest_registration.html', {'form': form, 'assessments': sorted(ASSESSMENTS.values(), cmp=lambda x,y: cmp(x.name, y.name))})

    return render(request, 'guest_registration.html', {'form': GuestRegistrationForm(), 'assessments': sorted(ASSESSMENTS.values(), cmp=lambda x,y: cmp(x.name, y.name))})

def record_assessment(request, assessmevent_id):
    ua = request.META.get('HTTP_USER_AGENT', '').lower()
    is_ipad = ua.find("ipad") > 0
        
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

        return render(request, 'assessment_complete.html', {'assessmevent_id':assessmevent_id, 'assessments': sorted(ASSESSMENTS.values(), cmp=lambda x,y: cmp(x.name, y.name)), 'is_ipad':is_ipad})
    return HttpResponse('something went wrong')    

def continuation_assessment(request):
    if request.method == 'POST':
        old_assessmevent_id = request.POST['assessmevent_id']
        old_assessmevent = AssessEvent.objects.get(id=old_assessmevent_id)

        new_assessmevent = AssessEvent (
                student = old_assessmevent.student,
                section = old_assessmevent.section,
                date = datetime.datetime.now(),
                location = old_assessmevent.location,
                assessment_set = request.POST['assessment_set']
                )
        new_assessmevent.save() 
        return render(request, 'sets/' + ASSESSMENTS[new_assessmevent.assessment_set].url, {'assessment': ASSESSMENTS[new_assessmevent.assessment_set], 'assessmevent': new_assessmevent})

    return HttpResponse('something went wrong')    

def data_export(request):
    if (request.GET.__contains__('lname')):
        return export_by_lname(request)
    else:
        return export_by_school(request)

def export_by_lname(request):
    teacher_lname = request.GET.get('lname')

    teacher = Teacher.objects.get(last_name=teacher_lname)
    sections = Section.objects.filter(teacher=teacher)

    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    header_pt1 = ['assess DB ID', 'school', 'teacher f_name', 'teacher l_name', 'section name', 'subject', 'section', 'student DB-ID', 'student school ID', 'student fname', 'student lname', 'grade', 'sex', 'dob', 'ethnicity', 'assessment date', 'assessment set', 'location']

    for assessment in ASSESSMENTS:
        assessEvents = []  
        for section in sections:
            assessEvents += AssessEvent.objects.filter(section=section, assessment_set=assessment)


        has_header = False

        for a in assessEvents:
            t = teacher
            sec = a.section
            st = a.student
            a_info = [a.id, t.school, t.first_name, t.last_name, sec.name, sec.subject, sec.section, st.id, st.student_id, st.first_name, st.last_name, st.grade, st.sex, st.dob, st.ethnicity, a.date, a.assessment_set, a.location ]
            responses = Response.objects.filter(assess_event=a).order_by("item_name")
            item_names = []
            for r in responses:
                item_names.append(r.item_name)
                a_info.append(r.response)
            if len(responses) > 0: 
                a_info.append(responses[0].submitted_at)
                if not has_header:
                    writer.writerow(header_pt1 + item_names + ['submitted_at'])
                    has_header = True
                writer.writerow([unicode(a).encode("utf-8") for a in a_info])

        writer.writerow("")
        writer.writerow("")


    response['Content-Disposition'] = 'attachment; filename="student_responses.csv"'

    return response

def export_by_school(request):
    school_name = request.GET.get('school')

    students = Student.objects.filter(school__istartswith=school_name)
    section = Section.objects.get(name='Guest Section')

    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    header_pt1 = ['assess DB ID', 'school', 'student DB-ID', 'student fname', 'student lname', 'assessment date', 'assessment set']

    for assessment in ASSESSMENTS:
        assessEvents = []  
        for student in students:
            assessEvents += AssessEvent.objects.filter(section=section, student=student, assessment_set=assessment)


        has_header = False

        for a in assessEvents:
            sec = a.section
            st = a.student
            a_info = [a.id, st.school, st.id, st.first_name, st.last_name, a.date, a.assessment_set ]
            responses = Response.objects.filter(assess_event=a).order_by("item_name")
            item_names = []
            for r in responses:
                item_names.append(r.item_name)
                a_info.append(r.response)
            if len(responses) > 0: 
                a_info.append(responses[0].submitted_at)
                if not has_header:
                    writer.writerow(header_pt1 + item_names + ['submitted_at'])
                    has_header = True
                writer.writerow([unicode(a).encode("utf-8") for a in a_info])

        writer.writerow("")
        writer.writerow("")


    response['Content-Disposition'] = 'attachment; filename="student_responses.csv"'

    return response  

def robots(request):
    return(HttpResponse("User-agent: *\nDisallow: /"))
