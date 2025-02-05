from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

class Project(models.Model):
    short_title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=bool)
    full_title = models.CharField(max_length=500)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    # images = models.ImageField(upload_to='images/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')

    def __str__(self):
        return self.short_title
    
    def get_absolute_url(self):
        return reverse('bbi_app:project_detail', args=[self.slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.short_title)
            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)