from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.urls import reverse
import datetime as datetim
from datetime import datetime,timedelta
import time
import pytz
from tzlocal import get_localzone
from .models import Task #,Kategories,dates,weecklines
import os
from users.views import db
from kasse.views import select,validate,create_date



w_days=["Monday", "Tuesday", "Wednesday","Thursday","Friday","Saturday","Sunday" ]
my_months=["", "January", "February","March","April", "May", "June", "July","August","September","October","November","December"]
my_time=datetim.datetime.now().weekday()
my_time = str(datetim.datetime.now().date()) +","+ w_days[my_time]
base_dir=settings.BASE_DIR
birds =["plan/static/plan/Bird_Ringtone(256k).mp3",
        "plan/static/plan/Birds_Ringtone____Sweet_Voice____New_Ringtones_2020____Ringtones_2.O___(256k).mp3",
        "plan/static/plan/Bird_Voice_-_Ringtone_[With_Free_Download_Link](256k).mp3"
        ]
mybird=os.path.join(base_dir,birds[0])

def find_week(date):
    date=datetime.strptime(date,'%Y-%m-%d')
    y=date.year
    m=date.month
    da=date.day
    d=datetime(y,m,da)
    cal=d.isocalendar()
    w=cal[1]
    return w

def class_or_head(id,end_point,val,key,option):
    if id is not None and val is not None:
            li=[]
            try:
             
              k=db.child(id).child(end_point).get().val()
              if len(k)>0:
                  if end_point =="weekt":
                    
                    li=db.child(id).child(end_point).child(option).get().val()
                    li.append(val)
                    db.child(id).child(end_point).child(option).set(li)
                    
                   # db.child(id).child(end_point).child(len(k)).child(option).set({key:val})
                  else:
                      db.child(id).child(end_point).child(len(k)).set({key:val})
                      
              else:
                  if end_point =="weekt":
                    try:
                      li=db.child(id).child(end_point).child(option).get().val()
                      li.append(val)
                      db.child(id).child(end_point).child(option).set(li)
                    except Exception as e:
                        print(e)
                        li=[val]
                        db.child(id).child(end_point).child(option).set(li)
                  else:
                      db.child(id).child(end_point).child(0).set({key:val})
                  
            except Exception as e:
                print(e)
                if end_point =="weekt":
                    li=[val]
                    db.child(id).child(end_point).child(option).set(li)
                    #db.child(id).child(end_point).child(0).set({key:val,"w":option})
                else:
                    db.child(id).child(end_point).child(0).set({key:val})
 
class date_details():
  def __init__(self,string1,integer1,string2,integer2):
      self.seting1=string1
      self.integer2=integer2
      self.seting2=string2
      self.integer1=integer1
      
      
   



