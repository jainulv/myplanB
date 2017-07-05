from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from .utils import scrape_course_cat as sc

def index(request):
    #return HttpResponse('Hello, world. You\'re at the front index.')
    return render(request, 'front/index.html')

def result(request):
    course_data=request.POST.getlist('coursename')
    rating_data=request.POST.getlist('rating')
    sc.main()
    #return HttpResponseRedirect(reverse('front:result'))
    return render(request, 'front/courses.json')