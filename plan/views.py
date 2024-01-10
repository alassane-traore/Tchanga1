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
from .models import Task,Kategories,dates,weecklines
import pygame
import os

w_days=["Monday", "Tuesday", "Wednesday","Thursday","Friday","Saturday","Sunday" ]

my_time=datetim.datetime.now().weekday()
my_time = str(datetim.datetime.now().date()) +","+ w_days[my_time]
base_dir=settings.BASE_DIR
birds =["plan/static/plan/Bird_Ringtone(256k).mp3",
        "plan/static/plan/Birds_Ringtone____Sweet_Voice____New_Ringtones_2020____Ringtones_2.O___(256k).mp3",
        "plan/static/plan/Bird_Voice_-_Ringtone_[With_Free_Download_Link](256k).mp3"
        ]
mybird=os.path.join(base_dir,birds[2])

last_tone=""

def give_tone(req):
    global last_tone
    nw=last_tone
    pygame.mixer.init()
    pygame.mixer.music.load(mybird)
    if last_tone==""or datetim.datetime.now() > datetim.datetime(nw.year,nw.month,nw.day,nw.hour,nw.minute+2,nw.second):
      pygame.mixer.music.play()
    
      while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick()
      pygame.mixer.quit()
      last_tone=datetim.datetime.now()
    
    return HttpResponseRedirect(reverse("days"))

def find_week(date):
    date=datetime.strptime(date,'%Y-%m-%d')
    y=date.year
    m=date.month
    da=date.day
    d=datetime(y,m,da)
    cal=d.isocalendar()
    w=cal[1]
    return w

def new_time(req):
    k=Kategories.objects.all().filter(author=req.user)
    d=datetim.datetime.now()
    #dt=d
    cw=find_week(f"{d.year}-{d.month}-{d.day}")
    lines=weecklines.objects.all().filter(author=req.user,week=cw)
    
    if req.method=="POST":
      dt =req.POST["date1"].split("T")[0]
      dt1=req.POST["date1"]
      d=datetime.strptime(str(dt),'%Y-%m-%d')
      
      cw=find_week(f"{d.year}-{d.month}-{d.day}")
      lines = weecklines.objects.all().filter(author=req.user,week=cw)
      return render(req,'plan/add.html',context={"t":my_time,"k":k,"l":lines,"d":dt1})
    else:
        
        HttpResponseRedirect(reverse("add"))  
  
def add(req):
    k=Kategories.objects.all().filter(author=req.user)
    d=datetim.datetime.now()
        
    cw=find_week(f"{d.year}-{d.month}-{d.day}")
    md = ""
    if req.method=="POST":
       post=req.POST
       author=req.user
       the_date=post["date"]
       the_date=datetime.strptime(the_date,'%Y-%m-%dT%H:%M')
       y=the_date.year
       m=the_date.month
       da=the_date.day
       fd=f"{y}-{m}-{da}"
       num=post["hid"]
       selected_date=datetime.strptime(fd,'%Y-%m-%d')#T%H:%M
       for i in range(1,int(num)+1):
           classi=post[f"typo{i}"]
           el = k.filter(kategorie=classi,author=req.user)
          
           if len(el)<1:
              newK=Kategories(author=author,kategorie=classi)
              newK.save()
              
           fm=post[f"timF{i}"]
           to=post[f"timT{i}"]
           acti=post[f"act{i}"]
           kat=Kategories.objects.get(kategorie=classi,author=req.user)
           nwtask=Task(date=selected_date,author=author,begin=fm,end=to,task=acti,classi=kat)  
           nwtask.save()
    elif not req.user.is_authenticated:
        rev=reverse('login')
        return redirect(rev) 
    
    return render(req,'plan/add.html',context={"t":my_time,"k":k,"d":md})
    #else: 
     #return render(req,'plan/add.html',context={"t":my_time,"k":k,"l":lines})

def add_week(req):
    if req.method=="POST":
        dt=req.POST["week"].split("T")[0]
        dt=str(dt)
       
        w=find_week(dt)
        author=req.user
        l=req.POST["line"]
        
        if author is not None and w is not None and l !="":
           myweek=weecklines(author=author,week=w,line=l)
           myweek.save()
    elif not req.user.is_authenticated:
        rev=reverse('login')
        return redirect(rev) 
        
      
    return render(req,'plan/weeklines.html',context={"t":my_time})

def transit(req):
    
    return render(req,'plan/transit.html',context={"t":my_time})

def ordi(taff1):
    taff2=[]
    
    for el in taff1:  
      taff2.append(el["begin"])
        
    taff=[]
    taff2.sort()
    for t in taff2:
        if type(taff1)!=list:
          ti=taff1.get(begin=t)
          taff.append(ti)
        else:
            for i in taff1:
                if i["begin"] == t:
                    taff.append(i)
    if type(taff1)==list:
      taff0=[]
      for el in taff:
         taff0.append(el["date"])
      taff3=[]
      taff4=[]
      taff0.sort()
      for n in taff0:
        for i in taff:
          if i["date"] == n :
            if not n in taff4:
                taff4.append(n)
            else:
                i["date"]=""
            taff3.append(i)
            taff.remove(i)              
      taff=taff3
    return taff

