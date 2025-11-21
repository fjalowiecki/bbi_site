from django.core.paginator import Paginator
from django.templatetags.static import static
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Tag
from .forms import ProjectForm, ProjectLinkFormSet, ProjectFileFormSet
from django.db.models import Q
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

def index(request):
    tags = Tag.objects.all()
    projects = Project.objects.filter(is_approved=True).order_by('-id')[:12]
    
    # Utwórz absolutny URL dla obrazka OG (logo)
    og_image_url = request.build_absolute_uri(static('bbi_app/images/logo.svg'))

    # Utwórz absolutny URL dla strony
    og_url = request.build_absolute_uri()

    context = {
        'projects': projects, 
        'tags': tags,
        'og_image_url': og_image_url,
        'og_url': og_url,
    }
    return render(request, 'index.html', context)

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
    
    # Utwórz absolutny URL dla obrazka OG
    og_image_url = None
    if project.image1:
        og_image_url = request.build_absolute_uri(project.image1.url)

    # Utwórz absolutny URL dla strony
    og_url = request.build_absolute_uri()

    context = {
        'project': project,
        'og_image_url': og_image_url,
        'og_url': og_url,
    }
    return render(request, 'detail.html', context)

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
            
            # --- POCZĄTEK: Logika wysyłania e-maila ---
            try:
                subject = f'Nowy projekt w Banku Pomysłów: "{project.title}"'
                
                # Budowanie linku do panelu admina
                admin_url = request.build_absolute_uri(
                    reverse('admin:bbi_app_project_change', args=[project.id])
                )
                
                message = (
                    f'Użytkownik dodał nowy projekt o tytule: "{project.title}".\n\n'
                    f'Możesz go przejrzeć i zaakceptować w panelu administracyjnym:\n'
                    f'{admin_url}\n\n'
                    f'--\n'
                    f'Automatyczne powiadomienie z serwisu Bank Pomysłów.'
                )
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.ADMIN_EMAIL],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Błąd podczas wysyłania e-maila: {e}")
            # --- KONIEC: Logika wysyłania e-maila ---
            
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

def accessibility(request):
    current_date = timezone.now()
    return render(request, 'accessibility.html', {'current_date': current_date})