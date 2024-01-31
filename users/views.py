from django.shortcuts import render,redirect 
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password,check_password
from django.urls import reverse
from django import forms
from Tchanga1.settings import firebase 
import os
from Tchanga1.settings import firebase
from kasse.views import select

#firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db=firebase.database()




class Signup_form(forms.Form):
    username=forms.CharField(max_length=69)
    email = forms.EmailField()
    password=forms.CharField(min_length=8,max_length=79)
    

class Login_form(forms.Form):
      username=forms.EmailField()#(max_length=69)
      password=forms.CharField(min_length=8,max_length=79)

# Create your views here.

def exists_or_signup(req,me):
   res= select([db,me],{},"get")
   
   if res is None:
       req.session.clear()
       auth.logout(req)
       return redirect(reverse("signup"))

def home(req):
    
    try:
      if req.session['user']:
         me=req.session['user']['mail']
         
         exists_or_signup(req,me.split(".")[0])
         n=req.session['user']['name']
         
         return  render(req, "users/home.html",context={"user":n})#redirect(rev) 
    except Exception as e:
        rev=reverse('login')
        return redirect(rev)
            
    try:

      rev=reverse('login')
      return redirect(rev)
    except Exception as e:
        print("exception happened:",e)
    

def signup(request):
    
    if request.method == "POST":
        post1=request.POST
        use=Signup_form(post1)
        
        if use.is_valid:
           name=post1["username"]
           email=post1["email"]
           password= post1["password"] #make_password(str())
           
           #user = User(username=name,email=email,password=password)
           try:
               auth.create_user_with_email_and_password(email,password)
               user={'name':name,'mail':email}
               u=db.child("users").get().val()
               
               base=db.child(email.split(".")[0]).get().val()
               if not base or base is None:
                   db.child(email.split(".")[0]).set({'name':name})
                   #request.session["user"]={"mail":name,'token':auth.current_user['idToken'],'name':name}
               if u is not None:
                   db.child("users").child(len(u)).set(user)
               else:
                   db.child("users").child(0).set(user)
               
               
               rev=reverse("home")
               return  redirect(rev)   
       
           except Exception as e:
                 
                 message= "Please try again!"
                 return render(request,"users/signup.html",context={"message":message})
                  
               
        else:
            message="Please submit correct und complete information"
            return render(request,"users/signup.html",context={"message":message})
    else:
        message="Signup or login !"
        return render(request,"users/signup.html",context={"message":message})


def loginin(request):
   
    if request.method=="POST":
        
        post=request.POST
        use=Login_form(post)
        message="welcome"
        if use.is_valid:
           name=request.POST["username"]
           password=request.POST["password"]    
           try:
               auth.sign_in_with_email_and_password(name,password)
               n=db.child(name.split('.')[0]).child('name').get().val()
               
               
               request.session["user"]={"mail":name,'token':auth.current_user['idToken'],'name':n}#user1[0]['name']
               
               rev=reverse("home")
               return redirect(rev)
           except Exception as e:
               print(e)
               message="Invalid credentials"
        
               return render(request,"users/login.html",context={"message":message})  
    return render(request,"users/login.html")
    
    
def profile(request):
    try:
      n=request.session['user']['name']
    except:
        pass
    
    return render(request,"users/profile.html",context={"n":n}) 
        
        
def edit_profile(request):
    
    return render(request,"profiledit.html")  


    
def logingout(request):
    request.session.clear()
    #auth.logout(request)
    #logout(request)
    rev=reverse("login")
    return redirect(rev)

def welcome(req):
    
    rev=reverse("home")
    return redirect(rev)
    #return render(req, "users/home.html")