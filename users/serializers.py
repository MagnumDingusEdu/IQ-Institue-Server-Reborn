from rest_framework import serializers
from users.models import Course


class CourseSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return instance.title

    class Meta:
        model = Course
        fields = ("title", "id")
