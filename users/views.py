from django.shortcuts import render,redirect 
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password,check_password
from django.urls import reverse
from django import forms

class Signup_form(forms.Form):
    username=forms.CharField(max_length=69)
    email = forms.EmailField()
    password=forms.CharField(min_length=8,max_length=79)
    

class Login_form(forms.Form):
      username=forms.CharField(max_length=69)
      password=forms.CharField(min_length=8,max_length=79)

# Create your views here.


def home(req):
    try:
      if req.user.is_authenticated:
         print("user is aut in home !")
         #rev=reverse('login')
         return  render(req, "users/home.html")#redirect(rev) 
    except Exception as e:
         print("exception in home:",e)
         #rev=reverse('login')
         #return redirect(rev)
    try:
      print("redirecting to login") 
      rev=reverse('login')
      return redirect(rev)
    except Exception as e:
        print("exception happened:",e)
        
    #return render(req, "users/home.html")

def signup(request):
    if request.method == "POST":
        post1=request.POST
        use=Signup_form(post1)
        
        if use.is_valid:
           name=post1["username"]
           email=post1["email"]
           password= make_password(str(post1["password"]))
           user = User(username=name,email=email,password=password)
           try:
               user1=User.objects.get(name,None)
               if user1 is not None:
                  message="Please use an other username !"
                  return render(request,"users/signup.html",context={"message":message})
               else:
                  user.save()
                  rev=reverse("home")
                  return  redirect(rev)
                   
           except:
               message="Please use an other username 2!"
               return render(request,"users/signup.html",context={"message":message})
        else:
            message="Please submit correct und complete information"
            return render(request,"users/signup.html",context={"message":message})
    else:
        message="If you have allready an accound , do not create one again !Simply login !"
        return render(request,"users/signup.html",context={"message":message})


def loginin(request):
    """try:
      if not request.method=="POST" and request.user.is_authenticated:
        print("try in login")
       
        print("trying to check !")
        ev=reverse("home")
        return redirect(ev)
      #  return check_user_account(request,request.user,"login")
    except:
        
        pass"""
    if request.method=="POST":
        
        post=request.POST
        use=Login_form(post)
        if use.is_valid:
           name=request.POST["username"]
           password=request.POST["password"]    
           user = authenticate(request,username=name,password=password)
           if user is not None:
              login(request,user)
              return redirect(reverse("days")) # HttpResponseRedirect(reverse("plan/today.html"))
           else:
              message="Invalid credentials"
              return render(request,"users/login.html",context={"message":message})
    
     
       
    return render(request,"users/login.html")
    
def profile(request):
    
    return render(request,"profile.html") 
        
        
def edit_profile(request):
    
    return render(request,"profiledit.html")  


    
def logingout(request):
   
    logout(request)
    rev=reverse("login")
    return redirect(rev)

def welcome(req):
    rev=reverse("home")
    return redirect(rev)
    #return render(req, "users/home.html")
