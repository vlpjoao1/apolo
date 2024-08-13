from django.urls import path
from core.api.views import CategoryListAPIView

urlpatterns = [
    path('category/list/', CategoryListAPIView.as_view(), name='category_list '),
]