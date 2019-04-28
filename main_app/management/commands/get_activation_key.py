from users.models import CustomUser, Subscriptions, Profile
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

#this management command is used to get some users activation_key for debugging purposes

class Command(BaseCommand):
    help = 'Get users activation key for debugging'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='email of user')


    def handle(self, *args, **kwargs):
        username = kwargs['username']
        User_name = CustomUser.objects.get(email=username)
        #access users profile onetoone field
        profile = User_name.profile

        print(str(profile.activation_key))

