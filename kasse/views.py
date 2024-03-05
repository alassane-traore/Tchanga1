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
#from .models import Sector,Basket,Goods
#import pygame
import os
from Tchanga1.settings import firebase


db=firebase.database()

my_months=["", "Jan", "Feb","Mar","Apr", "May", "June", "July","Aug","Sept","Oct","Nov","Dec"]

def get_user(key,message,users):
    user=False
    try:
     for u in users:
        
        if u[f"{key}"]==message:
          user=u
          return user
    except Exception as e:
        #print("THIS IS THE EX:", e)
        pass
    return user

def form_clien_date(x):
      dtim =x.split("TIME")[1].split(":")[0]
      y=dtim.split("-")[0]
      y=int(y)
      mon=dtim.split("-")[1]
      mon=int(mon)+1
      d=dtim.split("-")[2]
      d=int(d)
      h=x.split("TIME")[1].split(":")[1]
      h=int(h)
      min=x.split("TIME")[1].split(":")[2]
      min=int(min)
      sec=x.split("TIME")[1].split(":")[3]
      sec=int(sec)
      nd=datetime.datetime(year=y,month=mon,day=d,hour=h,minute=min,second=sec)
      return nd

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

def select(root,data,message):   
  """ This function gets firebase realtime date in the using information given in  root argument. If no data was found , it retuns the typ ardument"""
  try:
    if isinstance(root,list):
      r=root[0]
      root=[x for x in root if x !=root[0]]
      #bild the root
      for el in root:
         r=r.child(el) 
      if message=="get":
       
       s=r.get().val()
       
       return s
      elif message=="set":
        r.set(data)
        ms=f"{root[-1]} sucessfully added to your {root[-2]}"
        return ms
      elif message=="update":
        r.update(data)
        ms=f"{root[-1]} updated seccessfully !"
        return ms
      elif message=="rm":
        r.remove()
        ms=f"{root[-1]} removed seccessfully !"
        return ms
    else:
       ms=f"{root} is supposed to be a list, not {type(root)} !"
       return f"An error occured{ms}"
       
  except Exception as e:
       s=data
    
       ms=f"Got an obtacle when try to {message} {root[-1]} {e}"
       return ms
 
 
def validate(x):
  try:
   if isinstance(x,list):
     a=[i for i in x if i is None or i==""] 
     return len(a)==0 and len(x)>0   
   else:
    return x is not None and x !=""  
  except :
    return False


def design(x,y):
  if y*100/x>=50 and y*100/x <75 :
    return "orange"
  elif y*100/x>=75 and y*100/x <100:
    return "orangered"
  elif y*100/x>=100 or x<=0:
    
    return "red"
  else:
    return "normal"
  
  
def new_sector(req):
    mg=""
    signaler="new sector"
    maga=False
  #verify that user is authenticated
    try :
     me=req.session.get('user')['mail'].split('.')[0]
     maga=select([db,me,"name"],{},"get")
    except:
      return redirect(reverse("login"))
  #verify if their allready sector existing
    message=""       
    if req.method =="POST" : 
      try:
        if validate([req.POST["begin"],req.POST["end"],req.POST["sector"],eval(req.POST["budget"])]):
          post=req.POST
          begin = post["begin"]
          end = post["end"]
          sector=post["sector"]
          budget= eval(post["budget"])
          auto=True
       #update auto accordingly
          try:
            if post["yes"]:
              auto=True
            else:
              auto=False
          except :
            auto=False
    #prevent empty submition
     
      #format begin date
          date1=datetime.strptime(begin,'%Y-%m-%dT%H:%M')
          y=date1.year
          m=date1.month
          da=date1.day
          fd=f"{y}-{m}-{da}"
          f=datetime.strptime(fd,'%Y-%m-%d')
          f=str(f)
       #format end date
          date2=datetime.strptime(end,'%Y-%m-%dT%H:%M')
          y2=date2.year
          m2=date2.month
          da2=date2.day
          fd2=f"{y2}-{m2}-{da2}"
          t=datetime.strptime(fd2,'%Y-%m-%d')
          t=str(t)
          ob ={'begin':f,"fbegin":f,'end':t,'budget':budget,'newbudget':budget,'counter':0,'newcounter':0,'automate':auto}    
       #db.child(me).child('kasse').child('sectors').child(id).set(ob) 
          s={sector:ob}
       #select([db,me,"kasse",'sectors',id],ob,"set")
          try:
            sec = select([db,me,"kasse",'sectors',sector],ob,"get")  #db.child(me).child('kasse').child('sectors').get().val()
            if sec is not None :
              message=f"{sector} already exists ! You can only update it !"
            else:
               message=select([db,me,"kasse",'sectors'],s,"update")
          except Exception as e:
             #print("Confronted with following error when trying to get sectors, sector is ", s, "problem is ",e )
             pass
      except:
        previous_url = req.META.get('HTTP_REFERER', '/')
        return redirect(previous_url)
    return render(req,"kasse/sectors.html",context={"m":message,"ident":mg,"signaler":signaler,"maga":maga})


