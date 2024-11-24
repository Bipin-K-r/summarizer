from django.urls import path
from .views import PaperListView, PaperDetailView

urlpatterns = [
    path('papers/', PaperListView.as_view(), name='paper-list'),
    path('papers/<str:filename>/', PaperDetailView.as_view(), name='paper-detail'),
]