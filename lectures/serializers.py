from rest_framework import serializers
from lectures.models import Node
from users.serializers import CourseSerializer


class NodeSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(read_only=True, many=True)

    class Meta:
        model = Node
        fields = ["id", "title", "type", "parent", "courses", "video_link"]


class NodeChildrenSerializer(serializers.ModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name="node-detail", format="html")

    class Meta:
        model = Node
        fields = ("id", "title", "type", "video_link", "link", "date_created")


class NodeDetailSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(read_only=True, many=True)
    # link = serializers.HyperlinkedIdentityField(view_name='node-detail', format='html', lookup_field='pk')

    parent = NodeChildrenSerializer()

    class Meta:
        model = Node
        fields = ("id", "title", "path", "date_created", "courses", "parent",)

        depth = 1
