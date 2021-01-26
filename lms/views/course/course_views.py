# Core Django imports.
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.db.models import Q
# Blog application imports.
from lms.models.course_model import Course, CourseSubscribe
from lms.forms.course.course_section_forms import SectionForm, CourseSubscribeForm

class CourseListView(ListView):
    model = Course
    context_object_name = "courses"
    template_name = "lms/course/home.html"

def course_subscribe(request,**kwargs):
    form = CourseSubscribeForm()
    course_id = kwargs['pk']
    course_name = Course.objects.get(id = course_id)
    if request.method=='POST':
        form = CourseSubscribeForm(request.POST)
        print('form fetched', form)
        if form.is_valid():
            form.save()
            print('form validation successful')
            return redirect('/')
    # print('final dictionary', {'form':form, 'course_name': course_name, 'course_id':course_id})
    return render(request,'lms/course/subscribe.html',{'form':form, 'course_name': course_name, 'course_id':course_id})

def course_list(request):
    search_post = request.GET.get('search')
    if search_post:
        course = Course.objects.filter(Q(title__icontains=search_post))
    else:
        course = Course.objects.all()
    paginator = Paginator(course, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'lms/course/home.html', {'course_list': page_obj})

def course_details(request,**kwargs):
    # course_number = request.GET.get('search')
    data = Course.objects.filter(id = kwargs['pk'])
    responseData = []
    for eachEntry in data:
        responseData.append(eachEntry)
    return render(request,'lms/course/coursedetails.html',{'course_list':data})