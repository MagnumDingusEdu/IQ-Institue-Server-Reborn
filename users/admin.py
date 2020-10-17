from django.contrib import admin
from django.contrib.auth.models import User
from users.models import Course, Student


class UserInline(admin.TabularInline):
    model = User


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    def user_count(self, instance):
        return str(len(instance.student_set.all()))

    list_display = ("title", "user_count")


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    def user_name(self, instance):
        return instance.user.username + " - " + instance.user.first_name

    list_display = (
        "user_name",
        "last_login_time",
        "logged_in",
        "account_active",
        "multi_device_login",
    )
    list_filter = (
        "user",
        "courses",
        "account_active",
        "logged_in",
        "last_login_time",
        "multi_device_login",
    )
    readonly_fields = (
        "logged_in",
        "last_login_time",
    )
    filter_horizontal = [
        "courses",
    ]
    search_fields = ["user.username", "user.first_name"]
