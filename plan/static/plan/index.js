
let timeInput= document.getElementById("timput")
let tim= document.getElementById("time")

let hd= document.getElementById("head")
let addForm = document.getElementById("addform")
let daily = document.getElementById("daily")
let los0 = document.getElementById("los0")
let onemore = document.getElementById("onemore")
let actsdiv= document.getElementById("actsdiv")

let senddiv= document.getElementById("senddiv")
let times = document.querySelectorAll(".times")
let acts = document.querySelectorAll(".act")
let percents = document.querySelectorAll(".percent")
let ench = document.querySelectorAll(".ench")

let wdate = document.querySelectorAll(".wdate")
let wtask= document.querySelectorAll(".wtask")
let wtask1= document.querySelectorAll(".wtask1")
let enchClass = "fa-solid fa-circle-dot ench"
let taskElement=document.querySelectorAll(".tks")
let head=document.getElementById("head")
let dayIc=document.getElementById("day")
let tchanger=document.getElementById("tchanger")
let timereserve =document.getElementById("timereserve")
let timereserve1 =document.getElementById("timereserve1")
let anul=document.querySelectorAll(".anul")
let pen=document.querySelectorAll(".fa-pen")
let trash = document.querySelectorAll(".fa-trash-can")
let deletesValue=document.getElementById('deletes')
let sendDelete =document.getElementById('deleteb')
let pointedRow = document.querySelectorAll(".pointed-row")
let deleteOrEdit=document.querySelectorAll(".edit-delete")
let container=document.getElementById('container'),
loading=document.getElementById('load'),
html5=document.querySelector('.html5')

let ev = new Event("click")

//manage loading
document.addEventListener("DOMContentLoaded",()=>{
    try{
        loading.style.display="block"
        html5.id="html"
        
    }
    catch{

    }
   
})

window.addEventListener("load",()=>{
    loading.style.display="none"
    container.style.display="block"
    html5.id=""
    
})

//handle hide an show of edit and delete icones

function focus(parent,child){
    let pointedRow= document.querySelectorAll(`.${parent}`) //".pointed-row"
    let deleteOrEdit=document.querySelectorAll(`.${child}`)
    for(let i=0;i<pointedRow.length;i++){
        let pointed =pointedRow[i]
       let  delOrEd=deleteOrEdit[i]
        pointed.addEventListener("mouseenter",()=>{
         delOrEd.style.visibility="visible"
        })
        pointed.addEventListener("mouseleave",()=>{
            delOrEd.style.visibility="hidden"
           })
    
    }
}

focus("pointed-row","edit-delete")

//Delete week preprogramed task for 
anul.forEach(el=>{
    el.addEventListener("click",()=>{
        timereserve1.value=el.id
        let goAnul=document.getElementById("goAnul")
        goAnul.dispatchEvent(ev)
        goAnul.click()
    })
})
let lin=0
let myPoint=0

function visible(x){
x.style.visibility !=="visible"?x.style.visibility="visible":x.style.visibility="hidden"
}


function progresser(element,complet,current){
let percentage =(current*100)/complet
element.style.background=`linear-gradient(to right,black ${percentage}%, gray ${100-percentage}%)`

percents[myPoint].innerHTML=`<i class="fa-solid fa-arrow-right-long">${Math.round(percentage)}%</i>`

//`-----> ${Math.round(percentage)}%`
}

function getISOWeekNumber(date) {
    const onejan = new Date(date.getFullYear(), 0, 1);
    const weekNum = Math.ceil(((date - onejan) / 86400000 + onejan.getDay() + 1) / 7);

    return weekNum;
  }



let begin=""
let ringed =""

function signal(){
    let aud =new Audio(document.getElementById("day").textContent)
    
    aud.play().catch((e)=>{})
 }


    dayIc.addEventListener("click",()=>{
        signal()
        
       })
       


