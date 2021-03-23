from django.contrib import admin
from lectures.models import Node


# Register your models here.


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    @staticmethod
    def course_details(instance):
        course_list = ""
        data = instance.courses.all()
        for course in data:
            course_list = course_list + course.title + ", "
        return course_list

    list_display = (
        "title",
        "type",
        "parent",
        "video_link",
        "course_details",
        "date_created",
    )
    list_filter = (
        "courses",
        "type",
    )
    filter_horizontal = [
        "courses",
    ]
    search_fields = ["title", "parent__title"]
    readonly_fields = ["path", "id"]
