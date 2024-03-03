let yes = document.querySelectorAll(".yesno"),
plus = document.getElementById("plus"),
sector = document.getElementById("sector"),
losdiv = document.getElementById("losdiv"),
stock = document.getElementById("stock"),
end = document.getElementById("end"),
beging = document.getElementById("begin"),
 num=document.getElementById("num"),
 marktSubmit=document.querySelectorAll(".marktSubmit"),
 sectors=document.querySelectorAll(".sectors"),
 goodId=document.querySelectorAll(".goodId"),
 goods=document.querySelectorAll(".goods"),
 givelist=document.getElementById("givelist"),
 pluslist=document.getElementById("pluslist"),
 checkSector=document.querySelectorAll(".checkSector"),
 sectionId=document.getElementById("sectionId"),
 //deletlist=document.getElementById("del"),
 anul=document.querySelectorAll(".anul"),
 upgoodChek=document.querySelectorAll(".upgood"),
 upgoodStock=document.getElementById("goodstock"),
 upListCheck=document.querySelectorAll('.uplist')


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

focus("brow","upd")

focus("brow","del")

focus('sectors','btn')

function manageBusket(check,stock){
    for (let i=0;i<check.length;i++){
        check[i].addEventListener("change",(event)=>{
            chk=event.target
            for(let j=0;j<check.length;j++){
                let upgoodStock=document.getElementById(stock)
                let  stk=upgoodStock.value
                if(!check[j].checked && stk.includes(check[j].name)){
                   stk=stk.replace("41259"+check[j].name,"")
                   upgoodStock.value=stk
                   console.log("1",stk)
                }else if(check[j].checked && !stk.includes(check[j].name)){
                    stk=`${stk}41259${check[j].name}`
                    upgoodStock.value=stk
                    console.log("2",stk)
                }
            }
        })
    }
}

manageBusket(upgoodChek,"goodstock")

manageBusket(upListCheck,"liststock")

 ev=new Event("click")

 setInterval(()=>{
    if (new Date().getHours()===0&& new Date().getMinutes()===0 && new Date().getSeconds()<1){
        
        location.reload()
    }
},1000)

for(let i=0;i<checkSector.length;i++){
    checkSector[i].addEventListener("change",(event)=>{
        let check=event.target
    sectionId.value=check.name
    console.log(sectionId.value)
    for(let j=0;j<checkSector.length;j++){
        if(checkSector[j] !==check){
            checkSector[j].checked=false
        }
    }

    })
}

for(let i=0;i<sectors.length;i++){
    sectors[i].addEventListener("click",(event)=>{
        console.log("EVENT",event.target.className)
        if(event.target.className !=="fa-solid fa-pen"){
            marktSubmit[i].dispatchEvent(ev)
            marktSubmit[i].click()
            console.log(i)
        }
        
    })
}

for(let i=0; i<yes.length;i++){
    yes[i].addEventListener("change",(event)=>{
        let c=event.target;
        document.getElementById('checker').value=c.id
        c.name=c.id
        console.log(c.id,"i<=d:name=>",c.name)
        yes.forEach(el=>{
            if(el !==c){
                el.checked=false

            }
        })
    })
}


let prod=0

for (let i=0;i<goods.length;i++){
    goods[i].addEventListener("change",(event)=>{
        let targ = event.target
        let korb=document.getElementById("korb")
        let goodnum=document.getElementById("goodnum")
        if(targ.checked){
            goodId[i].name="good"+prod
            console.log(goodId[i].value)
            goodnum.value=prod
            
            korb.textContent=parseInt(korb.textContent)+1
            prod+=1
            console.log("n:",goodnum.value)
        }else{
            goodId[i].name=""
            console.log(goodId[i].value)

            prod-=1
            if(parseInt(korb.textContent)>0){
                korb.textContent=parseInt(korb.textContent)-1
            }
            
            
            goodnum.value=prod
            console.log("nn:",goodnum.value)
        }
        

    })
}


let indx=0
if(plus){
plus.addEventListener("click",()=>{
    let f=document.getElementById("begin").textContent
    let t=document.getElementById("to").textContent
    let s = document.getElementById("sector").textContent
    let b=document.getElementById("budget").textContent

    let nf = document.createElement("input")
    let nt = document.createElement("input")
    nf.type="datetime-local"
    nt.type="datetime-local"
    nf.name="f"+indx
    nt.name="t"+indx
    nf.textContent=f
    nt.textContent=t
    let bdg = document.createElement("input")
    bdg.name="b"+indx
    let ns = document.createElement("input")
    ns.name="s"+indx
    ns.textContent=s
    let lab = document.createElement("label")
    lab.textContent="Automaticaly reusable ?"
    let ch = document.createElement("input")
    ch.name="c"+indx
    ch.textContent=yes.
    num.textContent=indx

})
}

async function toDelete(id){

    fetch(`/del/${id}`)
    .then(res =>{
        res.text()
    }).then(data=>console.log(data))
     .catch(e=>{throw Error(`I was confronted with an error : ${e}`)})
}

//if (anul){
    anul.forEach(el=>{
        el.addEventListener("click",()=>{
            
            console.log(el.id)
            toDelete(el.id)
            location.reload()
        })
    })
//}

function prepareCliendata(){
    let identity=document.getElementById("letter")
    
    //let data={}
    let secs=new Date().getSeconds()
    let dateInfo=`${new Date().getFullYear()}-${new Date().getMonth()}-${new Date().getDate()}:${new Date().getHours()}:${new Date().getMinutes()}:${secs}`
    let m=identity.value
    //console.log("m:",m)
    if (m !=="" && m !==" " && m){
        console.log("NOOO !")
        let m1=m
        m.includes("TIME")?m1=m.split("TIME")[0]:m1=m
        document.getElementById("letter").value=`${m1}TIME${dateInfo}`
        //let v=document.getElementById("letter")
        //console.log(v.value)
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
    let signaler=document.getElementById("signal").textContent
    let letter1=letter.value
    console.log(`signaler ==="":`,signaler ==="")
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
        
        if(ns-sec1>60000){//&& signaler.textContent !=="mon")
            console.log("signaler:",signaler)
            let comminicat=document.getElementById('com')

            comminicat.addEventListener("click",()=>prepareCliendata())
            comminicat.dispatchEvent(ev)
            comminicat.click()
            console.log("one minute ...")
            //changeMonth()
          }
    }else{ //if(signaler.textContent !=="mon")
        console.log("signaler2:",signaler)
        let comminicat=document.getElementById('com')

       comminicat.addEventListener("click",()=>prepareCliendata())
        comminicat.dispatchEvent(ev)

        comminicat.click()
        ///changeMonth()
        console.log("did not see Time in " )
    }
  
}
let signaler=document.getElementById("signal").textContent
if (signaler ==="" || signaler===" "){
    lauch()
}

