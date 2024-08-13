from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from core.api.serializers import CategorySerializers
from core.pos.models import Category


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers

    def get(self, request, *args, **kwargs):
        qeryset = self.get_serializer().Meta.model.objects.all()
        serializer = self.get_serializer_class()
        # items = [i.toJSON() for i in Category.objects.all()]
        # return Response(items)
        return Response(serializer.data)