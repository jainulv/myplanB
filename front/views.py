from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from couchdb import Server
from couchdb import Document
import couchdb
import json
from .utils import scrape_course_cat as sc
from .utils import recommender as rec
from .forms import InputForm, NCoursesForm

SERVER=Server(getattr(settings, 'COUCHDB_SERVER'))
SERVER.resource.credentials=('admin','*@Ja#9824147318!')
db=SERVER['course_catlog']
db2=SERVER['recommender_data']

lst=[]
kst=[]
view=db.iterview('query_doc/a_docs', batch=2500)
for row in view:
    lst.append(row.key)
    kst.append(row.value)
    
def update_DB(request):
    global lst,kst
    sc.main()
    # update course catlog
    with open('courses.json', 'r') as fin:
        db_entry=json.load(fin)
        for i in range(len(db_entry['catlog'])):
            for j in range(len(db_entry['catlog'][i]['courses'])):
                try:
                    db[db_entry['catlog'][i]['courses'][j]['title']]
                except couchdb.ResourceNotFound:
                    db[db_entry['catlog'][i]['courses'][j]['title']]={'description': db_entry['catlog'][i]['courses'][j]['description']}
    # update training data for the recommender
    view=db.iterview('query_doc/a_docs', batch=2500)
    lst=[]
    kst=[]
    for row in view:
        lst.append(row.key)
        kst.append(row.value)
    SERVER.delete('recommender_data')
    db2=SERVER.create('recommender_data')
    rec.main(key=lst, value=kst, to_train=True)
    return HttpResponse('Database Updated')

def  index(request):
    form=NCoursesForm(request.POST)
    return render(request, 'front/index.html', {'form': form})
        
def courses(request):
    #return HttpResponse('Hello, world. You\'re at the front index.')
    if request.method == 'POST':
        form=InputForm(extra_fields=int(request.POST['n_courses']), dropdown_data=lst)
    else:
        form=InputForm()
    return render(request, 'front/courses.html', {'form': form})

def result(request):
    course_data=[]
    rating_data=[]
    print(request.POST)
    for k,v in request.POST.items():
        if 'coursename_' in k:
            course_data.append(int(v))
        elif 'rating_' in k:
            rating_data.append(float(v))
    print(course_data)
    print(rating_data)
    rclist=rec.main(course_data, lst, kst)
    recommended_courses={}
    for i in rclist:
        recommended_courses[lst[int(i)]]=kst[int(i)]
    #return HttpResponseRedirect(reverse('front:result'))
    #return render(request, 'front/courses.json')
    return HttpResponse(recommended_courses.items())
