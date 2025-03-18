from .forms import FeedbackForm
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, HttpResponseForbidden, \
    HttpResponseServerError
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from  .models import News
# Create your views here.

cafs_db = [
{'id': 1, 'name': 'Astronomy'},
{'id': 2, 'name': 'Magic'},
{'id': 3, 'name': 'Fisics'},
{'id': 4, 'name': 'Qwertyuio'},
]
menu=[]


def index(request):
    posts = News.published.all()
    return render(request, 'university/index.html', {'posts': posts})



class MyClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b



def about(request):
    return render(request, 'university/about.html', {'title': 'o сайте', 'menu': menu})

def department(request, dep_id):
    return HttpResponse(f"<h1>Кафедры по номерам</h1><p >id:{dep_id}</p>")

def department_by_slug(request, deps):
    if request.GET:
        print(request.GET)
    return HttpResponse(f"<h1>Кафедры по направлениям</h1><p >slug: {deps}</p>")

@csrf_exempt
def feedback(request):
    if request.method == "POST":
        print(request.POST)
        form = FeedbackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            return HttpResponse(f"""
                <h2>Спасибо за ваш отзыв!</h2>
                <p><strong>Имя:</strong> {name}</p>
                <p><strong>Email:</strong> {email}</p>
                <p><strong>Сообщение:</strong> {message}</p>
                <br>
                <a href="/feedback/">Отправить ещё один отзыв</a>
            """)
    else:
        form = FeedbackForm()

    return HttpResponse(f"""
        <html>
        <head>
            <title>Оставьте отзыв</title>
        </head>
        <body>
            <h2>Форма для отправки отзыва</h2>
            <form method="post">
                {form.as_p()}
                <button type="submit">Отправить</button>
            </form>
        </body>
        </html>
    """)


def archive(request, year):
    if int(year) > 2024:
        return redirect('home', permanent=True)
    if int(year) < 1930:
        return redirect(f"/archive/1930-01-01/")
    return HttpResponse(f"<h1>Архив по годам</h1><p >{year}</p>")

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def archive_date(request, dt):
    year = dt.year
    if year > 2024:
        return redirect('home', permanent=True)
    if year < 1930:
        return redirect(f"/archive/1930-01-01/")
    return HttpResponse(f"<h1>Архив по датам</h1><p >{dt.date()}</p>")

def server_error(request):
    return HttpResponseServerError('<h1>Ошибка сервера</h1>')

def access_error(request, exception):
    return HttpResponseForbidden('<h1>Ошибка доступа</h1>')


def show_post(request, post_slug):
    post = get_object_or_404(News, slug = post_slug)

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }

    return render(request, 'university/news.html',
                  context=data)


def contact(request):
    return render(request, 'university/contact.html')


def login(request):
    return HttpResponse("Авторизация")

def show_category(request, cat_id):
    """Функция-заглушка"""
    return index(request)