def add_list(req):
  mg=""
  signaler="add list"
  maga=False
  #verify that user is authenticated
  try :
     me=req.session.get('user')['mail'].split('.')[0]
     maga=select([db,me,"name"],{},"get")
  except:
      return redirect(reverse("login"))
  
  message=""  
  nw = datetim.datetime.now()
  s=select([db,me,"kasse","sectors"],{},"get")
  
  gs=[]
  
  leng=0  
      
  cs=[]
  nw1=datetime.strptime(f"{nw.year}-{nw.month}-{nw.day}",'%Y-%m-%d')
  for o in s:
       name=o
       o=select([db,me,'kasse','sectors',name],{},"get")
       nb=o["begin"].split(' 00:00:00')[0]
       nb=datetime.strptime(nb,'%Y-%m-%d') 
       nt=o["end"].split(' 00:00:00')[0]
       nt=datetime.strptime(nt,'%Y-%m-%d')
       
       if nb<=nw1 and nt>=nw1:
           o['name']=name
           try:
             o["list"]=[x for x in o["list"] if x is not None]
             o["len"]=len(o["list"])
             
           except:
             o["list"]=[]
             o["len"]=0
           leng+=len(o["list"])
           cs.append(o)
           
       elif nt<nw1 and o["automate"]:
           period=nt-nb 
           period=period.days
           nb=create_date(1,nt)
           nt=create_date(period,nb)
           rest = o["newbudget"]-o["newcounter"]
           o["newbudget"]=o["budget"]+rest
           o["newcounter"]=0
           o["begin"]=str(nb)
           o["end"]=str(nt)
           fresh={name:o}
           select([db,me,"kasse","sectors"],fresh,"update")
           o['end']=str(nt).split(' 00:00:00')[0]
           o['name']=name
           try:
            o["list"]=[x for x in o["list"] if x is not None]
            o["len"]=len(o["list"])
           except Exception as e:
             o["list"]=[]
             o["len"]=0
            # print(e)
           leng+=len(o["list"])
           cs.append(o)
        
  if req.method=="POST":
    post=req.POST
    #dat=post["date"]
    n=post["good"]
    sec=post["sector"]
    s=select([db,me,"kasse","sectors",sec],{},"get")
    
    try:
      li=s["list"]
      if li is None:
        li=[]
    except:
      li=[]
    if validate([n,sec]):
     li.append(n)
     ob={"list":li}
     s=select([db,me,"kasse","sectors",sec],ob,"update")  #Sector.objects.get(id=)
     
    return redirect("addlist")
  
  return render(req,"kasse/addliste.html",context={"li":gs,"cs":cs,"len":leng,"ident":mg,"signaler":signaler,"maga":maga})


def shopping_list(req):
    mg=""
    signaler="shopping list"
    
    return render(req, "kasse/kaufliste.html",context={"ident":mg,"signaler":signaler})

            
