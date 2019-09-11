from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.http import JsonResponse

from schools.mixins import TeacherRequiredMixin
from teachers.decorators import teacher_required
from schools.models import AcademicYear
from classroom.models import Subject, ClassRoom
from .forms import ExamForm
from .models import Exam

@login_required
@teacher_required
def exam_view(request):
    
    # queryset = Classes.objects.filter(school = request.user.school).values('name').distinct()
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.school = request.user.school
            exam.academicyear = AcademicYear.objects.get(status = True)
            exam.save()
            messages.success(request, 'Exam saved with success!')

            return redirect('exams:exams')
    else:
        # classroom = ClassRoom(school = request.user.school)
        form = ExamForm()

    exams = Exam.objects.filter(school = request.user.school)
    return render(request,"exams/exams.html", {'form': form, 'exams':exams })


class MarkEntry(TeacherRequiredMixin, View):
    def get(self, request):
        school = request.user.school
        resp ={
            'subjects': Subject.objects.filter(school=school).order_by('name'),
            'exams' : Exam.objects.filter(school=school).order_by('name'),
        }        
        return render(request,'exams/markentry.html', resp)

class getDivisions(TeacherRequiredMixin, View):
    def get(self, request):
        exam = Exam.objects.get(id=request.GET['exam'])
        classes = [c.division for c in ClassRoom.objects.filter(school = request.user.school, name=exam.exam_class)]
        return JsonResponse({'classes':classes,'is_grade':exam.is_grade},safe=False)