from django.forms import ModelForm
from django import forms
from .models import Project

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title','description','featured_image',
         'demo_link','source_link','tags']

        widgets = {
            'tags':forms.CheckboxSelectMultiple(),
        }
    # over write init 
    def __init__(self , *args , **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        # ja ndryshon emrin e klases
#       self.fields['title'].widget.attrs.update({'class':'input','placeholder':'Add Title'})

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

