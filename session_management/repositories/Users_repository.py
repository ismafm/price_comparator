from session_management.models import Users
class Users_repository():

    def __init__(self,user=None,password=None):

        self._user = user
        self._password = password


    # verify if the user exists in the database and return true if it is
    def exist_user(self):

        usr = Users.objects.all().filter(user=self._user)

        if usr.count() == 1:
            return True
        else:
            return False

    # verify if the password is correct for the user
    def correct_password(self):

        usr = Users.objects.get(user=self._user)

        if usr._password == self._password:
            return True
        else:
            return False