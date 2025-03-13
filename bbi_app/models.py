from django.db import models
from django.urls import reverse
from django.utils.text import slugify

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

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    short_description = models.CharField(max_length=250)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    people_involved_nb = models.PositiveBigIntegerField()
    year_of_completion = models.PositiveSmallIntegerField()
    location = models.CharField(max_length=30, choices=LOCATION)
    financing_type = models.CharField(max_length=20, choices=FINANCING_TYPES)
    financing_type_other = models.CharField(max_length=250, blank=True, null=True)
    proj_site = models.URLField(blank=True, null=True)
    contact_info = models.TextField(max_length=250, blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='projects', blank=True)
    
    # Photo
    image1 = models.ImageField(upload_to='media/', blank=True, null=True)
    image2 = models.ImageField(upload_to='media/', blank=True, null=True)
    image3 = models.ImageField(upload_to='media/', blank=True, null=True)
    image4 = models.ImageField(upload_to='media/', blank=True, null=True)
    MAIN_IMAGE_CHOICES = [
        (1, 'Zdjęcie 1'),
        (2, 'Zdjęcie 2'),
        (3, 'Zdjęcie 3'),
        (4, 'Zdjęcie 4'),
    ]
    main_image = models.PositiveSmallIntegerField(choices=MAIN_IMAGE_CHOICES, blank=True, null=True, help_text="Wybierz numer zdjęcia, które ma być głównym")
    

    def __str__(self):
        return self.short_description
    
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

