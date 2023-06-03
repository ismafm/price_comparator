from django.http import HttpResponse
from session_management.repositories.Users_repository import Users_repository
from django.shortcuts import render, redirect
import datetime
def login(request):
    #obtain the session message error if exists
    usr_sess_msg = request.session.get("usr_msg","")
    pass_sess_msg = request.session.get("pass_msg","")
    username = request.session.get("usr_name","")
    #return HttpResponse(usr_sess_msg)
    return render(request, "login.html", {"usr_msg":usr_sess_msg,"pass_msg":pass_sess_msg,"username":username})

def logout(request):
    request.session.flush()
    return redirect("/")

def login_verification(request):

    usr = request.POST["user"]
    pss = request.POST["pass"]

    #creates the user object
    user = Users_repository(usr,pss)

    if user.exist_user():
        if user.correct_password():
            request.session["pass_msg"] = ""
            request.session["usr_msg"] = ""
            request.session["usr_name"] = usr
            request.session["usr_session"] = user.user_hash()
            return redirect('/search/')
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

def profile(request):
    id_hash_object = Users_repository(id_hash=request.session["usr_session"])
    usr_info = id_hash_object.hash_user()
    #return HttpResponse(usr_info.born_date)
    return render(request, "profile.html",{"usr":usr_info})

def change_info(request):
    info_type = request.GET["info_type"]
    #texto informativo
    text = ""
    if info_type == "user":
        text = "Cambie su nombre de usuario:"
    elif info_type == "email":
        text = "Cambie su correo electrónico:"
    elif info_type == "mobile":
        text = "Cambie su número de teléfono:"
    elif info_type == "pass":
        text = "Cambie su contraseña:"
    return render(request, "info.html", {"text_info":text, "info_type":info_type})
def apply_changes(request):
    info_type = request.POST["info_type"]
    new_info = request.POST["new_info"]
    hash = request.session["usr_session"]
    if info_type == "user":
        usr = Users_repository(id_hash=hash, user=new_info)
        usr.change_user()
    elif info_type == "email":
        usr = Users_repository(id_hash=hash, email=new_info)
        usr.change_email()
    elif info_type == "mobile":
        usr = Users_repository(id_hash=hash, mobile=new_info)
        usr.change_mobile()
    elif info_type == "pass":
        usr = Users_repository(id_hash=hash, password=new_info)
        usr.change_password()
    return redirect("/profile/")