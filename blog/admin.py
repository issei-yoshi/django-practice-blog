from django.contrib import admin

from blog.models import Post, Category, Tag

class PostAdmin(admin.ModelAdmin):
    list_display=(
        "title",
        "category",
        "created_at",
        "updated_at",
        "is_published",
    )

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)