let timeInput= document.getElementById("timput")
let tim= document.getElementById("time")
let hd= document.getElementById("head")
let addForm = document.getElementById("addform")
let daily = document.getElementById("daily")
let los0 = document.getElementById("los0")
let onemore = document.getElementById("onemore")
let actsdiv= document.getElementById("actsdiv")

let senddiv= document.getElementById("senddiv")

let lin=0

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




