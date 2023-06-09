import pytest

from .factories import UserProfileFactory
from users.models import UserProfile

pytestmark = pytest.mark.django_db


def test_create_user_profile():
    user_profile = UserProfileFactory()
    assert isinstance(user_profile, UserProfile)
    assert UserProfile.objects.count() == 1
