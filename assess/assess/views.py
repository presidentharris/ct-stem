from django.shortcuts import render
from django.template.loader import get_template
from django.template import Context
from django.http import Http404, HttpResponse
from oas.models import Student, Section, Teacher
from forms import StudentLoginForm

import datetime
import json


def student_login(request):
    schools = Teacher.objects.values('school').distinct()
    teachers = Teacher.objects.all().order_by("last_name")
    return render(request, 'student_login.html', {'schools':schools, 'teachers':teachers})

def get_data(request, table):
    if 'filter' in request.GET:
        inFilter = request.GET['filter']
        if table == 'Teacher':
            teachers = Teacher.objects.filter(school=inFilter).order_by("last_name")
            data_json = [(t.id, t.first_name + ' ' + t.last_name) for t in teachers]
        elif table == 'Section':
            teacher = Teacher.objects.get(id=inFilter)
            sections = Section.object.filter(teacher=teacher)
            data_json = [(s.id, s.subject + ' ' + s.section) for s in sections]
        return HttpResponse(json.dumps({'table' : table, 'values': data_json}), mimetype="application/json")
    else:
        return HttpResponse(table)

def student_status(request):
    form = StudentLoginForm()
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                student = Student.objects.get(student_id=cd['student_id'], school=cd['school'])
                return render(request, 'student_status.html', {'student': student})
            except Student.DoesNotExist:
                message = 'Studnet with that id didn\'t exist in that school so create entry and go to registration page' 
        else:
            message = 'error retrieving student info'
    else:
        message = 'error with submitted info'
    return render(request, 'student_login.html', {'error': True, 'message': message, 'student_login_form': form})

def student_registration(request):
    return render(request, 'student_login.html')

def hello(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))

def current_datetime(request):
    now = datetime.datetime.now()
    t = get_template('current_datetime.html')
    html = t.render(Context({'current_date': now}))
    return HttpResponse(html)

    # alternative/more clever version of what's above:
    # return render(request, 'current_datetime.html', {'current_date': datetime.datetime.now()})

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()

    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    return render(request, 'hours_ahead.html', {'hour_offset': offset, 'next_time': dt})