class Make_time_interval(date_details):
  def __init__(self,reference):
      self.reference=reference
  def forme_week(self):
      d=datetime(self.reference.year,self.reference.month,self.reference.day)
      wd= d.isoweekday()
      f=d-timedelta(days=-1+wd)
      t=d+timedelta(days=7-wd)
      
      self.seting1=f"{w_days[f.weekday()]},{f.day} {my_months[f.month]} {f.year}"
      self.seting2=f"{w_days[t.weekday()]},{t.day} {my_months[t.month]} {t.year}" 
      self.integer1=f
      self.integer2=t
      
      
      
      return self
    
  def forme_month(self):
      fst=self.reference-timedelta(days=self.reference.day-1)
      f=fst
      t=self.end_month()
      self.seting1=f"{w_days[f.weekday()]},{f.day} {my_months[f.month]} {f.year}"
      self.seting2=f"{w_days[t.weekday()]},{t.day} {my_months[t.month]} {t.year}" 
      self.integer1=f
      self.integer2=t
      return self
      
  def end_month(self):
      fst=self.reference-timedelta(days=self.reference.day-1)
      thirtyone=fst+timedelta(days=31-1)
      
      if thirtyone.month==fst.month:
          
          return thirtyone
      thirty=fst+timedelta(days=30-1)
     
      if thirty.month==fst.month:
         
         return thirty
      twentynine=fst+timedelta(days=29-1)
     
      if twentynine.month==fst.month:
          
          return twentynine
          
      else:  
          
          return fst+timedelta(days=28-1)
          
      
  def forme_year(self):
        firstday=datetim.datetime(self.reference.year,1,1,0,0,0,0)
        f=firstday
        up=firstday+timedelta(days=366)
        norm=firstday+timedelta(days=365)
        down=firstday+timedelta(days=364)
        t=""
        if up.year==firstday.year: 
          
          t=datetim.datetime(up.year,up.month,up.day,self.reference.hour,self.reference.minute,self.reference.second)
          """self.seting1=f"{w_days[f.weekday()]},{f.day,my_months[f.month]},{f.year}"
          self.seting2=f"{w_days[t.weekday()]},{t.day,my_months[t.month]},{t.year}" 
          self.integer1=f
          self.integer2=t
          return self"""
          
        elif norm.year==firstday.year:
            #f=firstday
            t=datetim.datetime(norm.year,norm.month,norm.day,self.reference.hour,self.reference.minute,self.reference.second)
            """self.seting1=f"{w_days[f.weekday()],f.day,my_months[f.month]}"
            self.seting2=f"{w_days[t.weekday()],t.day,my_months[t.month]}" 
            self.integer1=f
            self.integer2=t  
            return self"""
            
        
        elif down.year==firstday.year:
            #f=firstday
            t=datetim.datetime(down.year,down.month,down.day,self.reference.hour,self.reference.minute,self.reference.second)
            """self.seting1=f"{w_days[f.weekday()],f.day,my_months[f.month]}"
            self.seting2=f"{w_days[t.weekday()],t.day,my_months[t.month]}" 
            self.integer1=f
            self.integer2=t
            return self"""
            
        else:
            f=firstday
            t=datetim.datetime(norm.year,norm.month,norm.day,self.reference.hour,self.reference.minute,self.reference.second)
            """self.seting1=f"{w_days[f.weekday()],f.day,my_months[f.month]}"
            self.seting2=f"{w_days[t.weekday()],t.day,my_months[t.month]}" 
            self.integer1=f
            self.integer2=t"""
            
        self.seting1=f"{w_days[f.weekday()]},{f.day} {my_months[f.month]} {f.year}"
        self.seting2=f"{w_days[t.weekday()]},{t.day} {my_months[t.month]} {t.year}" 
        self.integer1=f
        self.integer2=t
        return self
    
  def formulate(self,f,t):
      
      self.seting1=f"{w_days[f.weekday()]},{f.day,my_months[f.month]},{f.year}"
      self.seting2=f"{w_days[t.weekday()]},{t.day,my_months[t.month]},{t.year}" 
      self.integer1=f
      self.integer2=t
        
        

 
        

def new_time(req):
    me=req.session.get('user')['mail'].split('.')[0]
    k=[]
    try:
      k=db.child(me).child('classes').get().val()
    except Exception as e:
        print("when get classes in new time:",e)
        k=[]
    d=datetim.datetime.now()
    #dt=d
    cw=find_week(f"{d.year}-{d.month}-{d.day}")
    lines=[]
    try:
      lines=db.child(me).child("weekt").child(cw).get().val()
    except Exception as e:
        
        lines=[]
    
    if req.method=="POST":
     try:
      verifix=req.POST["date2"] 
      if verifix is not None:
        
        date=verifix#req.POST['date']
        
        
        try:  
           date=datetime.strptime(date,'%Y-%m-%dT%H:%M')
           y=date.year
           m=date.month
           da=date.day
           fd=f"{y}-{m}-{da}"
           date=datetime.strptime(fd,'%Y-%m-%d')
           id=req.POST['id']
           id=int(id)
           ob= db.child(me).child('tasks').child(date).child(id).get().val()
        except Exception as e:
           print("Got an issue by UPDATE:",e)
               
        return render(req,'plan/update.html',context={"t":my_time,"d":ob,"l":lines,"k":k})
        
      else:
        
         previous_url = req.META.get('HTTP_REFERER', '/')
      
         return redirect(previous_url)
                
     except Exception as e:
      try:
        print("finalGot an issue by UPDATE:",e)
        
        dt =req.POST["date1"].split("T")[0]
        dt1=req.POST["date1"]
        d=datetime.strptime(str(dt),'%Y-%m-%d')
        cw=find_week(f"{d.year}-{d.month}-{d.day}")
        try:
          
          lines =select([db,me,"plan","weekt",cw],{},"get")    #db.child(me).child("weekt").child(cw).get().val()
        except:
          
            return render(req,'plan/add.html',context={"t":my_time,"k":k,"l":lines,"d":dt1})
      except:
          previous_url = req.META.get('HTTP_REFERER', '/')
      
          return redirect(previous_url)
    else:
        
        previous_url = req.META.get('HTTP_REFERER', '/')
      
        return redirect(previous_url)
   
   
