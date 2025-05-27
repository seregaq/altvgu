from django import forms
from unicodedata import category
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from .models import News,Author, Category
from django.core.validators import validate_slug

class FeedbackForm(forms.Form):
    name = forms.CharField(label="Ваше имя", max_length=100)
    email = forms.EmailField(label="Ваш email", required=False)
    message = forms.CharField(label="Отзыв", widget=forms.Textarea)


@deconstructible
class RussianValidator:
    ALLOWED_CHARS ="АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыьъэюя0123456789 - . , ;"
    code = 'russian'


    def __init__(self, message=None):
        self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел."


    def __call__(self, value):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message,code=self.code, params={"value": value})


# class AddPostForm(forms.Form):
#     title = forms.CharField(max_length=255, label="Заголовок", validators = [RussianValidator()])
#     slug = forms.SlugField(max_length=255,label="URL")
#     content = forms.CharField(widget=forms.Textarea(), label="Содержание")
#     actual = forms.BooleanField(required=False , label="Актуальность")
#     cat = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категория", empty_label="Категория не выбрана")
#     author = forms.ModelChoiceField(queryset=Author.objects.all(),required=False, label="Автор", empty_label="Автор не выбран")

class UploadFileForm(forms.Form):
    file = forms.FileField(label="Файл")

class AddPostForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Категория не выбрана",
        label="Категория"
    )
    author = forms.ModelChoiceField(
        queryset=Author.objects.all(),
        required=False,
        empty_label="Нет автора",
        label='Автор'
    )
    slug = forms.SlugField(
        label="URL",
        #validators=[validate_slug]
    )
    visibility = forms.ChoiceField(
        choices=News.Visibility.choices,
        label="Видимость"
    )

    def clean_title(self):
        title = self.cleaned_data['title']

        validator = RussianValidator()
        validator(title)

        return title

    class Meta:
        model = News
        fields = ['title', 'slug', 'content','photo', 'actual', 'category','author', 'visibility']


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'