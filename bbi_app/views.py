from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Tag
from .forms import ProjectForm, ProjectLinkFormSet, ProjectFileFormSet
from django.db.models import Q

def index(request):
    tags = Tag.objects.all()
    projects = Project.objects.filter(is_approved=True).order_by('-id')[:12]
    return render(request, 'index.html', {'projects': projects, 'tags': tags})
    
def project_list(request):
    tags = Tag.objects.all()
    query = request.GET.get('q')
    base_queryset = Project.objects.filter(is_approved=True)

    if query:
        project_queryset = base_queryset.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__slug__iexact=query)
        ).distinct()
    else:
        project_queryset = base_queryset.all()

    paginator = Paginator(project_queryset, 12)  # Pokaż 12 projektów na stronę
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'list.html', {'projects': page_obj, 'tags': tags})

def project_detail(request, slug): 
    project = get_object_or_404(Project, slug=slug, is_approved=True)
    return render(request, 'detail.html', {'project': project})

def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        link_formset = ProjectLinkFormSet(request.POST, prefix='links')
        file_formset = ProjectFileFormSet(request.POST, request.FILES, prefix='files')

        if form.is_valid() and link_formset.is_valid() and file_formset.is_valid():
            project = form.save()

            link_formset.instance = project
            link_formset.save()

            file_formset.instance = project
            file_formset.save()
            
            return redirect('bbi_app:project_added_success')
    else:
        form = ProjectForm()
        link_formset = ProjectLinkFormSet(prefix='links')
        file_formset = ProjectFileFormSet(prefix='files')

    context = {
        'form': form,
        'link_formset': link_formset,
        'file_formset': file_formset
    }
    return render(request, 'add_project.html', context)

def project_added_success(request):
    tags = Tag.objects.all()
    return render(request, 'project_added_success.html', {'tags': tags})

def regulations(request):
    return render(request, 'regulations.html')