def add(req):
 blocked=False
 try:
    me=req.session.get('user')['mail'].split('.')[0]
    
    k=[]
    try:
      k=select([db,me,"plan","classes"],{},"get") #db.child(me).child('classes').get().val()
    except Exception as e:
        k=[]
        print("when geting classes by add:",e)
        
    d=datetim.datetime.now()   
    #cw=find_week(f"{d.year}-{d.month}-{d.day}")
    md = ""
    fd=d
    if req.method=="POST":
       post=req.POST
       the_date=post["date"]
       the_date=datetime.strptime(the_date,'%Y-%m-%dT%H:%M')
       y=the_date.year
       m=the_date.month
       da=the_date.day
       fd=f"{y}-{m}-{da}"
       num=post["hid"]
       
       selected_date=datetime.strptime(fd,'%Y-%m-%d')#T%H:%M
       d=selected_date
       for i in range(1,int(num)+1):
           classi=post[f"typo{i}"]
           try:
             el = [c for c in k if c==classi]
             if len(el)<1 and len(k)>0:
                 k.append(classi)
             else:
                 k=[]
                 k.append(classi)
             ob={"classes":k}
             cl=select([db,me,"plan"],ob,"update")
               #db.child(me).child("classes").child(len(k)).set({'class':classi})
           except:
               pass
              #db.child(me).child("classes").child(0).set({'class':classi})
              
           fm=post[f"timF{i}"]
           to=post[f"timT{i}"]
           acti=post[f"act{i}"]
          
           
             
           nwtask=Task(date=selected_date,me=me,begin=str(fm),end=str(to),task=acti,classi=classi)
           nwtask1=nwtask.clean(alt="")
          
           if(len(nwtask1)<1):
               nwtask.save(alt="")  
        
           else:
               if nwtask1 is not None and len(nwtask1)>1 :
                 ar=nwtask.clean(alt="ok")
                
                 
                 nwtask.save(alt=ar)
               if blocked:
                   blocked=f"{blocked};{fm}-{to}"
               else:
                   blocked=f"{fm}-{to}"
           
           #nwtask.save()
 except Exception as e:# not req.user.is_authenticated:
        print("Final:",e)
        rev=reverse('add')
        return redirect(rev) 
 try:
     k=select([db,me,"plan","classes"],{},"get")
 except Exception as e:
     k=[]
     print("when geting classes by add at the end of add:",e)
 try:
     cw=find_week(f"{d.year}-{d.month}-{d.day}")
     li=select([db,me,"plan",'weekt',cw],{},"get")
     
 except Exception as e:
        print("I was blocked by an Errro when getting the week kines :",e)
        li=[]
 period=Make_time_interval(d).forme_week()
 return render(req,'plan/add.html',context={"t":my_time,"k":k,"d":md,"blocked":blocked,"l":li,"period":period})
    



def add_week(req):
    try:
        me=req.session.get('user')['mail'].split('.')[0]
    except:
        return redirect(reverse("login"))
    d=datetim.datetime.now()
    periodate=d
    d1=f"{d.year}-{d.month}-{d.day}"
    w=find_week(d1)
    if req.method=="POST":
        dt=req.POST["week"] #.split("T")[0]
        the_date=datetime.strptime(dt,'%Y-%m-%dT%H:%M')
        periodate=the_date
        y=the_date.year
        m=the_date.month
        da=the_date.day
        fd=f"{y}-{m}-{da}"
        d1=fd
        w=find_week(fd)
        
        #author=req.user
        l=req.POST["line"]
        if validate([w,l]):
           try:
             myweek= select([db,me,"plan",'weekt',w],{},"get") #db.child(me).child("weekt").child(w).get().val()
             if myweek is not None and len(myweek)>0:
               #id=len(myweek)
               myweek.append(l)
               #db.child(me).child("weekt").child(w).child(id).set({"name":l,"id":id})
             elif len(myweek)==0:
                 myweek=[]
                 myweek.append(l)
             ob={w:myweek}
             wk=select([db,me,"plan",'weekt'],ob,"update")
             
             
           except Exception as e:
               print("I wa getting Weekt but ",e)
               ob={w:[l]}
               wk=select([db,me,"plan",'weekt'],ob,"update")
               
               
    try:
      l=select([db,me,"plan",'weekt',w],{},"get")
    except:
        l=[]
   # d1=datetim.datetime.now()
    perio=Make_time_interval(periodate).forme_week()
    
    return render(req,'plan/weeklines.html',context={"t":my_time,"lines":l,"w":w,"d":d1,"period":perio})


