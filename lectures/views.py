from django.http import Http404
from rest_framework import generics, status
from rest_framework.authentication import (
    TokenAuthentication,
    BasicAuthentication,
    SessionAuthentication,
)
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from lectures.serializers import (
    NodeDetailSerializer,
    NodeChildrenSerializer,
    NodeCRUDOperations
)
from lectures.models import Node
from lectures.permissions import IsActive


class NodeDetailView(APIView):
    authentication_classes = [
        TokenAuthentication,
        SessionAuthentication,
        BasicAuthentication,
    ]

    permission_classes = [IsAuthenticated, IsActive]

    def get_object(self, pk, *args, **kwargs):
        try:
            return Node.objects.get(pk=pk)
        except Node.DoesNotExist:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        user_courses = list(request.user.student.courses.all())

        serializer_context = {
            "request": request,
        }
        node = self.get_object(pk)
        serializer = NodeDetailSerializer(node, context=serializer_context)
        folder_detail = serializer.data
        children = Node.objects.filter(parent=node).filter(courses__in=user_courses).distinct()
        children_detail = NodeChildrenSerializer(
            children, many=True, context=serializer_context
        )

        folder_detail["children"] = children_detail.data

        return Response(folder_detail)

    def put(self, request, pk, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied({"detail": "You do not have the required permissions to perform this action."})
        node = self.get_object(pk)
        serializer = NodeCRUDOperations(node, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied({"detail": "You do not have the required permissions to perform this action."})
        node = self.get_object(pk)
        node.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NodeRootView(APIView):
    authentication_classes = [
        TokenAuthentication,
        SessionAuthentication,
        BasicAuthentication,
    ]

    permission_classes = [IsAuthenticated, IsActive]

    def get(self, request, *args, **kwargs):
        user_courses = list(request.user.student.courses.all())

        serializer_context = {
            "request": request,
        }
        node = Node.objects.get(parent=None)
        serializer = NodeDetailSerializer(node, context=serializer_context)
        folder_detail = serializer.data
        children = Node.objects.filter(parent=node).filter(courses__in=user_courses).distinct()
        children_detail = NodeChildrenSerializer(
            children, many=True, context=serializer_context
        )

        folder_detail["children"] = children_detail.data

        return Response(folder_detail)

    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied({"detail": "You do not have the required permissions to perform this action."})
        serializer = NodeCRUDOperations(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NodeSearchView(generics.ListAPIView):
    authentication_classes = [
        TokenAuthentication,
        SessionAuthentication,
        BasicAuthentication,
    ]
    permission_classes = [IsAuthenticated, IsActive]
    serializer_class = NodeChildrenSerializer

    def get_queryset(self):
        node_title = self.request.query_params.get('query', None)
        if not node_title:
            return Node.objects.none()
        user_courses = list(self.request.user.student.courses.all())
        queryset = Node.objects \
            .filter(type='vid', title__search=node_title) \
            .filter(courses__in=user_courses).distinct()
        return queryset
