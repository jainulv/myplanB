from django import forms
from .fields import ListTextWidget

#class NCoursesForm(forms.Form):
#    n_courses=forms.CharField(label='Number of Courses')
#    
class InputForm(forms.Form):
#    coursename=forms.ChoiceField(label='Course name', choices=[(i, lst[i]) for i in range(0, len(lst))])
    #rating=forms.CharField(label='Rating', max_length=10)
    
    def __init__(self, dropdown_data, *args, **kwargs):
        super(InputForm, self).__init__(*args, **kwargs)
        self.fields['coursename'] = forms.ChoiceField(label='Course name', choices=[(i, dropdown_data[i]) for i in range(0, len(dropdown_data))])
        #self.fields['coursename']=forms.CharField(required=True)
        #self.fields['coursename'].widget=ListTextWidget(data_list=dropdown_data, name='coursename')
        #self.fields['rating_%s'%j]=forms.CharField(label='Rating', max_length=10)