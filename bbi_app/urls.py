from django.urls import path
from . import views

app_name = 'bbi_app'

urlpatterns = [
    path('', views.index, name="index"),
    path('projects/', views.project_list, name="project_list"),
    path('add_project/', views.add_project, name="add_project"),
    path('regulamin/', views.regulations, name='regulations'),
    path('dostepnosc/', views.accessibility, name='accessibility'),
    path('project_added_success/', views.project_added_success, name='project_added_success'),
    path('<slug:slug>/', views.project_detail, name="project_detail"),
]