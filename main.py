from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table

from getpass import getpass
import json
import numpy as np

import methods
from InterfaceStrings import Interface

from datetime import datetime
from zoneinfo import ZoneInfo

def main():
    console=Console()
    loggedStatus=False
    loggedEmail=""

    while not loggedStatus:
        access=methods.Access()
        console.print(strToPanel(Interface.ACCESS_MENU))
        userOption=input(">>")

        if userOption == "1":
            LoginOutput=LoginSequence(console,access)
            if LoginOutput:
                loggedStatus=LoginOutput[0]
                loggedEmail=LoginOutput[1]

        elif userOption == "2":
            RegisterSequence(console,access)
        
        elif userOption == "3":
            quit()
        else:
            console.print("[red](!) Ingrese una opción valida[/red]")

    # Main Loop
    while True:
    
        with open("users.json",mode="r",encoding="utf-8") as rawUsers:
            users=json.load(rawUsers)
        with open("userData.json",mode="r",encoding="utf-8") as rawUserData:
            userData=json.load(rawUserData)


            widget1=Widgets(userData[loggedEmail]["widgetSetup"][0],loggedEmail).get_widget()
            widget2=Widgets(userData[loggedEmail]["widgetSetup"][1],loggedEmail).get_widget()

            widgetColumn=Group("",widget1,"",widget2)

            mainMenuLayout=Table(box=None, show_header=False, padding=(0,2))
            mainMenuLayout.add_column("Opciones", vertical="top", width=45)
            mainMenuLayout.add_column("Widgets", vertical="top")

            mainMenuLayout.add_row(Interface.MAIN_MENU.format(Name=users[loggedEmail]["nombre"]) , widgetColumn)

            mainMenu=strToPanel(mainMenuLayout)

            console.print(mainMenu)

        userOption=input(">> ")
        if userOption == "2":
            ScheduleLoop=True
            while ScheduleLoop:
                ScheduleLoop=ScheduleSequence(console,loggedEmail)
        elif userOption == "5":
            quit()

def strToPanel(strName):
    return Panel(strName,title=Interface.APP_TITLE)

def LoginSequence(console,access):
            console.print(strToPanel(Interface.LOGIN))

            console.print("[magenta]--[/magenta]Correo: ",end="")
            email=input()
            console.print("[magenta]--[/magenta]Contraseña: ",end="")
            password=getpass("")

            loginStatus=access.login(email,password)
            if loginStatus == 1:
                return [True,email]
            elif loginStatus == "UserNotFound":
                console.print("[red](!) El correo no está registrado[/red] ")
                return False
            elif loginStatus == "IncorrectPassword":
                console.print("[red](!) Contraseña incorrecta[/red]")
                return False

def RegisterSequence(console,access):

    console.print(strToPanel(Interface.REGISTER))

    console.print("[magenta]--[/magenta]Correo: ",end="")
    email=input()
    console.print("[magenta]--[/magenta]Telefono/Celular: ",end="")
    phone=input()
    console.print("[magenta]--[/magenta]Nombre: ",end="")
    userName=input()
    console.print("[magenta]--[/magenta]Dirección: ",end="")
    adress=input()
    console.print("[magenta]--[/magenta]Universidad: ",end="")
    uni=input()
    console.print("[magenta]--[/magenta]Contraseña: ",end="")
    password=input()
    console.print("[magenta]--[/magenta]Confirmar contraseña: ",end="")
    passwordConfirm=input()

    if password == passwordConfirm:
        registerStatus=access.register(email,password,userName,phone,adress,uni)
        if registerStatus == 1:
            console.print("[green]El usuario se ha registrado correctamente.[/green]")
        elif registerStatus == "InvalidEmail":
            console.print("[red](!) Ingrese un correo valido[/red]")
        elif registerStatus == "InvalidPassword":
            console.print("[red](!) La contraseña debe tener al menos 8 caracteres[/red]")
        elif registerStatus == "UserAlreadyExists":
            console.print("[red](!) Este correo ya se encuentra registrado[/red]")
    else:
        console.print("[red](!) Las contraseñas no coinciden[/red]")


