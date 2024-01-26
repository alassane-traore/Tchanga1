"""from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _ 
from datetime import datetime

# Create your models here.

class Kategories(models.Model):
    author = models.CharField(max_length=85)
    kategorie=models.CharField(max_length=25)
   
    def __str__(self) -> str:
        return f"{self.kategorie}"
    
    
class weecklines(models.Model):
    author = models.CharField(max_length=85)
    week=models.IntegerField()
    line=models.CharField(max_length=89)
   
    def __str__(self) -> str:
        return f"W({self.week}):{self.line}"
        """
 
from users.views import db 
  
def filter_list(li,cond):
    l=li
    print('filt:',li)
    for i in cond:
        for j in l:
            if j ==i:
                print("i:",i,"j:",j)
                l.remove(i)
                #return l
    return l

def makeborder(old,new,opt): 
    if opt :
      last=[]
      for x in new:
        
        if x  in old :
          print(x ,"is  in ",old ) 
          last.append(new.index(x))
          return new.index(x)
      if len(last)<1:
          
          return ""
    else:
        last=[]
        for x in new:
          if x not  in old :
            last.append(new.index(x))
            print(x ,"is not in ",old ) 
          #else:  
            #return last[0]
        print(">"*9,last)
        if len(last)<1:
            last=[""]
            
        return last[0]        
  
def prevent_ovolapp(borders,i,a):
    if not "" in borders :
      if borders[0]<borders[1]:
         print("b0<b1")
      
         borders[0]=borders[1]
         nl=[x for x in i if i.index(x)>borders[0]]
         print("nl=",nl)
         end1=makeborder(a,nl,True)
         end=borders[1]
         if type(end1) is not int():
           print("typof end1:",type(end1))
           end1=len(i)-1
           end=len(i)
         else:
           end= i.index(nl[end1])
         
         borders[1]= end-1 #len(i)-1
      elif borders[0]>0:
       borders[0]=borders[0]-1
       print(borders[0],">",0)
      
      borders.sort()
      b=[i[borders[0]],i[borders[1]]]
      print("lena",b)
      if b[0]==b[1]:
          b=[]
      return b
    else: 
      print(a, "and",i, "are totaly overlapping")
      return[]
       
         
class watch():
 def __init__(self,frm1,to1):
    self.frm=frm1
    self.to=to1
    self.ar=[]
  
 def new_hours(self,f,t):
    self.f=f
    self.t=t
    ar=self.ar
    #global ar
    #prevent beging to be after end 
    go=True
    
    if go:
      for i in range(60):
        frm=self.f
        to=self.t
        if i<10:
            i=f"0{i}"
        nh=f"{frm.split(':')[0]}:{i}"
        print(nh)
        self.ar.append(nh)
        if nh==to:
            print("return first:")
            return self.ar
        elif i==59:
            print("h:",int(frm.split(':')[0]))
            if int(frm.split(':')[0])<23:
                
              h=int(frm.split(':')[0])+1
              if h<10:
                  h=f"0{h}"
              nh=f"{h}:{i}"
              #ar.append(nh)
              self.new_hours(nh,to)
              
            else:
                h="00"+":"+"00"
                self.new_hours(h,to)
        #else:
            #ar.append(nh)
    else:
        self.ar=[]
        
    print('last returning:',self.ar)
    return self.ar
 def filter(self,ar):
      self.ar=ar
      no=[x for x in self.ar if x.split(':')[0]==self.frm.split(':')[0] and int(x.split(':')[1])<int(self.frm.split(':')[1])]
      
      self.ar = [x for x in self.ar if x not in no]
      print("filted:",self.ar)
      return self.ar
    
     
class Task():
  """ Save tasks """
  def __init__(self,me,date,begin,end,task,classi):
    self.date =date
    self.begin= begin
    self.end=end
    self.task=task
    self.classi= classi
    self.me=me
    
   #Verify that  the current planing is not overlapping the allready existing planings 
  def clean(self,alt):
        self.ar=[]
        self.alt=alt
        tk=[]
        #get the existing planing
        try:
          tk=db.child(self.me).child('tasks').child(self.date).get().val()
        except:
            tk=[]
        #an  Array of the ongoing planing     
        f=str(self.begin)
        t=str(self.end)
        ar=watch(f,t).filter(watch(f,t).new_hours(f,t))
        print("not cleaned list:",ar)
        print("not cleaned list2:",tk)
        #make a list of the already planed 
        
        if tk  and len(tk)>0:
            tk0=[]
            for ob in tk:
                l=watch(ob['begin'],ob['end']).filter(watch(ob['begin'],ob['end']).new_hours(ob['begin'],ob['end']))   #watch(ob['begin'],ob['end']).new_hours(ob['begin'],ob['end'])
                tk0.extend(l)
            tk=tk0
            
            
        #proceed the filtering
        ar1=[]
        try:
          ar1=[x for x in ar if x  in tk]
          if len(ar1)>0:
            borders=[makeborder(tk,ar,True),makeborder(tk,ar,False)]
            self.ar=prevent_ovolapp(borders=borders,i=ar,a=tk)
          else:  
              self.ar=[] #x for x in ar if x not in tk
              
        except:
          if ar1 is None or tk is None:
             ar1=[]
        print("cleaned list:",ar1)
        if alt =="":
           print("<"*19)
           return ar1
        else:
            return self.ar
    
       #Save the cleaned date      
  def save(self,alt):
        self.alt=alt
        id=0
        
        print("mycleaner:",self.alt)
        
        ob=[f"begin,{self.begin}",
            f"end,{self.end}",
            f"task,{self.task}",
            f"classi,{self.classi}",
            f"date,{self.date}"]
        if self.alt !="" and len(self.alt)>1:
            b=self.alt[0]
            en=self.alt[-1]
            print("using special object"*5)
            print("FROM:",b,"TO:",en)
            ob=["begin," +b ,
            "end," + en,
            f"task,{self.task}",
            f"classi,{self.classi}",
            f"date,{self.date}"]
        try:
          tk=db.child(self.me).child('tasks').child(self.date).get().val()
          
          if tk is not None and len(tk)>0:
              id=len(tk)
              ob.append(f"id,{id}")
              for a in ob:
               at=a.split(',')[0]
               v=a.split(',')[1]
               db.child(self.me).child('tasks').child(self.date).child(id).child(at).set(v)
              #db.child(self.me).child('tasks').child(self.date).child(id).set(ob)
          else:
              ob.append(f"id,{id}")
              for a in ob:
               at=a.split(',')[0]
               v=a.split(',')[1]
               db.child(self.me).child('tasks').child(self.date).child(id).child(at).set(v)
             # db.child(self.me).child('tasks').child(self.date).child(id).set(ob)
              
        except Exception as e:
            
            ob.append(f"id,{id}")
            for a in ob:
                at=a.split(',')[0]
                v=a.split(',')[1]
                db.child(self.me).child('tasks').child(self.date).child(id).child(at).set(v)
            print(e)
   
  def delet_task(self,id): 
      self.id=id
      try:
        tk=db.child(self.me).child('tasks').child(self.date).child(self.id).get().val()
        if tk is not None:
            db.child(self.me).child('tasks').child(self.date).child(self.id).remove()
        
      except:
           print("could not see:", tk)
           
           pass
  def delet_date(self,d): 
      self.d=d
      try:
        tk=db.child(self.me).child('tasks').child(self.d).get().val()
        if tk is not None:
            db.child(self.me).child('tasks').child(self.d).remove() 
      except:
           print("could not see:", tk)
           
           pass
       

#Task("alassanet076@gmail","","","","","").delet_date("2024-01-21 00:00:00")

