from django.urls import path
from lectures.views import NodeDetailView, NodeRootView, NodeSearchView

urlpatterns = [

    path("detail/<uuid:pk>/", NodeDetailView.as_view(), name="node-detail"),
    path("", NodeRootView.as_view(), name="node-root"),
    path("search/", NodeSearchView.as_view(), name='node-search'),
]
