from django import forms
from .models import News

class FeedbackForm(forms.Form):
    name = forms.CharField(label="Ваше имя", max_length=100)
    email = forms.EmailField(label="Ваш email", required=False)
    message = forms.CharField(label="Отзыв", widget=forms.Textarea)


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'category', 'tags']