def disprogram(req):
    try:
        me=req.session.get('user')['mail'].split('.')[0]
    except:
        return redirect(reverse("login"))
    ind=req.POST['l']
    w=ind.split(':')[0]
    w=int(w)
    
    
    l=ind.split(':')[1]
    
    lines=select([db,me,"plan","weekt",w],{},"get") #db.child(me).child("weekt").child(w).get()
    
    
    li=[x for x in lines if x !=l]
    select([db,me,"plan","weekt"],{w:li},"update")
        
    previous_url = req.META.get('HTTP_REFERER', '/')
    return redirect(previous_url)
    
def transit(req):
    
    return render(req,'plan/transit.html',context={"t":my_time})

def ordi(me,date):
    
   try:
        taff1 = db.child(me).child('tasks').child(date).get().val() #order_by_child('date').equal_to(t).get().val()
        
        taff0=[]
        if taff1 is not None:
         for i in taff1:
           if i is not None:
            taff0.append(str(i['begin']))
        taff0.sort()
       
        tas=[]
        for i in taff0:
         #if i is
          el = [x for x in taff1 if x is not None and x["begin"]==i][0]
          ob={}
          ob["begin"]=i #[:-3]
          ob["end"]=str(el['end'])#[:-3]
          ob["task"]=el['task']
          ob["classi"]=el['classi']
          ob["date"]=el['date'].split(' 00:00:00')[0]
          ob["id"]=el['id']
          tas.append(ob)
        
   except Exception as e:
          print("exception when get tasks in day:",e)
          tas=[]
   return tas

def days(req):
    tas=[]
    try:
        user1=req.session.get('user')['name']
        me=req.session.get('user')['mail'].split('.')[0]
        
    except Exception as e:
       print(e)
       return redirect(reverse("login")) 
    id=0
        #tasks=db.child(m).child("tasks").get().val()
    lc = get_localzone()
    tm=datetime.now(lc)
    y=tm.year
    m=tm.month
    da=tm.day
     
    fd=f"{y}-{m}-{da}"
    t=datetime.strptime(fd,'%Y-%m-%d') #'%Y-%m-%d'
    perid=Make_time_interval(tm).forme_week()
    if req.method=="POST":
            try:
             we=find_week(fd)
             li=db.child(me).child("weekt").child(we).get().val()
            except:
                li=[]
            el=req.POST['delete'].split(':')
            id=int(el[0])
            message=el[1]
            try:
                ob= db.child(me).child('tasks').child(t).child(id).get().val()
                
            except Exception as e:
                print("could not get object:",ob,"because of ",e)   
            if ob is not None and message=="D":
                
                return render(req,'plan/delete.html',context={"t":my_time,"d":ob})
            elif ob is not None:
                try:
                 cl=db.child(me).child("classes").get().val()
                except Exception as e:
                    print("could not get classes",cl,":",e)
                    cl=[]
                
                return render(req,'plan/update.html',context={"t":my_time,"d":ob,"l":li,"k":cl})
                
    tas=ordi(me=me,date=t)
        
    return render(req,'plan/today.html',context={"t":my_time,"taff":tas,"period":perid})
    

      
def week(req):
    me=req.session.get('user')['mail'].split('.')[0]
    today=datetim.datetime.now()
    current_Week=find_week(f"{today.year}-{today.month}-{today.day}")
    we=[]
    try:
       we=db.child(me).child('tasks').get().val()
    except Exception as e:
        print("Exception when trying to get we tasks:",e)
        we=[]
    #getting only plannings of the currentweek
    try:
      wee= [x for x in we if find_week(x.split(' 00:00:00')[0])== current_Week]  #[]
      
    except Exception as e:
        print("got problem when trying to filter", we , "-->"*9, e)
        wee=[]
    #getting planed dates of the week 
    wee.sort()
    w1=[ordi(me,x)for x in wee]
    w1.reverse()
    period=Make_time_interval(today).forme_week()
   
    return render(req,'plan/week.html',context={"t":my_time,"week":w1,"period":period})



