from django.contrib import admin
from photomanagementapp.models import Gallery, Photo

admin.site.register(
    Gallery,
    list_display=["id", "title", "description", "created_at"],
    list_display_links=["id", "title"],
)

admin.site.register(
    Photo,
    list_display=["id", "title", "image", "description", "created_at", "gallery"],
    list_display_links=["id", "title"],
)
