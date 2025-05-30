from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView, TemplateView
from django.views import View
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy,reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError, HttpResponseForbidden
from .models import News, Comment, CommentVote, NewsVote
from .forms import AddPostForm, FeedbackForm, CommentForm
from .utils import DataMixin
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.decorators.http import require_POST
from django.utils.http import urlencode



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
        return News.published.filter(actual=True).order_by('-published_date')  # или .order_by('-id')

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

class DeleteNews(PermissionRequiredMixin, DeleteView):
    permission_required = 'university.delete_news'
    raise_exception = True
    model = News
    template_name = 'university/delete.html'
    success_url = reverse_lazy('home')
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    title_page = 'Удаление статьи'

@require_POST
def vote_news(request, news_id):
    if not request.user.is_authenticated:
        return redirect(f"{reverse('users:login')}?next={request.META.get('HTTP_REFERER', '/')}")

    news = get_object_or_404(News, pk=news_id)
    value = int(request.POST.get('value'))
    NewsVote.objects.update_or_create(news=news, user=request.user, defaults={'value': value})
    return redirect(news.get_absolute_url())


@require_POST
def vote_comment(request, comment_id):
    if not request.user.is_authenticated:
        return redirect(f"{reverse('users:login')}?next={request.META.get('HTTP_REFERER', '/')}")

    comment = get_object_or_404(Comment, pk=comment_id)
    value = int(request.POST.get('value'))
    CommentVote.objects.update_or_create(comment=comment, user=request.user, defaults={'value': value})
    return redirect(comment.news.get_absolute_url())


class ShowNews(DataMixin, DetailView):
    model = News
    template_name = 'university/news.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_object(self, queryset=None):
        return get_object_or_404(News.published, slug=self.kwargs[self.slug_url_kwarg])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['can_edit'] = user.has_perm('university.change_news')
        context['can_delete'] = user.has_perm('university.delete_news')
        context['comments'] = self.object.comments.all()
        context['form'] = CommentForm()
        context['like_count'] = self.object.votes.filter(value=1).count()
        context['dislike_count'] = self.object.votes.filter(value=-1).count()
        return self.get_mixin_context(context, title=self.object.title)

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated:
            messages.error(request, "Авторизуйтесь, чтобы просмотреть новость.")
            return redirect(f"{reverse_lazy('users:login')}?next={request.path}")

        if not request.user.has_perm('university.view_news'):
            messages.error(request, "У вас нет доступа к этой новости.")
            return redirect(f"{reverse_lazy('home')}?next={request.path}")

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)

        if not request.user.is_authenticated:
            messages.error(request, "Авторизуйтесь, чтобы оставить комментарий.")
            return redirect(f"{reverse_lazy('users:login')}?next={request.path}")

        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = self.object
            comment.author = request.user
            comment.save()
            messages.success(request, "Комментарий добавлен.")
            return redirect(self.object.get_absolute_url())

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)




class AddNews(CreateView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('university.add_news'):
            messages.error(request, "Недостаточно прав.")
            return redirect(f"{reverse_lazy('home')}?next={request.path}")
        return super().dispatch(request, *args, **kwargs)

    form_class = AddPostForm
    template_name = 'university/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление статьи'


class EditNews(PermissionRequiredMixin, UpdateView):
    permission_required = 'university.change_news'
    raise_exception = True
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
