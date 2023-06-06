from django.conf import settings
from django.core.management.base import BaseCommand
from apps.users.models import CustomUser


class Command(BaseCommand):
    help = 'Create super user'

    def handle(self, *args, **options):
        if not CustomUser.objects.filter(username=settings.ADMIN_USERNAME).exists():
            CustomUser.objects.create_superuser(
                username=settings.ADMIN_USERNAME,
                email=settings.ADMIN_EMAIL,
                password=settings.ADMIN_PASSWORD,
                user_group=1  # 1 = Admin
            )
            self.stdout.write(self.style.SUCCESS('Successfully created new super user'))
        else:
            self.stdout.write(self.style.SUCCESS('Super user already exists'))
