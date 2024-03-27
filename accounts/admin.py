from django.contrib import admin
from .models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'date_of_birth']
    search_fields = ['email', 'username']
    list_filter = ['date_of_birth']

    class Meta:
        model = User

admin.site.register(User, UserAdmin)


