from django.contrib import admin
from .models import Project, Tag
from django.utils.text import slugify

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

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_description', 'year_of_completion', 'location')
    list_filter = ('year_of_completion', 'location', 'financing_type', 'tags')
    search_fields = ('title', 'short_description', 'description')
    actions = [duplicate_project]

admin.site.register(Project, ProjectAdmin)
admin.site.register(Tag)