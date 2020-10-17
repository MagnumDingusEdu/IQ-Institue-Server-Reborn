from django.http import Http404
from rest_framework import generics
from rest_framework import permissions
from rest_framework.authentication import (
    TokenAuthentication,
    BasicAuthentication,
    SessionAuthentication,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from lectures.serializers import (
    NodeSerializer,
    NodeDetailSerializer,
    NodeChildrenSerializer,
)
from lectures.models import Node


# Create your views here.


class NodeAllListView(generics.ListAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    pagination_class = None
    permission_classes = [permissions.IsAdminUser]


class NodeDetailView(APIView):
    authentication_classes = [
        TokenAuthentication,
        SessionAuthentication,
        BasicAuthentication,
    ]

    permission_classes = [IsAuthenticated]

    def get_object(self, pk, *args, **kwargs):
        try:
            return Node.objects.get(pk=pk)
        except Node.DoesNotExist:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        serializer_context = {
            "request": request,
        }
        node = self.get_object(pk)
        serializer = NodeDetailSerializer(node, context=serializer_context)
        folder_detail = serializer.data
        children = Node.objects.filter(parent=node)
        children_detail = NodeChildrenSerializer(
            children, many=True, context=serializer_context
        )

        folder_detail["children"] = children_detail.data

        return Response(folder_detail)


class NodeRootView(APIView):
    authentication_classes = [
        TokenAuthentication,
        SessionAuthentication,
        BasicAuthentication,
    ]

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer_context = {
            "request": request,
        }
        node = Node.objects.get(parent=None)
        serializer = NodeDetailSerializer(node, context=serializer_context)
        folder_detail = serializer.data
        children = Node.objects.filter(parent=node)
        children_detail = NodeChildrenSerializer(
            children, many=True, context=serializer_context
        )

        folder_detail["children"] = children_detail.data

        return Response(folder_detail)
