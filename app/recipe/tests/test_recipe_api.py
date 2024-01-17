# Test for Recipe API
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe # Import Recipe Model
from recipe.serializers import RecipeSerializer

RECIPES_URL = reverse('recipe:recipe-list')

def create_recipe(user, **params):
    # Define a default Recipe - reusable for other tests
    defaults = {
        'title': 'Sample recipe title',
        'time_minutes': 22,
        'price': Decimal('5.25'),
        'description': 'Sample description',
        'link': 'http://example.com/recipe.pdf'
    }

    # Update defaults nếu params có giá trị
    # Trường hợp params không có giá trị, dùng giá trị defaults
    defaults.update(params)

    # Tạo recipe
    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe


# Tạo class Test Unauthenticated API requests
class PublicRecipeAPITest(TestCase):
    # Tạo hàm setup
    def setUp(self):
        self.client = APIClient()

    # Test yêu cầu: bắt buộc chứng thực người dùng
    def test_auth_required(self):
        res = self.client.get(RECIPES_URL)

        #Expected result
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

# Test for private API
class PrivateRecipeApiTest(TestCase):
    # Tạo hàm setup
    def setUp(self):
        # Create a client
        self.client = APIClient()
        # Create a user
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        # Authenticate user
        self.client.force_authenticate(self.user)

    # Test Retrive
    def test_retrive_recipe(self):
        # Tạo recipe để test - user được tạo ở phần setup
        create_recipe(user=self.user)
        create_recipe(user=self.user) # Tạo 2nd Recipe

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        #Expected result
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # Other Test Case
    def test_recipe_list_limited_to_user(self):
        other_user = get_user_model().objects.create_user(
            'otheruser@example.com',
            'testpass123'
        )
        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        #Expected result
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
