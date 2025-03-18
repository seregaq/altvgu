from django import forms

class FeedbackForm(forms.Form):
    name = forms.CharField(label="Ваше имя", max_length=100)
    email = forms.EmailField(label="Ваш email", required=False)
    message = forms.CharField(label="Отзыв", widget=forms.Textarea)
