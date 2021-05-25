from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import auth

@csrf_exempt
def login(request) : 

    if request.method == "POST" : #POST
        username = request.POST['username']
        password = request.POST['password']
        try :   
            user = User.objects.get(username=username) #유저가 있으면 user에 저장되고
            user = auth.authenticate(request, username=username, password=password) #해당 비밀번호가 맞는지 확인
            auth.login(request,user) #로그인
            return redirect("index")#로그인되면 메인으로 redirect
        except : #유저가 없으면
            context = {"error":'아이디 또는 비밀번호가 잘못되었습니다.', "isLoginPage": True}
            return render(request,"authentication/login.html", context)
   
    else : #GET메소드로 오면
        return render(request,"authentication/login.html", {"isLoginPage": True})
    
    
def logout(request) :
    auth.logout(request)
    context = {"logout_message":"로그아웃이 완료되었습니다."}
    return render(request,"index.html",context)