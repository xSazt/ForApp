from datetime import datetime
from zoneinfo import ZoneInfo

from methods import ScheduleManagement

dicc={
    "juandg000003@gmail.com": {
        "Financiero": {
            "divisa": "",
            "presupuesto_mensual": 0,
            "gastos": {}
        },
        "Tiempo": {
            "programacion_semanal": {
                "lunes": {
                    "10:00AM": "hola",
                    "03:00PM": "chao"
                },
                "martes": {
                    "03:33PM": "Almuerzo"
                },
                "miercoles": {
                    "08:30AM": "Desayuno"
                },
                "jueves": {},
                "viernes": {
                    "03:00PM": "xd"
                },
                "sabado": {},
                "domingo": {}
            },
            "otras_programaciones": [
                {
                    "fecha": "28/01/2026",
                    "hora": "08:00AM",
                    "desc": "Inicio de clases"
                }
            ]
        }
    }
}

horario=ScheduleManagement("juandg000003@gmail.com")

tasklist=horario.get_all_tasks()
allNextTasks=[]
now=datetime.now(ZoneInfo("America/Bogota"))
monthday=int(now.strftime("%d"))
month=int(now.strftime("%m"))
year=int(now.strftime("%Y"))
monthlydays=[31,29,30,31,30,31,31,30,31,30,31 if year%4==0 else 28,31,30,31,30,31,31,30,31,30,31]
for task in tasklist[0]:
    if task["dia"]=="lunes":
        task["dia"] = 0
    elif task["dia"]=="martes":
        task["dia"] = 1
    elif task["dia"]=="miercoles":
        task["dia"] = 2
    elif task["dia"]=="jueves":
        task["dia"] = 3
    elif task["dia"]=="viernes":
        task["dia"] = 4
    elif task["dia"]=="sabado":
        task["dia"] = 5
    elif task["dia"]=="domingo":
        task["dia"] = 6

for task in tasklist[0]:
    taskTime=int(str(task["dia"]) + "".join(task["hora"].split(":")))
    taskDay=int(task["dia"])
    currentTime=int(str(now.weekday())+now.strftime("%H%M"))
    if currentTime>=taskTime:
        dmes=monthday+(6-now.weekday())+taskDay
    else:
        dmes=monthday+(taskDay-now.weekday())
    if dmes>monthlydays[month-1]:
        dmes=dmes-monthlydays[month-1]
        month+=1
        if month>12:        
            month=1
            year+=1

    allData=[str(year),str(month),str(dmes),str(task["hora"].split(":")[0]),str(task["hora"].split(":")[1])]
    index=0
    for data in allData:
        if len(str(data))==1:
            allData[index]="0"+str(data)
        index+=1
    allNextTasks.append({"code":"".join(allData),"desc":task["desc"]})

for task in tasklist[1]:
    fecha=task["dia"].split("/")
    hora=task["hora"].split(":")
    allData=[str(fecha[2]),str(fecha[1]),str(fecha[0]),str(hora[0]),str(hora[1])]
    index=0
    
    allNextTasks.append({"code":"".join(allData),"desc":task["desc"]})

nextAct=min(allNextTasks,key=lambda x: x["code"])

