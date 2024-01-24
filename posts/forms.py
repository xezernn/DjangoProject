from .models import Comments
from django import forms

class CommentForm(forms.ModelForm):
    def _init_(self,*args,**kwargs):
        super(CommentForm,self)._init_(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs={'class':'form-control'}

        self.fields['bio'].widget.attrs['rows'] = 10
        self.fields['bio'].widget.attrs['cols'] = 50
        self.fields['bio'].widget.attrs['placeholder'] = "ADD COMMENT"

    class Meta:
            model = Comments
            fields = ['name','bio','photo']
