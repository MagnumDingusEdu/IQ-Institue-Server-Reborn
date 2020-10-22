from rest_framework import serializers
from users.models import Course, NewRegistration


class CourseSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return instance.title

    class Meta:
        model = Course
        fields = ("title", "id")


class NewRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewRegistration
        fields = ("name", 'email', 'mobile', 'courses')
