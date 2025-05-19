from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView, TemplateView
from django.views import View
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError, HttpResponseForbidden
from .models import News, UploadFiles
from .forms import AddPostForm, FeedbackForm, UploadFileForm
from django.core.paginator import Paginator
from .utils import DataMixin


cafs_db = [
{'id': 1, 'name': 'Astronomy'},
{'id': 2, 'name': 'Magic'},
{'id': 3, 'name': 'Fisics'},
{'id': 4, 'name': 'Qwertyuio'},
]
menu=[]
class HomePage(DataMixin, ListView):
    model = News
    template_name = 'university/index.html'
    context_object_name = 'posts'


    def get_queryset(self):
        return News.published.filter(actual=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        return self.get_mixin_context(
            super().get_context_data(**kwargs),
            title='Главная страница',
            cat_selected=0
        )

class ContactPage(TemplateView):
    template_name = 'university/contact.html'
    title_page = 'Контакт'

class AboutPage(TemplateView):
    template_name = 'university/about.html'
    title_page = 'О сайте'

class DeleteNews(DeleteView):
    model = News
    template_name = 'university/delete.html'
    success_url = reverse_lazy('home')
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    title_page = 'Удаление статьи'


class ShowNews(DataMixin, DetailView):
    model = News
    template_name = 'university/news.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title, cat_selected=1)

    def get_object(self, queryset=None):
        return get_object_or_404(News.published, slug=self.kwargs[self.slug_url_kwarg])


class AddNews(CreateView):
    form_class = AddPostForm
    template_name = 'university/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление статьи'


class EditNews(UpdateView):
    model = News
    form_class = AddPostForm
    template_name = 'university/addpage.html'
    success_url = reverse_lazy('home')
    slug_field = 'slug'
    slug_url_kwarg = 'post_slug'
    title_page = 'Редактирование статьи'


class FeedbackView(FormView):
    template_name = 'university/feedback.html'
    form_class = FeedbackForm

    def form_valid(self, form):
        return HttpResponse(f"""
            <h2>Спасибо за ваш отзыв!</h2>
            <p><strong>Имя:</strong> {form.cleaned_data['name']}</p>
            <p><strong>Email:</strong> {form.cleaned_data['email']}</p>
            <p><strong>Сообщение:</strong> {form.cleaned_data['message']}</p>
            <br><a href="/feedback/">Отправить ещё один отзыв</a>
        """)


def department(request, dep_id):
    return HttpResponse(f"<h1>Кафедры по номерам</h1><p >id:{dep_id}</p>")

def department_by_slug(request, deps):
    return HttpResponse(f"<h1>Кафедры по направлениям</h1><p >slug: {deps}</p>")

def archive(request, year):
    if int(year) > 2024:
        return redirect('home', permanent=True)
    if int(year) < 1930:
        return redirect("/archive/1930-01-01/")
    return HttpResponse(f"<h1>Архив по годам</h1><p >{year}</p>")

def archive_date(request, dt):
    year = dt.year
    if year > 2024:
        return redirect('home', permanent=True)
    if year < 1930:
        return redirect("/archive/1930-01-01/")
    return HttpResponse(f"<h1>Архив по датам</h1><p >{dt.date()}</p>")

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def server_error(request):
    return HttpResponseServerError('<h1>Ошибка сервера</h1>')

def access_error(request, exception):
    return HttpResponseForbidden('<h1>Ошибка доступа</h1>')



def login(request):
    return HttpResponse("Авторизация")

def show_category(request, cat_id):
    return redirect('home')