function pointer(){
let times = document.querySelectorAll(".times")
if (times && times.length>0 && document.getElementById("tab")){
    //implement alarm
     if (begin !==""){
        let  dm =new Date().getMinutes()
        let d0=new Date().getHours()
        let exd =new Date(begin).getHours()
        let exm=new Date(begin).getMinutes()
        
    if (exd==d0 && exm==dm && ringed !==d0 && new Date().getSeconds()<1){
         dayIc.dispatchEvent(ev)
         dayIc.click()
        
         ringed=d0
    }
      
     }


    for (let i=0;i<times.length;i++){
        
        let d=new Date()
        let el=times[i].textContent
        let timeAr=el.split("-")
        let h1 =timeAr[0].split(':')[0], m1= timeAr[0].split(':')[1] //m1=0
        let h2=timeAr[1].split(':')[0],m2=timeAr[1].split(':')[1] //m2=0
        //timeAr[0].includes("a.m.")?h1=timeAr[0].split("a.m.")[0]:h1=timeAr[0].split("p.m.")[0]
        //timeAr[1].includes("a.m.")?h2=timeAr[1].split("a.m.")[0]:h2=timeAr[1].split("p.m.")[0]
        //if (h1.includes(":") ){
            //hh=h1.split(":")
            //h1=parseInt(hh[0])
            //m1=parseInt(hh[1])
        //}

        //if(h2.includes(":")){
           // hh=h2.split(":")
            
            //h2=parseInt(hh[0])
            //m2=parseInt(hh[1])  
        //}
        h1=parseInt(h1)
        m1=parseInt(m1)
        h2=parseInt(h2)
        m2=parseInt(m2)
        let f = d.setHours(h1,m1)
        
        let t = d.setHours(h2,m2)
        
         
        
        if(new Date()>=f && new Date()<=t){
            myPoint=i
            begin=f
            progresser(acts[myPoint],t-f,new Date()-f)
            let nwtaskElement = document.createElement("h1")
            nwtaskElement.className="tks"
            let nwEnch = document.createElement("i")
            nwEnch.className=enchClass
            nwtaskElement.appendChild(nwEnch)
            
            nwtaskElement.insertAdjacentText("beforeend",taskElement[myPoint].textContent)
            //ench[i].
           
            if(taskElement[myPoint].parentNode){
                taskElement[myPoint].parentNode.replaceChild(nwtaskElement,taskElement[myPoint])
                let ench = document.querySelectorAll(".ench")
                ench[myPoint].style.color ="green"
                
              
            }
           
              
        }else{
            //let acts = document.querySelectorAll(".act")
            //let percents = document.querySelectorAll(".percent")
            //let ench = document.querySelectorAll(".ench")
            let taskElement=document.querySelectorAll(".tks")
                
            if(new Date()-t >=0){
                acts[i].style.backgroundColor="black"
            }
            if(taskElement[i].tagName==="H1"){
            let nwtaskElement = document.createElement("h5")
            nwtaskElement.className="tks"
            let nwEnch = document.createElement("i")
            nwEnch.className=enchClass
            nwtaskElement.appendChild(nwEnch)
            
            nwtaskElement.insertAdjacentText("beforeend",taskElement[i].textContent)
            //ench[i].
           
            if(taskElement[i].parentNode){
                taskElement[i].parentNode.replaceChild(nwtaskElement,taskElement[i])
                let ench = document.querySelectorAll(".ench")
                ench[i].style.color =""
                
              
            }
            }///

            ench[i].style.color =""
            ench[i].style.visibility="visible"
            percents[i].innerHTML=``

    }   
    
    }
}
}



setInterval(()=>{
    if (new Date().getHours()===0&& new Date().getMinutes()===0 && new Date().getSeconds()<1){
        
        location.reload()
    }
},1000)


function weekPointer(x,y,z){
    for(let i=0;i<x.length;i++){
        if (y==="w"){
           let wd=new Date(x[i].textContent).getDate()
            if (new Date().getDate()==wd){
                z[i*2].style.backgroundColor="black"
                z[i*2+1].style.backgroundColor="black"
                
            }else{
                z[i].style.backgroundColor=""   
                
            }
        }else if(y==="m"){
           let wd= getISOWeekNumber(new Date(x[i].textContent))
           let cwek=wd= getISOWeekNumber(new Date())
            if (cwek==wd){
                z[i*2].style.backgroundColor="black"
                z[i*2+1].style.backgroundColor="black"
                
            }else{
                z[i].style.backgroundColor=""   
                
            }
        }
        

    }
    
}

if(head.textContent==="WEEKLY PLAN"){
    weekPointer(wtask1,"w",wtask)
    
}else if (head.textContent==="MONTHLY PLAN"){
    weekPointer(wtask1,"m",wtask)
   
}
if(timeInput){
timeInput.addEventListener("change",()=>{
    timereserve.value=timeInput.value


    tchanger.dispatchEvent(ev)
    tchanger.click()
})
}

setInterval(()=>{
    let times = document.querySelectorAll(".times")
    pointer()
    let ench = document.querySelectorAll(".ench")
    if (times.length>0 && ench[myPoint].style.color==="green" ){
    visible(ench[myPoint])
    
    }
},500)

setInterval(()=>{
    let timeInput= document.getElementById("timput")
    if(timeInput && new Date(timeInput.value).getHours()){
        tim.textContent=new Date(timeInput.value).toLocaleString()
        
    }
},1000)

