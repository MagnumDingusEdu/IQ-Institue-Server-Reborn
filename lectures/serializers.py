from rest_framework import serializers
from lectures.models import Node
from users.serializers import CourseSerializer
from base64 import b64encode


class NodeChildrenSerializer(serializers.ModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name="node-detail", format="html")
    video_link = serializers.SerializerMethodField()

    def get_video_link(self, obj):
        a = None
        if obj.video_link:
            try:
                a = b64encode(obj.video_link[-11:].encode()).hex()
            except Exception as e:
                print(e)
                a = None
        return a

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
