from django.core.management.base import BaseCommand, CommandError
from core.models import Profile
from django.contrib.auth.models import User
class Command(BaseCommand):
    help = 'creates user profiles for existing users created before the profile implementation'

    def handle(self, *args, **options):
        users = User.objects.filter(profile=None)
        for u in users:
            Profile.objects.create(user=u)
            self.stdout.write(self.style.SUCCESS('Created profile for user %s' % u.id))