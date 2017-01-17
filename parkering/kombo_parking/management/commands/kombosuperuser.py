from django.contrib.auth.models import User
from account.models import User_data, Apartment_number
from django.core.management import BaseCommand

# create custom admin for kombo
class Command(BaseCommand):
    # Help
    help = "Creates a custom admin user for Kombo"

    # create the superuser
    def handle(self, *args, **options):

        usernameCheck = True
        emailCheck = True
        passwordCheck = True

        # check username
        username = input("Enter a username: ")
        while usernameCheck:
            if User.objects.filter(username=username).exists():
                print("This username already exists, please try another one.")
                username = input("Enter a username: ")
            else:
                user = User(username=username)
                usernameCheck = False

        # check user email, any email no validation
        email = input("Enter an email address: ")
        while emailCheck:
            if User.objects.filter(email=email).exists():
                print("This email already exists, please try another one.")
                email = input("Enter an email address: ")
            else:
                user.email = email
                emailCheck = False

        # check user password, any password no validation
        password = input("Enter a password: ")
        password_repeat = input("Enter the password again: ")
        while passwordCheck:
            if password != password_repeat:
                print("your passwords do no match, please try again")
                password = input("Enter a password: ")
                password_repeat = input("Enter the password again: ")
            else:
                user.set_password(password)
                passwordCheck = False

        # set user to superuser
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.save()

        User_Data = User_data(user=user)
        User_Data.phone_number = "None"
        User_Data.apartment = "None"
        User_Data.save()

        print("Superuser created")