def months(req):
 try:
   me=req.session.get('user')['mail'].split('.')[0]
 except Exception as e:
     print("Exception in month when geting user:",e)
     rev=reverse('login')
     return redirect(rev)
 mo=datetim.datetime.now().month
 yea=datetim.datetime.now().year
 fmo=db.child(me).child('tasks').get().val()
 #verify if an othen than current month was chosen
 md=datetime.now()
 try:
    month_info=req.GET["msel"]
    msel=int(month_info.split(":")[0])
    syea=int(month_info.split(":")[1])
    
    if not msel==mo:
     mo=msel
     yea=syea
     
 except:
        pass
        
 moar=[]
    #prepare the months list for a select tag
 allmonths=[]
 selected_month={"val":f"{mo}:{yea}","name":f"{my_months[mo]} {yea}"}
 if fmo is not None: 
  for el in fmo:
          date=datetime.strptime(el.split(' 00:00:00')[0],'%Y-%m-%d')
          ob={"val":f"{date.month}:{date.year}","name":f"{my_months[date.month]} {date.year}"}
          md=date
          if not ob in allmonths:
              if not date.month==mo or not date.year==yea:
                allmonths.append(ob)       
          if date.month == mo  and date.year==yea and not el in moar:
             moar.append(el)
    
 m1=[ordi(me,x)for x in moar]
 m1.reverse()
 period=Make_time_interval(md).forme_month()        
 return render(req,'plan/month.html',context={"t":my_time,"mo":m1,"sel":selected_month,"mo1":allmonths,"period":period})


def types(req):
    
    try:
       m=req.session.get('user')['mail'].split('.')[0]
       if m is None:
        rev=reverse('login')
        return redirect(rev)
    except:
        rev=reverse('login')
        return redirect(rev)
    message=""
    if req.method=="POST":
     
     classi=req.POST["typo"]
  
     try:
        c=select([db,m,"plan","classes"],{},"get") 
        if c is not None and len(c)>0:
            if not classi in c:
              c.append(classi)
        else:
            c=[]  
            
            c.append(classi)
        
        ob={"classes":c}
        cl=select([db,m,"plan"],ob,"update")
        message=f"{classi} added "
         
     except:  
        
       c=[]
       c.append(classi)
       ob={"classes":c}
       cl=select([db,m,"plan"],ob,"update")
       message=f"{classi} added "
       
          
    return render(req,'plan/types.html',context={"t":my_time,"m":message})

def give_to_update_object(req):
    
  try:
    me=req.session.get('user')['mail'].split('.')[0]
  except Exception as e:
      print("Who are you ?", e)
  date=req.POST['date']
  date=datetime.strptime(date,'%Y-%m-%dT%H:%M')
  y=date.year
  m=date.month
  da=date.day
  fd=f"{y}-{m}-{da}"
  
  date=datetime.strptime(fd,'%Y-%m-%d')
  
  
  id=req.POST['id']
  #ob=db.child(me).child('tasks').child(date).child(id)
  a=[f"begin,{req.POST['begin']}",f"end,{req.POST['end']}",f"task,{req.POST['task']}",f"classi,{req.POST['classi']}"]
  
  
  for x in a:
    if x.split(',')[1]is not None:
      db.child(me).child('tasks').child(date).child(id).child(x.split(',')[0]).set(x.split(',')[1])
      
     
      
  previous_url = req.META.get('HTTP_REFERER', '/')
      
  return redirect(previous_url)
 
   
def remov(req):
  try:
    me=req.session.get('user')['mail'].split('.')[0]
  except Exception as e:
      print("Who are you ?", e)
  date=req.GET['date']
  id=req.GET['id']
 
  ob=Task(me=me,date=date,begin='', end='', task='',classi= '')
  ob.delet_task(id=id)
 
  previous_url = req.META.get('HTTP_REFERER', '/')
  return redirect(previous_url)



