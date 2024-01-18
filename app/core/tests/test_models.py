"""
Test for models.
"""
# For recipe model
from decimal import Decimal

# import TestCase for testing
from django.test import TestCase
# reference the model directlty?
from django.contrib.auth import get_user_model

# Import models - models.py của app core
from core import models

def create_user(email='user@example.com',password='testpass123'):
    """Create and return a new user"""
    return get_user_model().objects.create_user(email,password)


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        # Test creating a user with an email is successfull.
        email = 'test@example.com'
        password = 'test123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        # Test email is normalized for new users.
        sample_emails = [
            ['test1@EXAMPLE.COM', 'test1@example.com'],
            ['Test2@Example.com','Test2@example.com'],
            ['TEST3@EXAMPLE.COM','TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]
        for email,expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email,expected)

    def test_new_user_without_email_raises_error(self):
        # Test that creating a user without an email
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('','test123')

    def test_create_superuser(self):
        # Test creating a superuser
        user=get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    # For recipe model testing
    def test_create_recipe(self):
        # Create a user that are going to assign to our recipe
        user = get_user_model().objects.create_user(
            'test@example.com',
            'test123'
        )

        #Create a recipe
        recipe = models.Recipe.objects.create(
            user = user, # Add user to the recipe
            title = 'Sample recipe name',
            time_minutes = 5,
            price = Decimal('5.50'),
            description = 'Sample recipe description'
        )

        # Test result
        self.assertEqual(str(recipe), recipe.title) # str - defined in model

    def test_create_tag(self):
        """Test for Tags model"""
        user = create_user()

        tag = models.Tag.objects.create(
            user = user,
            name = 'tag1'
        )

        self.assertEqual(str(tag), tag.name)