def days(req):
    #tm=datetime.utcnow()
    #local=pytz.timezone('Europe/Berlin')
    #localtime=tm.replace(tzinfo=pytz.utc).astimezone(local)
    #.datetime.now()
    
    lc = get_localzone()
    
    tm=datetime.now(lc)
    
    y=tm.year
    m=tm.month
    da=tm.day
    fd=f"{y}-{m}-{da}"
    t=datetime.strptime(fd,'%Y-%m-%d')
    taff1 = Task.objects.all().filter(author=req.user,date=t)
    taff0=[]
    for i in taff1:
       
        taff0.append(str(i.begin))
    taff0.sort()
    taff=[]
    for i in taff0:
        el = taff1.get(begin =i)
        ob={}
        ob["begin"]=i[:-3]
        ob["end"]=str(el.end)[:-3]
        ob["task"]=el.task
        ob["classi"]=el.classi
        ob["date"]=el.date
        ob["author"]=el.author
        ob["id"]=el.id
        taff.append(ob)
    if not req.user.is_authenticated:
        rev=reverse('login')
        return redirect(rev) 
              
      
    return render(req,'plan/today.html',context={"t":my_time,"taff":taff})

def week(req):
    today=datetim.datetime.now()
    current_Week=find_week(f"{today.year}-{today.month}-{today.day}")
    
    we=Task.objects.all().filter(author=req.user)
    
    wee=[]
    for el in we:
        
        if el.date is not None and find_week(f"{el.date.year}-{el.date.month}-{el.date.day}")== current_Week:
            wee.append(el)
    
    da=[]
    for i in wee:
        if not str(i.date) in da:
          da.append(str(i.date))  
        
    da.sort()
    da=da[::-1]
    wee1=[]
    taff0=[]
    w=[]
    verifier=[]
    for i in da:
        one=[]
        for el in wee:
            if str(el.date) ==i: 
                wee1.append(el)
        for el in wee1:
          if str(el.date) ==i:
            one.append(str(el.begin))
        one.sort()
        if not one in taff0:
          taff0.append(one)
    
        for ar in taff0:
         for el1 in ar:
          for o in wee1:
           if str(o.begin)==el1 and str(o.date)==i :
           
            ob={}
            ob["begin"]=str(o.begin)[:-3]
            ob["end"]=str(o.end)[:-3]
            ob["task"]=o.task
            ob["classi"]=o.classi
            
            ob["author"]=o.author
            ob["id"]=o.id
            if not o.date in verifier:
                verifier.append(o.date)
                ob["date"]=o.date
            else:
                ob["date1"]=o.date
            w.append(ob)    
    w1=[]
    v=[]
    for ob in w:
        if not ob["id"] in v:
            w1.append(ob)
            v.append(ob["id"])
    if not req.user.is_authenticated:
        rev=reverse('login')
        return redirect(rev) 
         
    return render(req,'plan/week.html',context={"t":my_time,"week":w1})

def months(req):
    mo=datetim.datetime.now().month
    fmo=Task.objects.all().filter(author=req.user)
    moar=[]
    for el in fmo:
        if el.date:
          date=datetime.strptime(f"{el.date.year}-{el.date.month}-{el.date.day}",'%Y-%m-%d')
          if date.month == mo and not el in moar:
             moar.append(el)
    da=[]
    for i in moar:
        d=datetim.datetime(i.date.year,i.date.month,i.date.day)
       
        if not d in da:
          da.append(d)  
        
    da.sort()
    
    da=da[::-1]
    
    wee1=[]
    taff0=[]
    m=[]
    verifier=[]
    for i in da:
        one=[]
        for el in moar:
            d=datetim.datetime(el.date.year,el.date.month,el.date.day)
            if d ==i: 
                wee1.append(el)
        for el in wee1:
          d=datetim.datetime(el.date.year,el.date.month,el.date.day)
          if d ==i:
            one.append(el.begin)
        one.sort()

        taff0.append(one)
    
        for ar in taff0:
         for el1 in ar:
          for o in wee1:
           d=datetim.datetime(o.date.year,o.date.month,o.date.day)
           
           if el1==o.begin and d==i :
           
            ob={}
            ob["begin"]=str(o.begin)[:-3]
            ob["end"]=str(o.end)[:-3]
            ob["task"]=o.task
            ob["classi"]=o.classi
            
            ob["author"]=o.author
            ob["id"]=o.id
            if not d in verifier:
                verifier.append(d)
                ob["date"]=o.date
            else:
                ob["date1"]=o.date
            m.append(ob) 
    m1=[]
    v=[]
    for ob in m:
        if not ob["id"] in v:
            m1.append(ob)
            v.append(ob["id"])
            
    if not req.user.is_authenticated:
        rev=reverse('login')
        return redirect(rev) 
   
    return render(req,'plan/month.html',context={"t":my_time,"mo":m1})

def types(req):
    if req.method=="POST":
        classi=req.POST["typo"]
        author=req.user
        
        if author is not None and classi is not None:
           k=Kategories(author=author,kategorie=classi)
           
           k.save()
    elif not req.user.is_authenticated:
        rev=reverse('login')
        return redirect(rev)  
           
    return render(req,'plan/types.html',context={"t":my_time})

def give_to_update_object(req,id):
    
      ob=Task.objects.get(id=id) #.filter(author=req.user,id=id)
      k=Kategories.objects.all().filter(author=req.user)
     
      dat1=ob.date
      dat=datetime.strptime(f"{dat1.month}-{dat1.day}-{dat1.year}",'%m-%d-%Y')
      wk=find_week(str(dat1))
      
      lines = weecklines.objects.all().filter(author=req.user,week=wk)
      
      return render(req,'plan/update.html',context={"t":my_time,"k":k,"l":lines,"task":ob,"d":dat})

def remov(req,id):
    ob=Task.objects.get(id=id)
    #delet =ob.task
    
    ob.delete()
    return redirect("days")
    #return render(req,'plan/delete.html',context={"t":my_time,"del":delet})