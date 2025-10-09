from django.urls import path
from . import views

app_name = 'bbi_app'

urlpatterns = [
    path('', views.index, name="index"),
    path('projects/', views.project_list, name="project_list"),
    path('add_project/', views.add_project, name="add_project"),
    path('regulamin/', views.regulations, name='regulations'),
    path('<slug:slug>/', views.project_detail, name="project_detail"),
]