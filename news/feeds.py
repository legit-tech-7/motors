from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Post

class MyProfessionalFeed(Feed):
    title = "DNN Blog - Latest News"
    link = "/rss/"
    description = "Latest news from DNN Blog: tech, sports, politics, finance."

    def items(self):
        # Fetch only published posts, latest 20
        return Post.objects.filter(is_published=True).order_by('-published_date')[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        # Add excerpt and Read more link
        description = item.excerpt or item.content[:200]  # fallback if excerpt is empty
        read_more = f'<p><a href="https://digitexpulse.com/{item.slug}/">Read more</a></p>'
        # Add image if exists
        if item.image:
            img_tag = f'<p><img src="https://digitexpulse.com{item.image.url}" alt="{item.title}" /></p>'
            return img_tag + description + read_more
        return description + read_more

    def item_link(self, item):
        return f"https://digitexpulse.com/{item.slug}/"

    def item_pubdate(self, item):
        return item.published_date or item.created_date

    def item_guid(self, item):
        return f"https://digitexpulse.com/{item.slug}/"

    def item_enclosure_url(self, item):
        if item.image:
            return f"https://digitexpulse.com{item.image.url}"
        return None

    def item_enclosure_length(self, item):
        return 0

    def item_enclosure_mime_type(self, item):
        if item.image:
            return "image/jpeg"
        return None