def ScheduleSequence(console, email):
    schedule=methods.ScheduleManagement(email)
    with open("userData.json","r",encoding="utf-8") as rawUserData:
        userSchedule=json.load(rawUserData)[email]["Tiempo"]
        weekly=userSchedule["programacion_semanal"]
        other=userSchedule["otras_programaciones"]
    horas=np.zeros(24)
    horario=Table(title="",show_header=False,show_lines=True)

    horario.add_row("","[magenta]Lunes[/magenta]","[magenta]Martes[/magenta]","[magenta]Miercoles[/magenta]","[magenta]Jueves[/magenta]","[magenta]Viernes[/magenta]","[magenta]Sabado[/magenta]","[magenta]Domingo[/magenta]")
    for day in weekly:
        for hora in weekly[day]:
            if "AM" in hora:
                horas[int(hora.split(":")[0])]+=1
            elif "PM" in hora:
                horas[int(hora.split(":")[0])+12]+=1
    for i in range(len(horas)):
        dailyActs={"lunes":"","martes":"","miercoles":"","jueves":"","viernes":"","sabado":"","domingo":""}
        if horas[i]>0:
            if i>11:
                for day in weekly:
                    if i-12 < 10:
                        index=f"0{i-12}"
                    else:
                        index=str(i-12)
                    actDict={k: v for k, v in weekly[day].items() if k.startswith(index) and "PM" in k}
                    if actDict:
                        dailyActs[day]=next(iter(actDict.values()))
                if i!=23:

                    horario.add_row(f"[magenta]{i-12}:00PM - {i-11}:00PM[/magenta]",dailyActs["lunes"],dailyActs["martes"],dailyActs["miercoles"],dailyActs["jueves"],dailyActs["viernes"],dailyActs["sabado"],dailyActs["domingo"])
                else:
                    horario.add_row(f"[magenta]{i-12}:00PM - 0:00AM[/magenta]",dailyActs["lunes"],dailyActs["martes"],dailyActs["miercoles"],dailyActs["jueves"],dailyActs["viernes"],dailyActs["sabado"],dailyActs["domingo"])
            else:
                for day in weekly:
                    if i < 10:
                        index=f"0{i}"
                    else:
                        index=str(i)
                    actDict={k: v for k, v in weekly[day].items() if k.startswith(index) and "AM" in k}
                    if actDict:
                        dailyActs[day]=next(iter(actDict.values()))
                if i!=11:
                    horario.add_row(f"[magenta]{i}:00AM - {i+1}:00AM[/magenta]",dailyActs["lunes"],dailyActs["martes"],dailyActs["miercoles"],dailyActs["jueves"],dailyActs["viernes"],dailyActs["sabado"],dailyActs["domingo"])
                else:
                    horario.add_row(f"[magenta]{i}:00AM - 12:00PM[/magenta]",dailyActs["lunes"],dailyActs["martes"],dailyActs["miercoles"],dailyActs["jueves"],dailyActs["viernes"],dailyActs["sabado"],dailyActs["domingo"])
    
    panelContent=Group(horario,"",Interface.SCHEDULE_MENU(other))
    console.print(strToPanel(panelContent))

    userOption=input(">> ")
    if userOption == "1":
        taskRegistered=False
        while not taskRegistered:
            console.print(strToPanel(Interface.ADD_TASK_MENU))
            console.print("[magenta]--[/magenta]Tipo de tarea: ",end="")
            taskType=input()
            console.print("[magenta]--[/magenta]Dia: ",end="")
            taskDay=input()
            console.print("[magenta]--[/magenta]Hora: ",end="")
            taskHour=input()
            console.print("[magenta]--[/magenta]Descripción: ",end="")
            taskDesc=input()
        
            #Validación
            if taskType == "1":
                if taskDay.lower() not in ["lunes","martes","miercoles","jueves","viernes","sabado","domingo"]:
                    console.print("[red]Los datos son incoherentes, lee las instrucciones e intenta nuevamente.[/red]")
                    continue
            elif taskType == "2":
                if len(taskDay.split("/")) != 3:
                    console.print("[red]Los datos son incoherentes, lee las instrucciones e intenta nuevamente.[/red]")
                    continue
            else:
                console.print("[red]Los datos son incoherentes, lee las instrucciones e intenta nuevamente.[/red]")
                continue
            if len(taskHour.split(":")) != 2 or taskHour[5:] not in ["AM","PM"]:
                console.print("[red]Los datos son incoherentes, lee las instrucciones e intenta nuevamente.[/red]")
                continue

            if taskType == "1":
                schedule.add_weekly_task({"day":taskDay,"hour":taskHour,"desc":taskDesc})
                console.print("[green]La tarea se ha registrado correctamente[/green]")
                taskRegistered=True
            elif taskType == "2":
                schedule.add_other_task({"day":taskDay,"hour":taskHour,"desc":taskDesc})
                console.print("[green]La tarea se ha registrado correctamente[/green]")
                taskRegistered=True
        return True
    elif userOption == "2":
        taskDeleted=False
        while not taskDeleted:
            console.print(strToPanel(Interface.DELETE_TASK_MENU(userSchedule)))
            console.print("[magenta]--[/magenta]Tipo de tarea: ",end="")
            taskType=input()
            console.print("[magenta]--[/magenta]Dia: ",end="")
            taskDay=input()
            console.print("[magenta]--[/magenta]Hora: ",end="")
            taskHour=input()

            if taskType == "1":
                try:
                    schedule.delete_weekly_task({"day":taskDay,"hour":taskHour})
                    console.print("[green]La tarea se ha eliminado correctamente[/green]")
                    taskDeleted=True
                except:
                    console.print("[red]Algo salió mal, lee las instrucciones e intenta nuevamente[/red]")
            elif taskType == "2":
                try:
                    schedule.delete_other_task({"day":taskDay,"hour":taskHour})
                    console.print("[green]La tarea se ha eliminado correctamente[/green]")
                    taskDeleted=True
                except:
                    console.print("[red]Algo salió mal, lee las instrucciones e intenta nuevamente[/red]")
    elif userOption == "3":
        return False

class Widgets:
    def __init__(self,widgetType,email):
        self.widgetType=widgetType
        self.email=email
    
    def get_widget(self):
        if self.widgetType == "nextAct":
            return self.nextAct()
        else:
            return Panel("Widget no disponible",expand=False)

    def nextAct(self):
        layout=Table(show_lines=False,show_header=False)
        layout.add_row("[magenta]Proxima actividad[/magenta]")
        
        horario=methods.ScheduleManagement(self.email)

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
        if not allNextTasks:
            layout.add_row("[cyan]No hay actividades programadas[/cyan]")
            return layout
        rawNextAct=min(allNextTasks,key=lambda x: x["code"])
        layout.add_row(f"[cyan]{rawNextAct['code'][:4]}-{rawNextAct['code'][4:6]}-{rawNextAct['code'][6:8]} {rawNextAct['code'][8:10]}:{rawNextAct['code'][10:]}[/cyan] - {rawNextAct['desc']}")
        return layout




main()

