from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class EmailLogin(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):

        try:

            user = UserModel.objects.get(email=username)

        except UserModel.DoesNotExist:
            
            print("User not found")
            return None

        if user.check_password(password): 

            if user.is_active: 

                return user
            
            print("User is inactive")

        else:

            print("Incorrect password") 

        return None
    
    def get_user(self, user_id):

        try:

            return UserModel.objects.get(pk=user_id)
        
        except UserModel.DoesNotExist:

            return None
