from django import forms
from couchdb import Server
from couchdb import Document
from django.conf import settings

SERVER=Server(getattr(settings, 'COUCHDB_SERVER'))
SERVER.resource.credentials=('admin','*@Ja#9824147318!')

class NCoursesForm(forms.Form):
    n_courses=forms.CharField(label='Number of Courses')
    
class InputForm(forms.Form):
    #coursename=forms.ChoiceField(label='Course name', choices=[(i, lst[i]) for i in range(0, len(lst))])
    #rating=forms.CharField(label='Rating', max_length=10)
    
    def __init__(self, extra_fields, dropdown_data, *args, **kwargs):
        super(InputForm, self).__init__(*args, **kwargs)
        for j in range(0,extra_fields):
            self.fields['coursename_%s'%j] = forms.ChoiceField(label='Course name', choices=[(i, dropdown_data[i]) for i in range(0, len(dropdown_data))])
            self.fields['rating_%s'%j]=forms.CharField(label='Rating', max_length=10)