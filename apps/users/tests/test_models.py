from django.test import TestCase
from django.contrib.auth import get_user_model


class CustomUserModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        User.objects.create(username='admin', user_group=1)
        User.objects.create(username='client', user_group=2)
        User.objects.create(username='seller', user_group=3)

    def test_user_creation(self):
        User = get_user_model()
        admin = User.objects.get(username='admin')
        client = User.objects.get(username='client')
        seller = User.objects.get(username='seller')

        self.assertEqual(admin.username, 'admin')
        self.assertEqual(admin.user_group, 1)

        self.assertEqual(client.username, 'client')
        self.assertEqual(client.user_group, 2)

        self.assertEqual(seller.username, 'seller')
        self.assertEqual(seller.user_group, 3)

    def test_user_retrieval(self):
        User = get_user_model()
        admin = User.objects.get(username='admin')
        client = User.objects.get(username='client')
        seller = User.objects.get(username='seller')

        self.assertEqual(admin.username, 'admin')
        self.assertEqual(client.username, 'client')
        self.assertEqual(seller.username, 'seller')

    def test_user_update(self):
        User = get_user_model()
        user = User.objects.get(username='admin')

        user.username = 'new_admin'
        user.save()

        updated_user = User.objects.get(pk=user.pk)
        self.assertEqual(updated_user.username, 'new_admin')

    def test_user_deletion(self):
        User = get_user_model()
        user = User.objects.get(username='admin')

        user.delete()

        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username='admin')

    def test_user_str_representation(self):
        User = get_user_model()
        admin = User.objects.get(username='admin')
        client = User.objects.get(username='client')
        seller = User.objects.get(username='seller')

        self.assertEqual(str(admin), 'admin')
        self.assertEqual(str(client), 'client')
        self.assertEqual(str(seller), 'seller')

    def test_user_count(self):
        User = get_user_model()
        user_count = User.objects.count()

        self.assertEqual(user_count, 3)

    def test_user_filtering(self):
        User = get_user_model()
        seller_users = User.objects.filter(user_group=3)

        self.assertEqual(seller_users.count(), 1)
        self.assertEqual(seller_users.first().username, 'seller')

    def test_user_ordering(self):
        User = get_user_model()
        users = User.objects.order_by('username')

        self.assertEqual(users[0].username, 'admin')
        self.assertEqual(users[1].username, 'client')
        self.assertEqual(users[2].username, 'seller')
