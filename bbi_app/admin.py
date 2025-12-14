from django.contrib import admin
from .models import Project, Tag, ProjectLink, ProjectFile
from django.utils.text import slugify

def approve_projects(modeladmin, request, queryset):
    for project in queryset:
        project.is_approved = True
        project.save()
approve_projects.short_description = "Zatwierdź zaznaczone projekty"

def duplicate_project(modeladmin, request, queryset):
    for project in queryset:
        original_tags = list(project.tags.all())

        project.pk = None
        project.id = None

        original_title = project.title
        project.title = f"{original_title} (Kopia)"

        base_slug = slugify(project.title)
        slug = base_slug
        counter = 1
        while Project.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        project.slug = slug
        
        project.save()
        project.tags.set(original_tags)
        
duplicate_project.short_description = "Kopiuj zaznaczone projekty"

class ProjectLinkInline(admin.TabularInline):
    model = ProjectLink
    extra = 1

class ProjectFileInline(admin.TabularInline):
    model = ProjectFile
    extra = 1

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'year_of_completion', 'location', 'is_approved')
    list_filter = ('year_of_completion', 'location', 'financing_type', 'tags')
    search_fields = ('title', 'description')
    actions = [duplicate_project, approve_projects]
    inlines = [ProjectLinkInline, ProjectFileInline]
    list_editable = ('is_approved',)

admin.site.register(Project, ProjectAdmin)
admin.site.register(Tag)