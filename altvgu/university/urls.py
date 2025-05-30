from django.urls import path, re_path, register_converter
from . import views, converters

from django.conf import settings
from django.conf.urls.static import static

register_converter(converters.FourDigitYearConverter, "year4")
register_converter(converters.DateConverter, 'date')

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('about/', views.AboutPage.as_view(), name='about'),
    path('contact/', views.ContactPage.as_view(), name='contact'),
    path('addpage/', views.AddNews.as_view(), name='addpage'),
    path('edit/<slug:post_slug>/', views.EditNews.as_view(), name='edit_news'),
    path('delete/<slug:post_slug>/', views.DeleteNews.as_view(), name='delete_news'),
    path('post/<slug:post_slug>/', views.ShowNews.as_view(), name='post'),
    path('news/<slug:post_slug>/', views.ShowNews.as_view(), name='news_detail'),
    path("feedback/", views.FeedbackView.as_view(), name="feedback"),
    path('cats/<int:dep_id>/', views.department, name='dep_id'),
    path('cats/<slug:deps>/', views.department_by_slug, name='deps'),
    re_path(r'^archive/(?P<year>[0-9]{4})/', views.archive, name='archive'),
    path('archive/<date:dt>/', views.archive_date, name='date'),
    path('vote/news/<int:news_id>/', views.vote_news, name='vote_news'),
    path('vote/comment/<int:comment_id>/', views.vote_comment, name='vote_comment'),

    #path('login/', views.login, name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
