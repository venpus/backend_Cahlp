from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError

class Command(createsuperuser.Command):
    help = 'Create a superuser with both username and email'

    def handle(self, *args, **options):
        # Prompt for username
        username = input("Enter username: ")
        while not username:
            username = input("Username cannot be empty. Enter username: ")

        # Prompt for email
        email = input("Enter email: ")
        while not email:
            email = input("Email cannot be empty. Enter email: ")

        # Set options
        options['username'] = username
        options['email'] = email

        # Call the original createsuperuser.Command.handle method
        super().handle(*args, **options)
