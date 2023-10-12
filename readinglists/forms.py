from django import forms
from .models import ReadingList


class AddBookForm(forms.Form):
    title = forms.CharField(max_length=100, label='Title')
    author = forms.CharField(max_length=100, label='Author')

class ReadingListForm(forms.ModelForm):
    class Meta:
        model = ReadingList
        fields = ['title', 'description', 'cover']

    widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control'}),
        'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        'cover': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
    }
    

