from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.urls import reverse
import datetime as datetim
from datetime import datetime
import time
import pytz
from tzlocal import get_localzone
from django.utils import timezone
from .models import Sector,Basket,Goods
import pygame
import os

print("localtime:",timezone.localtime(timezone.now()))

print("gettimezone:",get_localzone())

def create_date(period,begin):
    b=""
    y=begin.year
    m=begin.month
    d=begin.day
    ni=period
    for i in range(ni):
        d+=1
        try:
            b=datetim.datetime(y,m,d)  
                       
        except:
         try:
            ni1=i
            m+=1
            d=1 
            b=datetim.datetime(y,m,d)
            create_date(ni1,b)  
            
         except:
            ni2=i
            y+=1
            m=1
            d=1 
            b=datetim.datetime(y,m,d)
            create_date(ni2,b) 
            
    return b

def new_sector(req):
    s = Sector.objects.all().filter(author=req.user)
    
    if req.method =="POST":
       post=req.POST
       author = req.user
       begin = post["begin"]
       end = post["end"]
       sector=post["sector"]
       budget= eval(post["budget"])
       auto=True
       try:
         if post["yes"]:
           auto=True
         else:
            auto=False
       except  :
           auto=False
           
           
       ms=Sector(author=author,name=sector,begin=begin,end=end,budget=budget,automate=auto)
       ms.save()
    elif not req.user.is_authenticated:
        rev=reverse('login')
        return redirect(rev) 
    return render(req,"kasse/sectors.html")



def add_list(req):
  nw = datetim.datetime.now()
  s=Sector.objects.all().filter(author=req.user)
  g=Goods.objects.all().filter(author=req.user)
  gs=[]
  for j in g :
      #d=datetim.datetime(j.d.year,j.d.month,j.d.day,j.d.hour,j.d.minute)
      f=j.s.begin
      t=j.s.end
      f=datetim.datetime(f.year,f.month,f.day,f.hour,f.minute)
      t=datetim.datetime(t.year,t.month,t.day,t.hour,t.minute)
      
      if f<=nw and t>=nw and j.booked==False:
          gs.append(j)
  leng=len(gs)      
  cs=[]
  
  for o in s:
       nb=datetim.datetime(o.begin.year,o.begin.month,o.begin.day,o.begin.hour,59)
       nt=datetim.datetime(o.end.year,o.end.month,o.end.day,o.end.hour,59)
       busk=Basket.objects.filter(sector=o)
       costs=0
       for b in busk:
           if b.d>=o.begin and b.d<=o.end :
             costs+=b.costs
           
       if nb<=nw and nt>=nw:
           cs.append(o)
           
       elif nt<nw and o.automate:
          
           period=o.end-o.begin
           period=period.days
           nb=create_date(1,o.end)
           ne=create_date(period,nb)
           rest = o.budget-costs
           o.budget=o.budget+rest
           o.begin=nb
           o.end=ne
           print("renewing", o.name,"lastdate:", o.end, "newDate:",nb )
           o.save()
           cs.append(o)
  if req.method=="POST":
    post=req.POST
    #dat=post["date"]
    n=post["good"]
    s= Sector.objects.get(id=post["sector"])
    new_good=Goods(author=req.user,s=s,name=n)
    
    new_good.save()
    
    return redirect("addlist")
  elif not req.user.is_authenticated:
        rev=reverse('login')
        return redirect(rev) 
     
  return render(req,"kasse/addliste.html",context={"li":gs,"cs":cs,"len":leng})




def shopping_list(req):
    
    
    return render(req, "kasse/kaufliste.html")


             
            
def markets(req):
   
   if req.method=="POST":
     
     id=req.POST["id"]
     
     s=Sector.objects.all().get(id=id)
    
     basks=Basket.objects.filter(sector=s)
     #print(basks)
     cost=0
     for i in basks:
        if i.d >=s.begin and i.d<=s.end :
          cost+=i.costs
     s.c="{:.2f}".format(s.budget-cost)
     
     li=Goods.objects.filter(author=req.user)
     #f=s.begin
     #t=s.end
     li1=li.filter(s=s,booked=False)
     
     """for l in li:
         if f<=l.d and t>=l.d and not l.booked and l.s==s:
             li1.append(l)"""
      
     return render(req,"kasse/basket.html",context={"sc":s,"li":li1})
   elif not req.user.is_authenticated:
        rev=reverse('login')
        return redirect(rev) 
      
   nw = datetim.datetime.now()
   s = Sector.objects.all().filter(author=req.user)
   cs=[]
   for o in s:
       nb=datetim.datetime(o.begin.year,o.begin.month,o.begin.day,o.begin.hour,59)
       nt=datetim.datetime(o.end.year,o.end.month,o.end.day,o.end.hour,59)
       basks=Basket.objects.filter(sector=o)
       
       cost=0
       for i in basks:
          if i.d >=o.begin and i.d<=o.end :
            cost+=i.costs
          
       if nb<=nw and nt>=nw:
           
           o.c="{:.2f}".format(o.budget-cost)
           cs.append(o)
       elif nt<nw and o.automate:
           period=o.end-o.begin
           period=period.days
           nb=create_date(1,o.end)
           ne=create_date(period,nb)
           rest = o.budget-cost
           o.budget=o.budget+rest
           o.begin=nb
           o.end=ne
           o.save()
           cs.append(o)
           
   return render(req,"kasse/market.html",context={"sector":cs})


def basket(req):
    if req.method=="POST":
      post=req.POST
      nw = datetim.datetime.now()
      sid=post["id"]
      s=Sector.objects.get(id=sid)
      
      comment =post["comment"]
      prise =post["prise"]
      
      goodn=post["goodnum"]
      goodn=int(goodn)
      
      liste=[]
      for i in range(goodn+1):
        try:
          g=Goods.objects.get(id=post[f"good{i}"])
          if g is not None:
             
             g.s=s
             g.booked=True
             
             g.save()
             liste.append(g)
             
        except:
            pass
      baskt=Basket(author=req.user,d=nw,costs=eval(prise),comment=comment,sector=s)
      baskt.save()
      for o in liste:
        el=baskt.kaufliste.filter(id=o.id)
        if len(el)<1:
           baskt.kaufliste.add(o)
         #baskt.save()
      
      return HttpResponseRedirect(reverse("market"))
    elif not req.user.is_authenticated:
        rev=reverse('login')
        return redirect(rev)  
      
    return render(req,"kasse/basket.html")


def transit1(req):
    
    return render(req,'kasse/transit.html')
      

def count(req):
    sector=Sector.objects.filter(author=req.user)
    bt=[]
    totalcosts=0
    for s in sector:
     bu=s.buskets.all()
     costs=0
     s.b=bu
     for b in bu:
       costs+=b.costs
       totalcosts+=b.costs
       gu=b.kaufliste.all()
       b.li=gu
       b.len=len(gu)
       for g in range(len(gu)):
           if g==0:
               gu[g].d=b.d
               gu[g].costs="{:.2f}".format(b.costs)
     s.costs= "{:.2f}".format(costs)
    totalcosts= "{:.2f}".format(totalcosts)    
    return render(req,"kasse/counter.html",context={"sector":sector,"b":bt,"total":totalcosts})
      
    
    
def hist(req):
    
    
    return render(req,"kasse/history.html")

def removit(req,id):
    ob=Goods.objects.get(id=id)
    #delet =ob.task
    print(ob)
    ob.delete()
    return redirect("addlist")