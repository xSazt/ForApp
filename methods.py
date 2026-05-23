import json

class Access:
    def __init__(self):

        # Abrir archivo con los usuarios
        with open("users.json",mode="r",encoding="utf-8") as rawUsers:
            # Guardar datos como type Dict
            self.users=json.load(rawUsers)
        with open("userData.json",mode="r",encoding="utf-8") as rawUserData:
            # Guardar datos como type Dict
            self.userData=json.load(rawUserData)

    def login(self,correo,contraseña):
        if correo not in self.users:
            return "UserNotFound"
        if contraseña == self.users[correo]["password"]:
            return 1
        else:
            return "IncorrectPassword"

    def register(self,correo,contraseña,nombre="",telefono="",direccion="",universidad=""):

        # Validar correo
        if "@" not in correo:
            return "InvalidEmail"
        
        # Validar contraseña
        if len(contraseña) < 8:
            return "InvalidPassword"
        
        # Verificar si el correo ya está registrado
        if correo in self.users:
            return "UserAlreadyExists"
        
        # Si pasa todos los controles se registra el usuario
        self.users[correo]={"password":contraseña,"telefono":telefono,"nombre":nombre,"direccion":direccion,"universidad":universidad}
        self.userData[correo]=self.USER_DATA_TEMPLATE
        with open("users.json", "w") as rawUsers:
            json.dump(self.users, rawUsers, indent=4)
        with open("userData.json", "w") as rawUserData:
            json.dump(self.userData, rawUserData, indent=4)
            return 1

    USER_DATA_TEMPLATE={
        "widgetSetup":["nextAct",""],
        "Financiero":{
            "divisa":"",
            "presupuesto_mensual":0,
            "gastos": {}
        },
        "Tiempo":{
            "programacion_semanal":{
                "lunes":{
                    
                },
                "martes":{
                    
                },
                "miercoles":{
                    
                },
                "jueves":{
                    
                },
                "viernes":{
                    
                },
                "sabado":{
                    
                },
                "domingo":{
                    
                }
            },
            "otras_programaciones":[]
        }
    }


class ScheduleManagement:
    def __init__(self,email):
        with open("userData.json",mode="r",encoding="utf-8") as rawUserData:
            self.userTimeData=json.load(rawUserData)
        self.email=email
    def add_weekly_task(self,task):
        self.userTimeData[self.email]["Tiempo"]["programacion_semanal"][task["day"]][task["hour"]]=task["desc"]
        with open("userData.json",mode="w",encoding="utf-8") as rawUserData:
            json.dump(self.userTimeData,rawUserData, indent=4)
    def add_other_task(self,task):
        self.userTimeData[self.email]["Tiempo"]["otras_programaciones"].append({"fecha":task["day"],"hora":task["hour"],"desc":task["desc"]})
        with open("userData.json",mode="w",encoding="utf-8") as rawUserData:
            json.dump(self.userTimeData,rawUserData, indent=4)
    def delete_weekly_task(self,task):
        del self.userTimeData[self.email]["Tiempo"]["programacion_semanal"][task["day"]][task["hour"]]
        with open("userData.json",mode="w",encoding="utf-8") as rawUserData:
            json.dump(self.userTimeData,rawUserData, indent=4)
    def delete_other_task(self,task):
        lista_original = self.userTimeData[self.email]["Tiempo"]["otras_programaciones"]
    
        lista_filtrada = [act for act in lista_original if not (act["fecha"] == task["day"] and act["hora"] == task["hour"])]
    
        self.userTimeData[self.email]["Tiempo"]["otras_programaciones"] = lista_filtrada
        with open("userData.json",mode="w",encoding="utf-8") as rawUserData:
            json.dump(self.userTimeData,rawUserData, indent=4)

    def get_all_tasks(self):
        tasks=self.userTimeData[self.email]["Tiempo"]
        weeklyTasks=[]
        otherTasks=[]
        for day in tasks["programacion_semanal"]:
            if tasks["programacion_semanal"][day]:
                for hour,desc in tasks["programacion_semanal"][day].items():
                    if hour[5:]=="PM":
                        hour=str(int(hour[:2])+12)+hour[2:]
                    weeklyTasks.append({"dia":day,"hora":hour[:-2],"desc":desc})
        if tasks["otras_programaciones"]:
            for task in tasks["otras_programaciones"]:
                if task["hora"][5:]=="PM":
                    task["hora"]=str(int(task["hora"][:2])+12)+task["hora"][2:]
                otherTasks.append({"dia":task["fecha"],"hora":task["hora"][:-2],"desc":task["desc"]})
        return [weeklyTasks,otherTasks]