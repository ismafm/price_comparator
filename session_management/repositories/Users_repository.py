from session_management.models import Users
class Users_repository():

    def __init__(self,user=None,password=None,email=None, mobile=None, born_date=None, id_hash=None, admin=False, photo_url='img/profile_photos/none.jpg'):

        self._user = user
        self._password = password
        self._email = email
        self._mobile = mobile
        self._born_date = born_date
        self._id_hash = id_hash
        self._admin = admin
        self._photo_url = photo_url


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

        if usr.password == self._password:
            return True
        else:
            return False
    #recupera el usuario completo basandose en el hash
    def hash_user(self):

        usr = Users.objects.get(id_hash=self._id_hash)
        return usr
    #recupera el hash a partir del nombre de usuario
    def user_hash(self):

        usr_hash = Users.objects.get(user=self._user)
        return usr_hash.id_hash
    def change_password(self):
        usr = self.hash_user()
        usr.password = self._password
        usr.save()
    def change_user(self):
        usr = self.hash_user()
        usr.user = self._user
        usr.save()
    def change_email(self):
        usr = self.hash_user()
        usr.email = self._email
        usr.save()
    def change_mobile(self):
        usr = self.hash_user()
        usr.mobile = self._mobile
        usr.save()