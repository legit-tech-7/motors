from django.contrib import admin

# Register your models here.
from django.contrib import admin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from .models import Category, ContactMessage, Post

@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'name', 'color', 'is_main_nav', 'slug')
    list_display_links = ('indented_title',)
    list_editable = ('color', 'is_main_nav')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'parent', 'color', 'order', 'is_main_nav')
        }),
    )
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['parent'].queryset = Category.objects.exclude(id=obj.id) if obj else Category.objects.all()
        return form

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_date', 'is_published', 'is_featured')
    list_filter = ('category', 'is_published', 'is_featured', 'created_date')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_date'
    filter_horizontal = ()
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'category', 'image')
        }),
        ('Content', {
            'fields': ('excerpt', 'content')
        }),
        ('Publication', {
            'fields': ('is_published', 'is_featured', 'is_trending', 'published_date')
        }),

    )

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_date', 'is_read')
    list_filter = ('is_read', 'submitted_date')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('submitted_date',)
    list_editable = ('is_read',)

from .models import MusicTrack, VideoNews

@admin.register(MusicTrack)
class MusicTrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album', 'genre', 'download_count', 'play_count', 'is_published')
    list_filter = ('genre', 'is_published', 'release_date')
    search_fields = ('title', 'artist', 'album')
    list_editable = ('is_published',)

@admin.register(VideoNews)
class VideoNewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'view_count', 'is_published', 'publish_date')
    list_filter = ('category', 'is_published', 'publish_date')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_published',)


from .models import AffiliateBanner

@admin.register(AffiliateBanner)
class AffiliateBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)