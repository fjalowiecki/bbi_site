from django.shortcuts import render, get_object_or_404, redirect
from .models import Project
from .forms import ProjectForm
from django.db.models import Q

def project_list(request):
    query = request.GET.get('q')
    if query:
        projects = Project.objects.filter(Q(title__icontains=query) | Q(short_description__icontains=query) | Q(description__icontains=query))
    else:
        projects = Project.objects.all()
    return render(request, 'list.html', {'projects': projects})

def project_detail(request, slug): 
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'detail.html', {'project': project})

def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            new_project = form.save(commit=False)
            new_project.owner = request.user
            new_project.save()
            return redirect('bbi_app:project_list')
    else:
        form = ProjectForm()
    return render(request, 'add_project.html', {'form': form})