def markets(req):
   mg=""
   signaler="markets"
   maga=False
   #make sure user is athenticated
   try :
    me=req.session.get('user')['mail'].split('.')[0]
    maga=select([db,me,"name"],{},"get")
   except:
     try:
        mg=req.GET['letter']
        mg1=mg
        if "TIME" in mg:
          mg1=mg.split("TIME")[0]
        if mg1 and mg1 is not None and mg1 !=" ":
          users=select([db,'users'],{},'get')
          me= get_user(key="message",message=mg1,users=users)['mail'].split(".")[0]
          maga=select([db,me,"name"],{},"get")
        signaler=""
        if me is None:
           return redirect(reverse("login"))
        
     except Exception as e:
         me=""
         maga=False
         signaler=""
    #return redirect(reverse("login"))
   #prepare to redirect to the busket by click
   if req.method=="POST":
     
     sector=req.POST["id"]
     s=select([db,me,"kasse",'sectors',sector],{},"get")
     try:
      
      s["rest"]="{:.2f}".format(s["newbudget"]-s["newcounter"])
      
      s['name']=sector
      try:
         
         s["list"]=[x for x in s["list"] if x is not None]
         s["len"]=len(s["list"])
         s["decor"]=design(s["newbudget"],s["newcounter"])
      except Exception as e:
         s["list"]=[]
         s["len"]=0
         s["decor"]=design(s["newbudget"],s["newcounter"])
        # print("this is an exception",e)
      
      
     except Exception as e:
      # print("GOT AN EXCEPTION in marks", e)
      pass
       
     
     return render(req,"kasse/basket.html",context={"sc":s,"ident":mg,"signaler":signaler,"maga":maga})
   
   #present current available sector on the marketplace and renew them if automate is True 
   nw = datetim.datetime.now()
   s= select([db,me,'kasse','sectors'],{},"get")
   cs=[]
   if s is not None:
     nw=datetime.strptime(f"{nw.year}-{nw.month}-{nw.day}",'%Y-%m-%d') 
     for o in s:
       name=o
       o=select([db,me,'kasse','sectors',name],{},"get")
       nb=o["begin"].split(' 00:00:00')[0]
       nb=datetime.strptime(nb,'%Y-%m-%d') #datetim.datetime(o.year,o.begin.month,o.begin.day,o.begin.hour,59)
       nt=o["end"].split(' 00:00:00')[0]
       nt=datetime.strptime(nt,'%Y-%m-%d') 
       # only sectors uptodate
       
       if nb<=nw and nt>=nw:
           o["decor"]=design(o["newbudget"],o["newcounter"])
           o["rest"]="{:.2f}".format(o["newbudget"]-o["newcounter"])
           o["newbudget"]="{:.2f}".format(o["newbudget"])
           o['name']=name
           o['end']=str(nt).split(' 00:00:00')[0]
           
           cs.append(o)
       elif nt<nw and o["automate"]:
           #give the sector a new validity automatically
           
           period=nt-nb #o["end"]-o["begin"]
           period=period.days
           nb=create_date(1,nt)
           nt=create_date(period,nb)
           rest = o["newbudget"]-o["newcounter"]
           o["newbudget"]=o["budget"]+rest
           o["newcounter"]=0
           o["begin"]=str(nb)
           o["end"]=str(nt)
           fresh={name:o}
           select([db,me,"kasse","sectors"],fresh,"update")
           o['end']=str(nt).split(' 00:00:00')[0]
           o['name']=name
           o["decor"]=design(o["newbudget"],o["newcounter"])
           #db.child(me).child('kasse').child('sectors').child(o.id).update(o)
           cs.append(o)
           
   return render(req,"kasse/market.html",context={"sector":cs,"ident":mg,"signaler":signaler,"maga":maga})


