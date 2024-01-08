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
 anul=document.querySelectorAll(".anul")


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
    sectors[i].addEventListener("click",()=>{
        marktSubmit[i].dispatchEvent(ev)
        marktSubmit[i].click()
        console.log(i)
    })
}

for(let i=0; i<yes.length;i++){
    yes[i].addEventListener("change",(event)=>{
        let c=event.target;
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

