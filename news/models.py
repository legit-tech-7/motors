from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey # type: ignore

class Category(MPTTModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    color = models.CharField(max_length=7, default='#bb1919', help_text="Hex color code for category (e.g., #bb1919 for News)")
    order = models.PositiveIntegerField(default=0)
    is_main_nav = models.BooleanField(default=False, help_text="Display this category in the main navigation")
    
    class MPTTMeta:
        order_insertion_by = ['order', 'name']
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=300, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)

    def publish(self):
        self.published_date = timezone.now()
        self.is_published = True
        self.save()

    def __str__(self):
        return self.title
    

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.subject} - {self.name}"


class MusicTrack(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    text = models.TextField(blank=True)
    album = models.CharField(max_length=200, blank=True)
    audio_file = models.FileField(upload_to='music/')
    cover_image = models.ImageField(upload_to='music_covers/', blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    genre = models.CharField(max_length=100, blank=True)
    download_count = models.PositiveIntegerField(default=0)
    play_count = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)
    upload_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.title} - {self.artist}"
    
    def increment_download_count(self):
        self.download_count += 1
        self.save()
    
    def increment_play_count(self):
        self.play_count += 1
        self.save()

class VideoNews(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    duration = models.DurationField(blank=True, null=True)
    view_count = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)
    publish_date = models.DateTimeField(default=timezone.now)
    tags = models.CharField(max_length=250, blank=True)
    
    def __str__(self):
        return self.title
    
    def increment_view_count(self):
        self.view_count += 1
        self.save()




class AffiliateBanner(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='affiliate_banners/')
    link = models.URLField(max_length=500)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title