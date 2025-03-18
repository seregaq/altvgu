from django.urls import path,re_path,register_converter
from timetable import views


urlpatterns = [

    path('groups/<int:group_id>/', views.group, name='group_id'),


]