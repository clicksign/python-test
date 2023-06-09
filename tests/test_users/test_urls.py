from django.urls import reverse


def test_user_urls():
    assert reverse("user-list") == "/v1/users/"
    assert reverse("user-detail", args=[1]) == "/v1/users/1/"


def test_user_profile_urls():
    assert reverse("userprofile-list") == "/v1/profiles/"
    assert reverse("userprofile-detail", args=[1]) == "/v1/profiles/1/"
