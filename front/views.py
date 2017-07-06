from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from couchdb import Server
from couchdb import Document
import json
from .utils import scrape_course_cat as sc
from .utils import recommender as rec

SERVER=Server(getattr(settings, 'COUCHDB_SERVER'))
SERVER.resource.credentials=('admin','YOUR PASSWORD')
db=SERVER['course_catlog']
db2=SERVER['recommender_data']

def update_DB(request):
    global db,db2
    sc.main()
    # update course catlog
    with open('courses.json', 'r') as fin:
        db_entry=json.load(fin)
        for i in range(len(db_entry['catlog'])):
            for j in range(len(db_entry['catlog'][i]['courses'])):
                if not db[db_entry['catlog'][i]['courses'][j]['title']]:
                    db[db_entry['catlog'][i]['courses'][j]['title']]={'description': db_entry['catlog'][i]['courses'][j]['description']}
    # update training data for the recommender
    SERVER.delete('recommender_data')
    db2=SERVER.create('recommender_data')
    rec.main(to_train=True)
    return HttpResponse('Database Updated')
        
def index(request):
    #return HttpResponse('Hello, world. You\'re at the front index.')
    return render(request, 'front/index.html')

def result(request):
    course_data=request.POST.getlist('coursename')
    rating_data=request.POST.getlist('rating')
    #return HttpResponseRedirect(reverse('front:result'))
    #return render(request, 'front/courses.json')
    return HttpResponse(rec.main([3000, 3500, 1500]))
