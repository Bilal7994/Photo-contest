from django.contrib import admin
from .models import Contest,Like,Photo

# Register your models here.
class likes_count(admin.ModelAdmin):
    list_display = ('likes_count','user','contest')
    
admin.site.register(Contest)
admin.site.register(Photo,likes_count)
admin.site.register(Like)