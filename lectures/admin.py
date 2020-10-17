from django.contrib import admin
from lectures.models import Node


# Register your models here.

@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'parent', 'video_link')
    list_filter = ('courses',)
    filter_horizontal = ['courses', ]
    search_fields = ['title', 'parent']