function newRow(){
    lin+=1
    let taksNum= document.getElementById("num")
    let stock = document.getElementById("stock")
    let from = document.getElementById("timF")
    let to = document.getElementById("timT")

    let activity = document.getElementById("act")
    let kat = document.getElementById("typo")

    taksNum.textContent=lin

    let hours1 = document.createElement("input")
    let hours2 = document.createElement("input")
    //let typ = document.createElement("input")
    
    hours1.type="time"
    hours2.type="time"
    hours1.name="timF"+lin
    hours1.value=from.value
    from.value=""
    hours2.name="timT"+lin
    hours2.value=to.value
    to.value=""
    let act = document.createElement("input")
    let ka = document.createElement("input")

    let br = document.createElement("br")
    let br1 = document.createElement("br")
    let br0 = document.createElement("br")

    act.name="act"+lin
    ka.name="typo"+lin
    ka.value=kat.value
    //kat.value=""
    act.value=activity.value
    activity.value=""

stock.append(br,br1,hours1,hours2,br0,act,ka)
daily.textContent=lin
}

if(onemore){
onemore.addEventListener("click",()=>{
    
    //timeInput.style.display="none"
    newRow()
    let kat = document.getElementById("hid")
    let los0= document.getElementById("los0")
    los0.style.display="block"
    kat.value=lin
    
})
}

async function getToUpdateObject(id){
    deletesValue.value=`${id}:E`
     sendDelete.dispatchEvent(ev)
     sendDelete.click()
    
}


async function toDelete(id){

     deletesValue.value=`${id}:D`
     sendDelete.dispatchEvent(ev)
     sendDelete.click()
}

pen.forEach(el=>{
    el.addEventListener("click",()=>{
    let id=el.id
    getToUpdateObject(id)
    })
    
})

trash.forEach(el=>{
    el.addEventListener("click",()=>{
    let id=el.id
    toDelete(id)
    //location.reload()
    })
    
})


function prepareCliendata(){
    let identity=document.getElementById("letter")
    
    //let data={}
    let secs=new Date().getSeconds()
    let dateInfo=`${new Date().getFullYear()}-${new Date().getMonth()}-${new Date().getDate()}:${new Date().getHours()}:${new Date().getMinutes()}:${secs}`
    let m=identity.value
    
    if (m !=="" && m !==" " && m){
        
        let m1=m
        m.includes("TIME")?m1=m.split("TIME")[0]:m1=m
        document.getElementById("letter").value=`${m1}TIME${dateInfo}`
        
    }else{
        m=localStorage.getItem('https://tchanga12x.onrender.com1')
        
            m=m.split("TIME")[0]+"TIME"+dateInfo
            document.getElementById("letter").value=m
       
    }
   
    if (m.includes("TIME")){
        m=m.split("TIME")[0]
    }
        
    localStorage.setItem('https://tchanga12x.onrender.com1',`${m}TIME${dateInfo}`)
    
}

setInterval(()=>{
    letter0.style.display='none' 
},1000)



const lauch=()=>{
    let letter=document.getElementById("letter")
    let signaler=document.getElementById("signal").textContent
    let letter1=letter.value
    
    if(letter1.includes("TIME")){
        let s =letter1.split("TIME")[1]
        let t1=s.split(":")[0]
        let h=s.split(":")[1]
        h=parseInt(h)
        let m=s.split(":")[2]
        m=parseInt(m)
        let sec=s.split(":")[3]
        sec=parseInt(sec)
        let y=t1.split("-")[0]
        y=parseInt(y)
        let ma=t1.split("-")[1]
        ma=parseInt(ma)
        let d=t1.split("-")[2]
        d=parseInt(d)
        let sec1=new Date()
        sec1.setFullYear(y)
        sec1.setMonth(ma)
        sec1.setDate(d)
        sec1.setHours(h)
        sec1.setMinutes(m)
        sec1.setSeconds(sec)

        let ns=new Date()
       
        if(ns-sec1>60000){//&& signaler.textContent !=="mon")
            
            let comminicat=document.getElementById('com')

            comminicat.addEventListener("click",()=>prepareCliendata())
            comminicat.dispatchEvent(ev)
            comminicat.click()
           
            //changeMonth()
          }
    }else{ //if(signaler.textContent !=="mon")
        
        let comminicat=document.getElementById('com')

       comminicat.addEventListener("click",()=>prepareCliendata())
        comminicat.dispatchEvent(ev)

        comminicat.click()
        ///changeMonth()
       
    }
  
}
let signaler=document.getElementById("signal").textContent
if (signaler ==="" || signaler===" "){
    lauch()
}


// get new month date on change
const changeMonth=()=>{
    let monSubmit=document.getElementById("monSubmit")
let monSel=document.getElementById("msel")
if (monSubmit){
    monSel.addEventListener("change",()=>{
      
        monSubmit.dispatchEvent(ev)
        monSubmit.click()
       
    })
}
}

changeMonth()

