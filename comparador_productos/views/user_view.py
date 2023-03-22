from django.http import HttpResponse
from django.template import loader
from login.repositories.Users_repository import Users_repository
from django.shortcuts import render, redirect

def login(request):
    #obtain the session message error if exists
    usr_sess_msg = request.session.get("usr_msg","")
    pass_sess_msg = request.session.get("pass_msg","")
    username = request.session.get("usr_name","")
    #return HttpResponse(usr_sess_msg)
    return render(request, "login.html", {"usr_msg":usr_sess_msg,"pass_msg":pass_sess_msg,"username":username})

def login_verification(request):

    usr = request.POST["user"]
    pss = request.POST["pass"]

    #creates the user object
    user = Users_repository(usr,pss)

    if user.exist_user():
        if user.correct_password():
            return HttpResponse("Funciona!!")
        else:
            # if the password is not correct introduces the error message and deletes the error message from the user
            request.session["pass_msg"] = "La contraseña introducida es errónea, por favor, introduce la contraseña correcta"
            request.session["usr_msg"] = ""
            # saves the user name to write in login form
            request.session["usr_name"] = usr
            return redirect("/login/")
    else:
        # if the user is not correct introduces the error message and deletes the error message from the password
        request.session["usr_msg"] = "El usuario introducido no existe"
        request.session["pass_msg"] = ""
        # saves the user name to write in login form
        request.session["usr_name"] = usr
        return redirect("/login/")