def basket(req):
    mg=""
    signaler="basket"
    maga=False
   #ensure that user is authenticated
    try :
     me=req.session.get('user')['mail'].split('.')[0]
     maga=select([db,me,"name"],{},"get")
    except:
      try:
        mg=req.GET['letter']
        mg1=mg
        if "TIME" in mg:
          mg1=mg.split("TIME")[0]
        if mg1 and mg1 is not None and mg1 !=" ":
          users=select([db,'users'],{},'get')
          me= get_user(key="message",message=mg1,users=users)['mail'].split(".")[0]
          maga=select([db,me,"name"],{},"get")
        signaler=""
        if me is None:
           return redirect(reverse("login"))
        
      except Exception as e:
         me=""
         maga=False
         signaler=""
     #return redirect(reverse("login"))
   #handle post request in shop
    if req.method=="POST":
     try:
      post=req.POST
      nw = datetim.datetime.now()
      sid=post["id"]
      s=select([db,me,"kasse","sectors",sid],{},"get")
      
      comment =post["comment"]
      prise =post["prise"]
      
      goodn=post["goodnum"]
      goodn=int(goodn)
      
      liste=[]
      #build busket and removed bought goods from shoping list
      for i in range(goodn+1):
        try:
          good=post[f"good{i}"]
          g=select([db,me,"kasse","sectors",sid,"list"],'',"get")  
          
          if g is not None and good in g:
             liste.append(good)
             g.remove(good)
             rm=select([db,me,"kasse","sectors",sid],{"list":g},"update") 
             
          
            
        except Exception as e:
           g=select([db,me,"kasse","sectors",sid,"list"],'',"get")
          # print( "Exception occured when geting list element which is ",g, "Here is the Error: ",e)
           
      #Prevent empty submition
      if validate([prise,eval(prise)]) : 
       bk={"date":str(nw),"goods":liste,"costs":eval(prise),"comment":comment}
      #counter=select([db,me,"kasse","sectors",sid],'',"update")
       #ob={:bk}
       
       try:
         b=select([db,me,"kasse","sectors",sid,"buskets"],{},"get")  
         if b is not None:
           b.append(bk)
         else:
           b=[]
           b.append(bk)
       except Exception as e:
          # print("Got an exeption in Buskets ",e)
           b=[]
           b.append(bk)
           
       busket=select([db,me,"kasse","sectors",sid],{"buskets":b},"update")  
       
        
       s=select([db,me,"kasse","sectors",sid],{},"get")
       s["counter"]=s["counter"]+eval(prise)
       s["newcounter"]=s["newcounter"]+eval(prise)
       s={sid:s}
       counter=select([db,me,"kasse","sectors"],s,"update")
       
      
       return HttpResponseRedirect(reverse("market"))
     except Exception as e:
       # print("final exception in busket", e)
        previous_url = req.META.get('HTTP_REFERER', '/')
        return redirect(previous_url)
    return render(req,"kasse/basket.html",context={"ident":mg,"signaler":signaler,"maga":maga})


def transit1(req):
    mg=""
    signaler="transit"
    return render(req,'kasse/transit.html',context={"ident":mg,"signaler":signaler})
      

def count(req):
    mg=""
    signaler="count"
    maga=False
    try :
     me=req.session.get('user')['mail'].split('.')[0]
     maga=select([db,me,"name"],{},"get")
    except:
      try:
        mg=req.GET['letter']
        mg1=mg
        if "TIME" in mg:
          mg1=mg.split("TIME")[0]
        if mg1 and mg1 is not None and mg1 !=" ":
          users=select([db,'users'],{},'get')
          me= get_user(key="message",message=mg1,users=users)['mail'].split(".")[0]
          maga=select([db,me,"name"],{},"get")
        signaler=""
        if me is None:
           return redirect(reverse("login"))
        
      except Exception as e:
         me=""
         maga=False
         signaler=""
     
    sector=select([db,me,"kasse","sectors"],{},"get")
    bt=[]
    totalcosts=0
    sec=[]
    ntotal=0
    totalbudget=0
    secdates=[]#to receive the date of the sectors wich i will sort to find the first
    if sector is not None:
     for s in sector:
      
      name=s
      s=select([db,me,"kasse","sectors",name],{},"get")
      secdates.append(s['fbegin'])
      ntotal+=s["newcounter"]
      totalcosts+=s["counter"]
      totalbudget+=s["newbudget"]
      s["name"]=name
      s["newcounter"]= "{:.2f}".format(s["newcounter"])
      s["counter"]= "{:.2f}".format(s["counter"])
      f=datetime.strptime(s["begin"].split(' 00:00:00')[0],'%Y-%m-%d')
      t=datetime.strptime(s["end"].split(' 00:00:00')[0],'%Y-%m-%d')
      
      s["m"]=my_months[f.month]
      if f.month !=t.month:
        s["m"]=f"{my_months[f.month]}-{my_months[t.month]}"
      
      try:
       bk=s["buskets"]
       s["len"]=len(bk)
       
      except Exception as e:
       # print("Exception revailed in count :", e)
        s["len"]=1
      sec.append(s)
    totalcosts= "{:.2f}".format(totalcosts)  
    ntotal= "{:.2f}".format(ntotal)
    totalbudget= "{:.2f}".format(totalbudget)
    secdates.sort()
    try:
     first=datetime.strptime(secdates[0].split(" ")[0],'%Y-%m-%d')
     interv=f"from {first.day} {my_months[first.month]} {first.year}"
     sec[0]['interv']=interv
    
     if first.month<datetime.now().month:
        sec[0]['interv']=f"{interv}--{datetime.now().day} {my_months[datetime.now().month]} {datetime.now().year}"
    except:
      pass
    return render(req,"kasse/counter.html",context={"sector":sec,"b":bt,"total":totalcosts,"nt":ntotal,"bud":totalbudget,"ident":mg,"signaler":signaler,"maga":maga})
      
       
