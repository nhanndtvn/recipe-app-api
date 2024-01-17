# Views for Recipe API
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers

class RecipeViewSet(viewsets.ModelViewSet):
    # View for manage recipe apis
    serializer_class = serializers.RecipeSerializer
    # Queryset - represent objects available for view
    queryset = Recipe.objects.all()
    # Set Authentication - Phải dùng Token authen cho bất
    # kỳ endpoints nào được cung cấp bới viewset
    # Nếu gọi API mà không chứng thực sẽ bị lỗi
    authentication_classes = [TokenAuthentication]
    # Set Permission class
    permission_classes = [IsAuthenticated]

    # Override - GET query set method
    def get_queryset(self):
        # Retrieve recipes for authenticated user
        return self.queryset.filter(user=self.request.user).order_by('-id')
