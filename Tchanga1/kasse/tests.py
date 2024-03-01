from django.test import TestCase
from datetime import datetime
from .import views #.select ,db,datetim,create_date
# Create your tests here.
select=views.select
datetim=views.datetim
create_date=views.create_date
db=views.db
f=datetim.datetime.now()

#t=create_date(30,f)
#t=create_date(1,datetim.datetime(f.year,f.month,f.day-1))
t=str(datetime.strptime(f"{f.year}-{f.month}-{f.day-1}",'%Y-%m-%d'))
f=str(datetime.strptime(f"{f.year}-{f.month}-{f.day-23}",'%Y-%m-%d'))

#t=str(datetime.strptime(f"{t.year}-{t.month}-{t.day}",'%Y-%m-%d'))
me="alassanet076@gmail"
sec="Altag"
#ob=
obj={'begin':f,'end':t,'budget':100,'newbudget':100,'counter':500,'newcounter':79,'automate':True}#{"begin":f,"end":t}

def test_markets_view(me,objet,update):
 init=select([db,me,"kasse","sectors",objet],{},"get")
 select([db,me,"kasse","sectors"],{objet:update},"update")
 upated=select([db,me,'kasse','sectors',objet],{},'get')
 #print(f"Object {init} muss not be = object {upated}")
 
 sc=select([db,me,"kasse","sectors"],{},"get")
 for se in sc:
  o=select([db,me,'kasse','sectors',se],{},"get")
  nw=datetim.datetime.now()
  #t=create_date(30,f)
  f=datetime.strptime(o["begin"].split(' 00:00:00')[0],'%Y-%m-%d')
  t=datetime.strptime(o["end"].split(' 00:00:00')[0],'%Y-%m-%d')
  if f<=nw and t>=nw:
    print("#"*29)
    print("Testing uptodate sectors")
    o["rest"]="{:.2f}".format(o["newbudget"]-o["newcounter"])
    o["newbudget"]="{:.2f}".format(o["newbudget"])
    print(f"False = {o==upated}")
  elif t<nw and o["automate"]:
    print("#"*29)
    print("Testing expired sectors")
    print(f"{o['automate']} = {upated['automate']}")
    print(f"True= {objet==se}")
    name=se
    period=t-f #o["end"]-o["begin"]
    period=period.days
    f=create_date(1,t)
    t=create_date(period,f)
    print("True=",datetime.strptime(upated['end'].split(' 00:00:00')[0],'%Y-%m-%d')==datetime.strptime(update['end'].split(' 00:00:00')[0],'%Y-%m-%d'))
    print("False =",datetime.strptime(init['end'].split(' 00:00:00')[0],'%Y-%m-%d')==datetime.strptime(upated['end'].split(' 00:00:00')[0],'%Y-%m-%d'))
    rest = o["newbudget"]-o["newcounter"]
    o["newbudget"]=o["budget"]+rest  #wbudget=o["budget"]+rest#
    
    o["newcounter"]=0 #newcounter=0#
    #o["newcounter"]=o["newcounter"]
    o["begin"]=str(f)
    o["end"]=str(t)
    #o['automate']=True
   # o["budget"]=o["budget"]
    #o["newbudget"]
    
    #o={'begin':f,"end":t,"budget":o["budget"],'newbudget':nwbudget,"newcounter":0,'counter':o['counter'],'automate':True}
    fresh={name:o}
    print(select([db,me,"kasse","sectors"],fresh,"update"))
    fin=select([db,me,"kasse","sectors",objet],{},"get")
    print("nwbudget False=",fin["newbudget"]==upated["newbudget"])
    print(" begin False=",fin["begin"]==upated["begin"])
    print(" end False=",fin["end"]==upated["end"])
    print("newsector False=",select([db,me,'kasse','sectors',objet],{},'get')==upated)
    
class test_case(TestCase):
    def test_example(self):
        self.assertEqual(1 + 1, 2)
    
    test_markets_view(me=me,objet=sec,update=obj) 
    
    
 
    
    