def hist(req):
    
    return render(req,"kasse/history.html")

def removit(req,id):
    maga=False
    try :
     me=req.session.get('user')['mail'].split('.')[0]
     maga=select([db,me,"name"],{},"get")
    except:
      return redirect(reverse("login"))
    
    sector=id.split(";")[0]
    good=id.split(";")[1]
    li=select([db,me,"kasse","sectors",sector,"list"],{},"get")
    li=[x for x in li if x !=good]
    select([db,me,"kasse","sectors",sector],{"list":li},"update")

    return redirect("addlist")
  

def update_sector(req):
  signaler="update_sec"
  me=""
  m=""
  maga=False
  try :
     me=req.session.get('user')['mail'].split('.')[0]
     maga=select([db,me,"name"],{},"get")
  except:
      return redirect(reverse("login"))
  try:
   id=req.GET['id']
  except:
    id=""
  sec=select([db,me,"kasse","sectors",id],{},"get")
  sec["name"]=id
  busk=False
  try:
    busk=sec['buskets']
  except:
    pass
  if busk:
    sec['new']=False
  else:
   sec['new']=True
   
  if req.method =="POST":
    post=req.POST
    try:
      begin=post['begin']
    except:
      begin=False
    
    auto=post['auto']
    auto=eval(auto)
    name=post['sector']
    budget=post['budget']
    budget=eval(budget)
    end=post['end']
    sector=select([db,me,"kasse","sectors",name],{},"get")
    sector['automate']=auto
    initial_budget= sector['budget']
    sector['budget']=budget
    #newbudget=sector['newbudget']
    
    if begin:
      begin=datetime.strptime(begin,'%Y-%m-%dT%H:%M')
      bg=f"{begin.year}-{begin.month}-{begin.day}"
      begin=datetime.strptime(bg,'%Y-%m-%d')
      begin=str(begin)
      sector['begin']=begin
      sector['newbudget']=budget
    else:
      sector['newbudget']=sector['newbudget']-initial_budget+budget
      
    end=datetime.strptime(end,'%Y-%m-%dT%H:%M')
    nd=f"{end.year}-{end.month}-{end.day}"
    end=datetime.strptime(nd,'%Y-%m-%d')
    end=str(end)
    sector['end']=end
    m=select([db,me,"kasse","sectors"],{name:sector},"update")
    
    return redirect(reverse('market'))
    
  return render(req,'kasse/update.html',context={'s':sec,"signaler":signaler,"m":m,"maga":maga})


