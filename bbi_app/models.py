from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from cloudinary_storage.storage import MediaCloudinaryStorage, RawMediaCloudinaryStorage

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Project(models.Model):
    FINANCING_TYPES = [
        ('local', 'Lokalne działania'),
        ('local_initiative', 'Inicjatywa lokalna'),
        ('own_resources', 'Z własnych środków'),
        ('no_financing', 'Realizacja bez finansowania'),
        ('other', 'Inne'),
    ]
    LOCATION = [
        ("bobrek", "Bobrek"),
        ("gorecko", "Górecko"),
        ("gorniki", "Górniki"),
        ("karb", "Karb"),
        ("lagiewniki", "Łagiewniki"),
        ("miechowice", "Miechowice"),
        ("osiedle_zietka", "Osiedle gen. Jerzego Ziętka"),
        ("rozbark", "Rozbark"),
        ("srodmiescie", "Śródmieście"),
        ("stolarzowice", "Stolarzowice"),
        ("stroszek_dabrowa", "Stroszek-Dąbrowa Miejska"),
        ("sucha_gora", "Sucha Góra"),
        ("szombierki", "Szombierki"),
    ]
    
    YEAR_CHOICES = [(r, r) for r in range(2010, 2031)]

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    year_of_completion = models.IntegerField(choices=YEAR_CHOICES)
    location = models.CharField(max_length=30, choices=LOCATION)
    financing_type = models.CharField(max_length=20, choices=FINANCING_TYPES)
    financing_type_other = models.CharField(max_length=250, blank=True, null=True)
    contact_info = models.TextField(max_length=250, blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='projects', blank=True)
    
    # Photo
    image1 = models.ImageField(upload_to='project_images/', blank=True, null=True, storage=MediaCloudinaryStorage())
    image2 = models.ImageField(upload_to='project_images/', blank=True, null=True, storage=MediaCloudinaryStorage())
    image3 = models.ImageField(upload_to='project_images/', blank=True, null=True, storage=MediaCloudinaryStorage())
    image4 = models.ImageField(upload_to='project_images/', blank=True, null=True, storage=MediaCloudinaryStorage())


    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('bbi_app:project_detail', args=[self.slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

class ProjectLink(models.Model):
    project = models.ForeignKey(Project, related_name='links', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="Nazwa linku")
    url = models.URLField(verbose_name="Adres URL")

    def __str__(self):
        return f"{self.name} ({self.project.title})"
    
class ProjectFile(models.Model):
    project = models.ForeignKey(Project, related_name='files', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="Nazwa pliku")
    file = models.FileField(upload_to='project_files/', storage=RawMediaCloudinaryStorage())

    def __str__(self):
        return f"{self.name} ({self.project.title})"