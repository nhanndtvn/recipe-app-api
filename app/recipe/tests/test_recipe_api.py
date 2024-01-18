# Test for Recipe API
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe # Import Recipe Model
from recipe.serializers import (
    RecipeSerializer,
    RecipeDetailSerializer,
    )

RECIPES_URL = reverse('recipe:recipe-list')

def detail_url(recipe_id):
    # Create and return a recipe detail URL
    return reverse('recipe:recipe-detail', args=[recipe_id])

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

# Create user for testing
def create_user(**params):
    return get_user_model().objects.create_user(**params)


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
        """
        This code was replace after define the create_user(**params)
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        """
        self.user = create_user(
            email='test@example.com',
            password='testpass123'
        )
        # Authenticate user - set user tự động login khi test
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
        """
        Refactore
        other_user = get_user_model().objects.create_user(
            'otheruser@example.com',
            'testpass123'
        )
        """
        other_user = create_user(
            email='otheruser@example.com',
            password='testpass123'
        )
        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        #Expected result
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # Test for Recipe detail
    def test_recipe_detail(self):
        # 1.Tạo recipe
        recipe = create_recipe(user=self.user)

        # 2.Khai báo Url - id là id của recipe đã tạo ở bước 1
        url = detail_url(recipe.id)

        # 3.Giả lập request - lấy response
        res = self.client.get(url)

        # 4. Serialization: chuyển đổi object recipe -> định dạng có thể lưu
        # deserialization > phục hồi đối tượng đã chuyển đổi
        # đây là bước chuyển đổi từ dữ liệu đã lưu > dữ liệu có thể xem hay deserialization
        serializer = RecipeDetailSerializer(recipe)

        #5. Kết quả kỳ vọng: data của respone là data của serializer (data sau khi chuyển đổi)
        self.assertEqual(res.data, serializer.data)

    # Test creating recipe
    def test_create_recipe(self):
        #1. Tạo dữ liệu test
        payload = {
            'title': 'Sample recipe',
            'time_minutes': 30,
            'price': Decimal('5.99'),
        }

        # 2. Giải lập client gọi POST đến RECIPES_URL với content là payload
        res = self.client.post(RECIPES_URL, payload)

        # 3.Kết quả expected
        # Insert thành công
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # Lấy object đã tạo và so sánh với input
        recipe = Recipe.objects.get(id=res.data['id'])

        # k - key, v - value
        # Loop dict
        for k, v in payload.items():
            # Kết quả kỳ vọng
            # getattr(recipe,k) - lấy giá trị của attribute k trong recipe
            # giá trị của k phải bằng v của payload - insert đúng tất cả fields
            self.assertEqual(getattr(recipe, k),v)

        #Kết quả kỳ vọng - đúng user tạo recipe
        self.assertEqual(recipe.user, self.user)

    # Test for partial update
    def test_partial_update(self):
        original_link = 'http://example.com/recipe.pdf'
        recipe = create_recipe(
            user=self.user,
            title='Sample recipe title',
            link=original_link,
        )
        payload={'title':"New recipe title"}
        url = detail_url(recipe.id)
        res = self.client.patch(url,payload)
        # PATCH success
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Làm mới recipe lấy từ database
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.link, original_link)
        self.assertEqual(recipe.user, self.user)

    # Test full update for recipe
    def test_full_update(self):
        original_link = 'http://example.com/recipe.pdf'
        recipe = create_recipe(
            user=self.user,
            title='Sample recipe title',
            link=original_link,
            description = "Sample recipe description",
        )

        payload={
            'title': "New recipe title",
            'link': "http://example.com/new-recipe.pdf",
            'description': 'New recipe description',
            'time_minutes': 30,
            'price': Decimal('2.50'),
        }

        url = detail_url(recipe.id)
        res = self.client.put(url, payload)

        # PUT success
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Làm mới recipe lấy từ database
        recipe.refresh_from_db()

        for k,v in payload.items():
            self.assertEqual(getattr(recipe,k),v)

        self.assertEqual(recipe.user, self.user)

    # Test changing recipe user result in error
    def test_update_user_returns_error(self):
        new_user = create_user(
            email="newuser@example.com",
            password='newpass123'
        )
        recipe = create_recipe(user=self.user)

        payload ={'user':new_user.id}

        url = detail_url(recipe.id)
        res = self.client.patch(url, payload)

        recipe.refresh_from_db()
        # Do not update user
        self.assertEqual(recipe.user, self.user)

    # Test deleting a recipe success full
    def test_delete_recipe(self):
        # Tạo recipe
        recipe = create_recipe(user=self.user)

        url = detail_url(recipe.id)
        # Delete recipe
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())

    def test_recipe_other_users_recipe_error(self):
        new_user = create_user(
            email="newuser@example.com",
            password='newpass123'
        )

        recipe = create_recipe(user=new_user)

        url = detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Recipe.objects.filter(id=recipe.id).exists())



