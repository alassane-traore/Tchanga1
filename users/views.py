from django.shortcuts import render,redirect 
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password,check_password
from django.urls import reverse
from django import forms
import pyrebase  
import os
from django.conf import  settings

firebase_config={
   "apiKey":os.environ.get("apiKey"),
  "authDomain":os.environ.get("authDomainL"),
  "databaseURL": os.environ.get("DATABASE_URL"), 
  "projectId": "tchanga",
  "storageBucket":os.environ.get("storageBucket") ,
  "messagingSenderId":os.environ.get("messagingSenderId"),
  "appId": os.environ.get("appId"),
  "measurementId":os.environ.get("measurementId") 
}




firebase = pyrebase.initialize_app(firebase_config)
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


def home(req):
    try:
      if req.session['user']:
          
         print("user is aut in home !", "user:",req.session['user']['name'])
         print(req.session['user'])
         n=req.session['user']['name']
         
         print(req.session['user'])
         #rev=reverse('login')
         return  render(req, "users/home.html",context={"user":n})#redirect(rev) 
    except Exception as e:
        print("1Exception in home:",e)
        rev=reverse('login')
        return redirect(rev)
            
    try:

      rev=reverse('login')
      return redirect(rev)
    except Exception as e:
        print("2exception happened:",e)
        rev=reverse('signup')
        return redirect(rev)
        
    #return render(req, "users/home.html")

def signup(request):
    print("session:",request.session.session_key)
     
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
               if not base:
                   db.child(email.split(".")[0]).set({'name':name})
                   
               if u is not None:
                   db.child("users").child(len(u)).set(user)
               else:
                   db.child("users").child(0).set(user)
               
               
               rev=reverse("home")
               return  redirect(rev)   
       
           except Exception as e:
                 
                 message= e #"Please use an other username !"
                 return render(request,"users/signup.html",context={"message":message})
                  
               
        else:
            message="Please submit correct und complete information"
            return render(request,"users/signup.html",context={"message":message})
    else:
        message="If you have allready an accound , do not create one again !Simply login !"
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
               #user1= [o for o in n if o['mail']==name]
               print("Hey from Db:",n)
               request.session["user"]={"mail":name,'token':auth.current_user['idToken'],'name':n}#user1[0]['name']
               us=request.session.get("user")
               #print("I got this using req.session.get in login",us)
               rev=reverse("home")
               print("redirecting to home",rev)
               return redirect(rev)
           except Exception as e:
               print(e)
               message="Invalid credentials"
        
               return render(request,"users/login.html",context={"message":message})  
    return render(request,"users/login.html")
    
    
def profile(request):
    
    return render(request,"profile.html") 
        
        
def edit_profile(request):
    
    return render(request,"profiledit.html")  


    
def logingout(request):
    request.session.clear()
    #logout(request)
    rev=reverse("login")
    return redirect(rev)

def welcome(req):
    rev=reverse("home")
    return redirect(rev)
    #return render(req, "users/home.html")
