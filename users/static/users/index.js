
let timeInput= document.getElementById("timput")
let tim= document.getElementById("time")
let hd= document.getElementById("head")
let addForm = document.getElementById("addform")
let daily = document.getElementById("daily")
let los0 = document.getElementById("los0")
let onemore = document.getElementById("onemore")
let actsdiv= document.getElementById("actsdiv")
let letter0=document.getElementById("letter0")
let senddiv= document.getElementById("senddiv")

let lin=0
const ev=new Event("click")

setInterval(()=>{
    
    let timeInput= document.getElementById("timput")
    if(timeInput && new Date(timeInput.value).getHours()){
        tim.textContent=new Date(timeInput.value).toLocaleString()
        
    }
},1000)

function newRow(){
    lin+=1
    let hours1 = document.createElement("input")
    let hours2 = document.createElement("input")
    hours1.type="time"
    hours2.type="time"
    hours1.name="timF"+lin
    hours2.name="timT"+lin
    let act = document.createElement("input")
    let br = document.createElement("br")
    let br1 = document.createElement("br")
    let br0 = document.createElement("br")

    act.name="act"+lin
actsdiv.append(br,br1,hours1,hours2,br0,act)
daily.textContent=lin
}



function prepareCliendata(){
    let identity=document.getElementById("letter")
    
    //let data={}
    let secs=new Date().getSeconds()
    let dateInfo=`${new Date().getFullYear()}-${new Date().getMonth()}-${new Date().getDate()}:${new Date().getHours()}:${new Date().getMinutes()}:${secs}`
    let m=identity.value
    console.log("m:",m)
    if (m !=="" && m !==" " && m){
        console.log("NOOO !")
        let m1=m
        m.includes("TIME")?m1=m.split("TIME")[0]:m1=m
        document.getElementById("letter").value=`${m1}TIME${dateInfo}`
        let v=document.getElementById("letter")
        console.log(v.value)
    }else{
        m=localStorage.getItem('https://tchanga12x.onrender.com1')
          
        console.log(">>>>>>>")
        
            m=m.split("TIME")[0]+"TIME"+dateInfo
            document.getElementById("letter").value=m
       
    }
   
    if (m.includes("TIME")){
        m=m.split("TIME")[0]
    }
        
    localStorage.setItem('https://tchanga12x.onrender.com1',`${m}TIME${dateInfo}`)
    console.log("DON in manage...")
}

setInterval(()=>{
    letter0.style.display='none' 
},1000)



const lauch=()=>{
    let letter=document.getElementById("letter")
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
        console.log("old:",sec1.toLocaleString(),"nw:",ns.toLocaleString())
        if(ns-sec1>60000){
            let comminicat=document.getElementById('com')

            comminicat.addEventListener("click",()=>prepareCliendata())
            comminicat.dispatchEvent(ev)
            comminicat.click()
            console.log("one minute ...")
          }
    }else{
        let comminicat=document.getElementById('com')

       comminicat.addEventListener("click",()=>prepareCliendata())
        comminicat.dispatchEvent(ev)

        comminicat.click()
        console.log("did not see Time in " )
    }
  
}

lauch()



