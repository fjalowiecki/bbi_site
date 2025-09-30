from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Tag
from .forms import ProjectForm
from django.db.models import Q

def index(request):
    tags = Tag.objects.all()
    projects = Project.objects.all().order_by('-id')[:12]
    return render(request, 'index.html', {'projects': projects, 'tags': tags})
    
def project_list(request):
    tags = Tag.objects.all()
    query = request.GET.get('q')
    if query:
        project_queryset = Project.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__slug__iexact=query)
        ).distinct()
    else:
        project_queryset = Project.objects.all()

    paginator = Paginator(project_queryset, 12)  # Pokaż 12 projektów na stronę
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'list.html', {'projects': page_obj, 'tags': tags})

def project_detail(request, slug): 
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'detail.html', {'project': project})

def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            form.save_m2m()
            return redirect('bbi_app:project_detail', slug=project.slug)
    else:
        form = ProjectForm()
    return render(request, 'add_project.html', {'form': form})


