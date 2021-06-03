from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from authentication.models import User
from django.contrib import auth


@csrf_exempt
def register(request) : 
    if request.method == "POST" :   #POST
        new_user = User()
        new_user.username = request.POST['username']
        new_user.set_password(request.POST['password']) #비밀번호 암호화해서 저장
        new_user.name = request.POST['name']
        new_user.save() #DB에 저장하고
        
        auth.login(request,new_user) #로그인후 메인페이지로
        return redirect("index")
    
    else :  #GET으로 오면 회원가입 양식 띄워주기
        context={"isRegister":True}
        return render(request,"authentication/register.html",context)

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