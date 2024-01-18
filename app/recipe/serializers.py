# Serializer for Recipe API
from rest_framework import serializers

from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    # Serializer for Recipe Class

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link']
        read_only_fields = ['id']


class RecipeDetailSerializer(RecipeSerializer):
    # Serializer for Recipe detail
    # RecipeDetailSerializer lấy RecipeSerializer làm base class vì:
    # Serialize chi tiết là extension of the recipe serializer
    # Thứ chúng ta cần ở đây là: lấy tất cả của Reipe serializer
    # và thêm các field khác nếu cần

    # Meta class là cấu trúc bắt buộc của rest_framework
    # Khai báo kế thừa Meta class của lớp cha - tận dụng model, fields đã tạo
    class Meta (RecipeSerializer.Meta):
        # Khai báo các field cần dùng: dùng hết các fields của base class
        # Lấy thêm description
        fields =RecipeSerializer.Meta.fields + ['description']
