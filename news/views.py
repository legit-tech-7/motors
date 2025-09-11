from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import AffiliateBanner, ContactMessage, MusicTrack, Post, Category, VideoNews

def home(request):
    # Get main categories for navigation
    main_categories = Category.objects.filter(is_main_nav=True, parent__isnull=True)
    
    # Get featured posts
    featured_posts = Post.objects.filter(is_featured=True, is_published=True)[:4]
    
    # Get trending posts
    trending_posts = Post.objects.filter(is_trending=True, is_published=True)[:4]

    active_banners = AffiliateBanner.objects.filter(is_active=True).order_by('-created_at')

    
    # Get posts by main categories
    category_posts = {}
    
    for category in main_categories:
        # Get all descendants including the category itself
        all_categories = category.get_descendants(include_self=True)
        posts = Post.objects.filter(
            category__in=all_categories, 
            is_published=True
        ).order_by('-published_date')[:4]
        category_posts[category] = posts
    
    context = {
        'featured_posts': featured_posts,
        'trending_posts': trending_posts,
        'category_posts': category_posts,
        'main_categories': main_categories,
        'active_banners': active_banners,
    }
    return render(request, 'blog/home.html', context)

class CategoryPostListView(ListView):
    model = Post
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        # Get all descendants including the category itself
        all_categories = self.category.get_descendants(include_self=True)
        return Post.objects.filter(
            category__in=all_categories,
            is_published=True
        ).order_by('-published_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        # Add main_categories for navigation
        context['main_categories'] = Category.objects.filter(is_main_nav=True, parent__isnull=True)
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        return Post.objects.filter(is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get related posts from the same category
        context['related_posts'] = Post.objects.filter(
            category=self.object.category,
            is_published=True
        ).exclude(id=self.object.id)[:6]
        # Add main_categories for navigation
        context['main_categories'] = Category.objects.filter(is_main_nav=True, parent__isnull=True)
        return context

def search_posts(request):
    query = request.GET.get('q', '')
    if query:
        posts = Post.objects.filter(
            title__icontains=query, 
            is_published=True
        ).order_by('-published_date')
    else:
        posts = Post.objects.none()
    
    # Add main_categories for navigation
    main_categories = Category.objects.filter(is_main_nav=True, parent__isnull=True)
    
    return render(request, 'blog/search_results.html', {
        'posts': posts,
        'query': query,
        'main_categories': main_categories,
    })



from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.conf import settings
from django.http import FileResponse, HttpResponseRedirect
from django.contrib import messages

# Add these view functions
def about_page(request):
    # Add main_categories for navigation
    main_categories = Category.objects.filter(is_main_nav=True, parent__isnull=True)
    
    context = {
        'main_categories': main_categories,
    }
    return render(request, 'blog/about.html', context)

def privacy_page(request):
    # Add main_categories for navigation
    main_categories = Category.objects.filter(is_main_nav=True, parent__isnull=True)
    
    context = {
        'main_categories': main_categories,
    }
    return render(request, 'blog/privacy.html', context)

from django.core.mail import send_mail
from django.conf import settings


def contact_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Save to database
        try:
            contact_message = ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            
            # Send confirmation email to the user
            send_mail(
                f'Thank you for contacting us! #{contact_message.id}',
                f'''Hello {name},

Thank you for contacting BBC Blog. We have received your message and will get back to you within 24-48 hours.

Your message:
{message}

Best regards,
BBC Blog Team''',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            # Send notification email to both admin emails
            admin_subject = f'New Contact Form Submission: {subject}'
            admin_message = f'''
New contact form submission from {name} ({email}):

Subject: {subject}
Message: {message}

Message ID: #{contact_message.id}
Received: {contact_message.submitted_date}

To reply, simply respond to this email or contact {email} directly.
'''
            
            # Send to both email addresses
            send_mail(
                admin_subject,
                admin_message,
                settings.DEFAULT_FROM_EMAIL,
                [ 'litget27@gmail.com'],  # BOTH emails here
                fail_silently=False,
            )
            
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            
        except Exception as e:
            messages.error(request, 'There was an error sending your message. Please try again.')
            print(f"Error: {e}")
        
        return HttpResponseRedirect('/contact/')
    
    main_categories = Category.objects.filter(is_main_nav=True, parent__isnull=True)
    context = {'main_categories': main_categories}
    return render(request, 'blog/contact.html', context)

from django.core.paginator import Paginator
from django.shortcuts import render

def music_list(request):
    music_tracks = MusicTrack.objects.filter(is_published=True).order_by('-upload_date')
    
    # paginate (7 posts per page)
    paginator = Paginator(music_tracks, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'main_categories': Category.objects.filter(is_main_nav=True, parent__isnull=True),
    }
    return render(request, 'blog/music_list.html', context)


def music_detail(request, pk):
    track = get_object_or_404(MusicTrack, pk=pk, is_published=True)
    track.increment_play_count()

    # Fetch related tracks (e.g., same genre, exclude current track, limit 6)
    related_tracks = MusicTrack.objects.filter(
        genre=track.genre,
        is_published=True
    ).exclude(id=track.id)[:6]

    context = {
        'track': track,
        'related_tracks': related_tracks,
        'main_categories': Category.objects.filter(is_main_nav=True, parent__isnull=True),
    }
    return render(request, 'blog/music_detail.html', context)


def download_music(request, pk):
    track = get_object_or_404(MusicTrack, pk=pk, is_published=True)
    track.increment_download_count()
    
    response = FileResponse(track.audio_file)
    response['Content-Disposition'] = f'attachment; filename="{track.audio_file.name}"'
    return response

from django.core.paginator import Paginator

def video_news_list(request):
    videos = VideoNews.objects.filter(is_published=True).order_by('-publish_date')
    
    # Paginate (8 videos per page, change number as needed)
    paginator = Paginator(videos, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'main_categories': Category.objects.filter(is_main_nav=True, parent__isnull=True),
    }
    return render(request, 'blog/video_list.html', context)


def video_news_detail(request, slug):
    video = get_object_or_404(VideoNews, slug=slug, is_published=True)
    video.increment_view_count()

    # Related videos from the same category (exclude current)
    related_videos = VideoNews.objects.filter(
        category=video.category,
        is_published=True
    ).exclude(id=video.id).order_by('-publish_date')[:6]

    context = {
        'video': video,
        'related_videos': related_videos,
        'main_categories': Category.objects.filter(is_main_nav=True, parent__isnull=True),
    }
    return render(request, 'blog/video_detail.html', context)



def video_test(request):
    return render(request, 'blog/video_test.html')