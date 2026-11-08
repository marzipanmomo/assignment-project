from django.db import models

# Create your models here.

class Category(models.Model):
    GROUP_CHOICES = [
        ('room', 'Shop by Room'),
        ('aesthetic', 'Shop by Aesthetic'),
        ('type', 'Shop by Product Type'),
    ]
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    group = models.CharField(max_length=20, choices=GROUP_CHOICES)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['group', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_group_display()})"

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    option = models.CharField(max_length=50, blank=True) #filters
    image = models.ImageField(upload_to='products/', blank=True)
    is_featured = models.BooleanField(default=False) #spotlight
    categories = models.ManyToManyField(Category, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class ContactMessage(models.Model):
    TOPIC_CHOICES = [
        ('query', 'General Query'),
        ('order', 'Order issue'),
        ('complaint', 'Complaint'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    topic = models.CharField(max_length=20, choices=TOPIC_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_topic_display()} from {self.email}"