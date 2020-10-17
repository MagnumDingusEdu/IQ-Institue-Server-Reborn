from django.urls import path
from lectures.views import NodeAllListView, NodeDetailView, NodeRootView

urlpatterns = [
    path("", NodeAllListView.as_view(), name="all-admin-view"),
    path("detail/<uuid:pk>/", NodeDetailView.as_view(), name="node-detail"),
    path("detail/", NodeRootView.as_view(), name="node-root"),
]
