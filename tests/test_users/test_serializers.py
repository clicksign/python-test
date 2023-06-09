import pytest
from django.forms.models import model_to_dict

from .factories import UserFactory, UserProfileFactory
from users.models import UserProfile
from users.serializers import UserProfileSerializer, UserSerializer

pytestmark = pytest.mark.django_db


def test_user_profile_serializer():
    user_profile = UserProfileFactory()
    serializer = UserProfileSerializer(data=model_to_dict(user_profile))
    assert serializer.is_valid() is True


def test_user_serializer_create():
    user_data = UserFactory.build()
    profile_data = UserProfileFactory.build()
    data = {
        "username": user_data.username,
        "password": user_data.password,
        "email": user_data.email,
        "profile": {
            "name": profile_data.name,
            "role": profile_data.role,
            "phone_number": profile_data.phone_number,
            "address": profile_data.address,
        },
    }
    serializer = UserSerializer(data=data)
    assert serializer.is_valid()
    created_user = serializer.save()

    assert UserProfile.objects.filter(user=created_user).exists()


def test_user_serializer_create_invalid():
    user_data = UserFactory.build()
    data = {
        "username": user_data.username,
        "password": user_data.password,
        "email": user_data.email,
    }
    serializer = UserSerializer(data=data)
    assert serializer.is_valid() is False
    assert "profile" in serializer.errors
