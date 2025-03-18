from django.urls import path,re_path,register_converter
from university import views,converters

register_converter(converters.FourDigitYearConverter, "year4")
register_converter(converters.DateConverter, 'date')

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('cats/<int:dep_id>/', views.department, name='dep_id'),
    path("feedback/", views.feedback, name="feedback"),
    path('cats/<slug:deps>/',views.department_by_slug, name='deps'),
    re_path(r'^archive/(?P<year>[0-9]{4})/', views.archive, name='archive'),
    path('archive/<date:dt>/', views.archive_date, name="date"),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.show_post,name='post'),
    path('news/<slug:post_slug>/', views.show_post, name='news_detail'),



]