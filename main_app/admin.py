from django.contrib import admin

from .models import Movie


# Register your models here.
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'actor', 'release_date', 'status', 'created_at']
    list_filter = []
    search_fields = ['name', 'release_date', 'status']
    readonly_fields = ['created_at']