def update_busket(req):
  signaler="update_sec"
  me=""
  m=""
  maga=False
  try :
     me=req.session.get('user')['mail'].split('.')[0]
     maga=select([db,me,"name"],{},"get")
  except:
      return redirect(reverse("login"))
  if req.method=="GET":
   try:
    id=req.GET['sector']
    busket_date=req.GET['busket']
   
   except:
     id=""
     busket_date=""
    
   sec=select([db,me,"kasse","sectors",id],{},"get")
   sec['name']=id
   bk=get_user(key="date",message=busket_date,users=sec['buskets'])

  if req.method=="POST":
    post=req.POST
    costs=post['costs']
    costs=eval(costs)
    goods=post['good']
    ngoods=post['ngood']
    if "41259" in goods:
      goods=goods.split("41259")
    else:
      goods=False
    if "41259" in ngoods:
      ngoods=ngoods.split("41259")
    else:
      ngoods=False
      
    sector=post['sector']
    bk=post['busket']
    sec=select([db,me,"kasse","sectors",sector],{},"get")
    counter=sec['counter']
    newcounter=sec['newcounter']
    newbudget=sec['newbudget']
    begin=sec['begin']
    begin=begin.split(' ')[0]
    begin=datetime.strptime(begin,'%Y-%m-%d')
    
    end=sec['end']
    end=end.split(' ')[0]
    end=datetime.strptime(end,'%Y-%m-%d')
    
    bk=get_user(key="date",message=bk,users=sec['buskets'])
    busket_date=bk['date']
    busket_date=busket_date.split(' ')[0]
    busket_date=datetime.strptime(busket_date,'%Y-%m-%d')
    
    initial_cost=bk['costs']
    
    try:
     initial_goods=bk['goods']
     
    except:
      initial_goods=[]
    
    try:
     initial_list=sec['list']
    except:
      initial_list=[]
      
    new_goods=[]
    new_list=[]
    if goods:
      goods=[x for x in goods if x is not None and x !="" and x !=" "]
    else:
      
      goods=[]
      
    l=[x for x in initial_goods if x not in goods and x is not None and x !="" and x !=" "]
    new_list.extend(l)
    new_goods.extend(goods)
    
    if ngoods:
      ngoods=[x for x in ngoods if x is not None and x !="" and x !=" "]
    else:
      ngoods=[]
      
    l=[x for x in initial_list if not x in ngoods and x is not None]
    new_list.extend(l)
    new_goods.extend(ngoods)
    if len(new_goods)<1:
      costs=0 
      
    sec['list']=new_list
    bk['goods']=new_goods
    bk['costs']=costs
    allbk=sec['buskets'] 
    
    if begin<=busket_date and busket_date<=end:
     newcounter=newcounter-initial_cost+costs
     sec['newcounter']=newcounter
     
    else:
      newbudget=newbudget+initial_cost-costs
      sec['newbudget']=newbudget 
    counter=counter-initial_cost+costs
    sec['counter']=counter
    
    for b in allbk:
      if b['date']==bk['date']:
        if len(new_goods)<1 and len(initial_goods)>0:
          allbk.remove(bk)
        
       
    sec['buskets']=allbk
    
    sc=select([db,me,"kasse","sectors"],{sector:sec},"update")
    return redirect(reverse('counter'))
  return render(req,'kasse/updatebusket.html',context={'s':sec,'b':bk,"signaler":signaler,"m":m,"maga":maga})


def delete_busket(req):
  signaler="update_sec"
  me=""
  m=""
  maga=False
  try :
     me=req.session.get('user')['mail'].split('.')[0]
     maga=select([db,me,"name"],{},"get")
  except:
      return redirect(reverse("login"))
  if req.method=="GET":
   try:
    id=req.GET['sector']
    busket_date=req.GET['busket']
   except:
    id=""
    busket_date=""
    
   sec=select([db,me,"kasse","sectors",id],{},"get")
   sec['name']=id
  
   bk=get_user(key="date",message=busket_date,users=sec['buskets'])
  
  if req.method =="POST":
   try:
    post=req.POST
    sector=post['sector']
    date=post['date']
    sec=select([db,me,"kasse","sectors",sector],{},"get")
    bk=get_user(key="date",message=date,users=sec['buskets'])
    sec['name']=sector
    costs=bk['costs']
    goods=False
    try:
      goods=bk['goods']
    except:
      pass
    li=False
    try:
      li=sec['list']
    except:
      li=False
      
    if goods:
      l=[x for x in goods if x is not None and x and x !=" "]
      if li:
        sec['list'].extend(l)
      else:
        sec['list']=l
       
    sec['buskets'].remove(bk)
    counter=sec['counter']
    newcounter=sec['newcounter']
    newbudget=sec['newbudget']
    begin=sec['begin']
    begin=begin.split(' ')[0]
    begin=datetime.strptime(begin,'%Y-%m-%d')
    
    end=sec['end']
    end=end.split(' ')[0]
    end=datetime.strptime(end,'%Y-%m-%d')
    
    date=date.split(' ')[0]
    date=datetime.strptime(date,'%Y-%m-%d')
    if begin<=date and date<=end:
     newcounter=newcounter-costs
     sec['newcounter']=newcounter
     
    else:
      newbudget=newbudget+costs
      sec['newbudget']=newbudget 
    counter=counter-costs
    sec['counter']=counter
    sc=select([db,me,"kasse","sectors"],{sector:sec},"update")
    
    return redirect(reverse('counter'))
   except:
     pass
  
  return render(req,'kasse/deletebusket.html',context={'s':sec,'b':bk,"signaler":signaler,"m":m,"maga":maga})


 
