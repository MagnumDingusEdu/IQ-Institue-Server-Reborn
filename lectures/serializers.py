from rest_framework import serializers
from lectures.models import Node
from users.serializers import CourseSerializer


class NodeChildrenSerializer(serializers.ModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name="node-detail", format="html")

    class Meta:
        model = Node
        fields = ("id", "title", "type", "video_link", "link", "date_created")


class NodeDetailSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True)
    # link = serializers.HyperlinkedIdentityField(view_name='node-detail', format='html', lookup_field='pk')

    parent = NodeChildrenSerializer()

    class Meta:
        model = Node
        fields = (
            "id",
            "title",
            "path",
            "date_created",
            "courses",
            "parent",
        )

        depth = 1


class NodeCRUDOperations(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ("title", "parent", "courses", "video_link", "type")
