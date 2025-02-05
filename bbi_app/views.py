from django.shortcuts import render, get_object_or_404, redirect
from .models import Project
from .forms import ProjectForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required

def project_list(request):
    query = request.GET.get('q')
    if query:
        projects = Project.objects.filter(Q(full_title__icontains=query) | Q(description__icontains=query))
    else:
        projects = Project.objects.all()
    return render(request, 'list.html', {'projects': projects})

def project_detail(request, slug): 
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'detail.html', {'project': project})

@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bbi_app:project_list')
    else:
        form = ProjectForm()
    return render(request, 'add_project.html', {'form': form})


