from django.core.management.base import BaseCommand
from apps.users.models import CustomUser


class Command(BaseCommand):
    help = 'Create initial users'

    def handle(self, *args, **options):
        users_data = [
            {
                "username": "client",
                "password": "client123",
                "user_group": 2
            },
            {
                "username": "seller",
                "password": "seller123",
                "user_group": 3
            },
        ]

        for user_data in users_data:
            if not CustomUser.objects.filter(username=user_data['username']).exists():
                CustomUser.objects.create_user(
                    username=user_data['username'],
                    password=user_data['password'],
                    user_group=user_data['user_group']
                )
                self.stdout.write(self.style.SUCCESS(
                    f'Successfully created new user: {user_data["username"]} - {user_data["password"]}'))
            else:
                self.stdout.write(self.style.SUCCESS(
                    f'User {user_data["username"]} already exists - {user_data["password"]}'))
