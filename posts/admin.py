from django.contrib import admin
from .models import Post

# Register your models here.
# admin.site.register(Post)

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'created_at']
    search_fields = ['title', 'content']
    list_filter = ['created_at']

    class Meta:
        model = Post


admin.site.register(Post, PostAdmin)


